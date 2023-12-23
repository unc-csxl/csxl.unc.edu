"""
The Event Service allows the API to manipulate event data in the database.
"""

from datetime import datetime, timedelta
from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.organization_details import OrganizationDetails

from backend.models.user import User
from ..database import db_session
from backend.models.event import Event, DraftEvent, UserEvent
from backend.models.event_details import EventDetails
from backend.models.event_registration import (
    EventRegistration,
    EventRegistrationStatus,
    UserRegistrationStatus,
)
from backend.models.coworking.time_range import TimeRange
from ..entities import (
    EventEntity,
    EventRegistrationEntity,
)
from .permission import PermissionService
from .exceptions import (
    ResourceNotFoundException,
    EventRegistrationException,
)
from . import UserService

__authors__ = [
    "Ajay Gandecha",
    "Jade Keegan",
    "Brianna Ta",
    "Audrey Toney",
    "Kris Jordan",
]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EventService:
    """Service that performs all of the actions on the `Event` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
        user_svc: UserService = Depends(),
    ):
        """Initializes the `EventService` session"""
        self._session = session
        self._permission = permission
        self._user_svc = user_svc

    def all(self) -> list[EventDetails]:
        """
        Retrieves all events from the table

        Returns:
            list[EventDetails]: List of all `EventDetails`
        """
        # Select all entries in `Event` table
        query = select(EventEntity)
        entities = self._session.scalars(query).all()

        # Convert entities to details models and return
        return [entity.to_details_model() for entity in entities]

    def get_events_in_time_range(self, time_range: TimeRange) -> list[EventDetails]:
        """
        Get events in the time range

        Args:
            subject: The User making the request.
            time_range: The period over which to search for events.

        Returns:
            list[EventDetails]: list of valid EventDetails models representing the events
        """
        event_entities = (
            self._session.query(EventEntity)
            .where(EventEntity.time >= time_range.start)
            .where(EventEntity.time < time_range.end)
        )

        return [entity.to_details_model() for entity in event_entities]

    def get_registered_events_of_user(
        self, subject: User, time_range: TimeRange
    ) -> list[Event]:
        """
        Get registered events for a user in the given time range

        Args:
            subject: The User making the request.
            time_range: The period over which to search for events.

        Returns:
            list[Event]: list of valid Event models representing the events.
        """
        event_registrations = self.get_registrations_of_user(
            subject, subject, time_range
        )

        return [registration.event for registration in event_registrations]

    def create(self, subject: User, event: DraftEvent) -> EventDetails:
        """
        Creates a event based on the input object and adds it to the table.
        If the event's ID is unique to the table, a new entry is added.

        Args:
            subject: a valid User model representing the currently logged in User
            event: a valid Event model representing the event to be added

        Returns:
            EventDetails: a valid EventDetails model representing the new Event
        """

        # Ensure that the user has appropriate permissions to create users
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Otherwise, create new object
        event_entity = EventEntity.from_draft_model(event)

        # Add new object to table and commit changes
        self._session.add(event_entity)
        self._session.commit()

        # Retrieve the detail model of the event created
        event_details = event_entity.to_details_model()

        # Set the user as the organizer of the event
        self.set_event_organizer(subject=subject, event=event_details)

        # Return added object
        # NOTE: Must re-convert the entity to a model again so that the registration
        # for the event organizer is automatically populated
        return event_entity.to_details_model()

    def get_by_id(self, id: int) -> EventDetails:
        """
        Get the event from an id
        If none retrieved, a debug description is displayed.

        Args:
            id: a valid int representing a unique event ID

        Returns:
            Event: Object with corresponding ID

        Raises:
            ResourceNotFoundException when event ID cannot be looked up
        """

        # Query the event with matching id
        entity = self._session.get(EventEntity, id)

        # Check if result is null
        if entity is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Convert entry to a model and return
        return entity.to_details_model()

    def get_events_by_organization(
        self, organization: OrganizationDetails
    ) -> list[EventDetails]:
        """
        Get all the events hosted by an organization with slug

        Args:
            slug: a valid str representing a unique Organization slug

        Returns:
            list[EventDetail]: a list of valid EventDetails models
        """
        # Query the event with matching organization slug
        events = (
            self._session.query(EventEntity)
            .filter(EventEntity.organization_id == organization.id)
            .all()
        )

        # Convert entities to models and return
        return [event.to_details_model() for event in events]

    def update(self, subject: User, event: Event) -> EventDetails:
        """
        Update the event

        Args:
            event: a valid Event model

        Returns:
            EventDetails: a valid EventDetails model representing the updated event object
        """

        # Ensure that the user has appropriate permissions to update users
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Query the event with matching id
        event_entity = self._session.get(EventEntity, event.id)

        # Check if result is null
        if event_entity is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Update event object
        event_entity.name = event.name
        event_entity.time = event.time
        event_entity.description = event.description
        event_entity.location = event.location
        event_entity.public = event.public

        # Save changes
        self._session.commit()

        # Return updated object
        return event_entity.to_details_model()

    def delete(self, subject: User, id: int) -> None:
        """
        Delete the event based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Args:
            id: an int representing a unique event ID
        """

        # Find object to delete
        event = self._session.get(EventEntity, id)

        # Ensure that the user has appropriate permissions to delete users
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Ensure object exists
        if event is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Delete object and commit
        self._session.delete(event)

        # Save changes
        self._session.commit()

    """Event Registration Service Methods"""

    def get_registration(
        self, subject: User, attendee: User, event: EventDetails
    ) -> EventRegistration | None:
        """
        Get a registration of an attendee for an Event.

        Args:
            subject: User requesting the registration object
            attendee: User registered for the event
            event: EventDetails of the event seeking registration for

        Returns:
            EventRegistration or None if no registration found

        Raises:
            UserPermissionException if subject does not have permission
        """
        # Feature-specific authorization: User is unregistering themself
        # Administrative Permission: organization.events.manage : organization/{id}
        if subject.id != attendee.id:
            self._permission.enforce(
                subject,
                "organization.events.manage",
                f"organization/{event.organization.id}",
            )

        # Query for EventRegistration
        event_registration_entity = (
            self._session.query(EventRegistrationEntity)
            .where(EventRegistrationEntity.user_id == attendee.id)
            .where(EventRegistrationEntity.event_id == event.id)
            .one_or_none()
        )

        # Return EventRegistration model or None
        if event_registration_entity is not None:
            return event_registration_entity.to_model()
        else:
            return None

    def is_user_an_organizer(self, user: User, event: EventDetails) -> bool:
        """
        Test whether a user is an organizer of an event.

        Args:
            user: The user to check on event organizer status of.
            event: The event in question.

        Returns:
            bool True if user is an organizer, False otherwise.
        """
        registration = self.get_registration(user, user, event)
        return registration.is_organizer if registration else False

    def get_registrations_of_event(
        self, subject: User, event: EventDetails
    ) -> list[EventRegistration]:
        """
        List the registrations of an event.

        This API endpoint currently requires the subject to be registered as the
        organizer of an event or have administrative permission of action
        "organization.events.manage" for "organization/{organization id}".

        Args:
            subject: The authenticated user making the request.
            event: The event whose registrations are being queried.

        Returns:
            list[EventRegistration]

        Raises:
            UserPermissionException if user is not an event organizer or admin.
        """
        if not self.is_user_an_organizer(subject, event):
            self._permission.enforce(
                subject,
                "organization.events.manage",
                f"organization/{event.organization.id}",
            )

        event_registration_entities = (
            self._session.query(EventRegistrationEntity)
            .where(EventRegistrationEntity.event_id == event.id)
            .all()
        )

        return [entity.to_model() for entity in event_registration_entities]

    def set_event_organizer(
        self, subject: User, event: EventDetails
    ) -> EventRegistration:
        """
        Set the organizer of an event.

        Args:
            subject: User making the registration request
            event: The EventDetails being registered for

        Returns:
            EventRegistration

        """

        # Re-ensure that the user has the correct permissions to run this command
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Add new object to table and commit changes
        event_registration_entity = EventRegistrationEntity(
            user_id=subject.id, event_id=event.id, is_organizer=True
        )
        self._session.add(event_registration_entity)
        self._session.commit()

        # Return registration
        return event_registration_entity.to_model()

    def register(
        self, subject: User, attendee: User, event: EventDetails
    ) -> EventRegistration:
        """
        Register a user for an event.

        Args:
            subject: User making the registration request
            attendee: The user being registered for the event
            event: The EventDetails being registered for

        Returns:
            EventRegistration

        Raises:
            UserPermissionException if subject does not have permission to register user
            EventRegistrationException if the event is full
        """

        # Get the registration status.
        # NOTE: It is preferred to use the service function rather than the list of
        # registrations passed in from `event` in the case that registrations are added
        # between when `event` was fetched and this function runs.
        event_status = self.get_event_registration_status(event.id)

        # Raise exception if event is full.
        if event_status.registration_count >= event.registration_limit:
            raise EventRegistrationException(event.id)

        # Enable idemopotency in returning existing registration, if one exists.
        # Permission to manage / read registration is enforced in EventService#get_registration
        existing_registration = self.get_registration(subject, attendee, event)
        if existing_registration:
            return existing_registration

        # Add new object to table and commit changes
        event_registration_entity = EventRegistrationEntity(
            user_id=attendee.id, event_id=event.id
        )
        self._session.add(event_registration_entity)
        self._session.commit()

        # Return registration
        return event_registration_entity.to_model()

    def unregister(self, subject: User, attendee: User, event: EventDetails) -> None:
        """
        Delete a user's event registration.

        Args:
            subject: User performing the unregister action
            attendee: User whose registration is being deleted
            event: the event the attendee is unregistering for

        Returns:
            None in a successful invocation. Idempotent in the case of not registered.

        Raises:
            UserPermissionException when the user is not authorized to manage the registration.
        """
        # Find registration to delete
        # Permissions for reading/managing registration are enforced in #get_registration
        event_registration = self.get_registration(subject, attendee, event)

        # Ensure object exists
        if event_registration is None:
            return

        # Delete object and commit
        self._session.delete(
            self._session.get(
                EventRegistrationEntity,
                (event_registration.event.id, event_registration.user.id),
            )
        )
        self._session.commit()

    def get_registrations_of_user(
        self, subject: User, user: User, time_range: TimeRange
    ) -> Sequence[EventRegistration]:
        """
        Get a user's registrations to events falling within a given time range.

        Args:
            subject: The User making the request.
            user: The User whose registrations are being requested.
            time_range: The period over which to search for event registrations.

        Returns:
            Sequence[EventRegistration] event registrations

        Raises:
            UserPermissionException when the user is requesting the registrations
            of another user and does not have 'user.event_registrations' permission.
        """
        # Feature-specific authorization: User is getting their own registrations
        # Administrative Permission: user.event_registrations : user/{user_id}
        if subject.id != user.id:
            self._permission.enforce(
                subject,
                "user.event_registrations",
                f"user/{user.id}",
            )

        registration_entities = (
            self._session.query(EventRegistrationEntity)
            .where(EventRegistrationEntity.user_id == user.id)
            .join(EventEntity, EventRegistrationEntity.event_id == EventEntity.id)
            .where(EventEntity.time >= time_range.start)
            .where(EventEntity.time < time_range.end)
        ).all()

        return [entity.to_model() for entity in registration_entities]

    def get_event_registration_status(self, event_id: int) -> EventRegistrationStatus:
        """
        Retrieves the number of registrations for a given event.

        Args:
            event_id: a valid int representing the

        Returns:
            status: a valid EventRegistrationStatus representing the number of registrations for an event
        """
        count = (
            self._session.query(EventRegistrationEntity)
            .where(
                EventRegistrationEntity.event_id == event_id,
                EventRegistrationEntity.is_organizer == False,
            )
            .count()
        )

        status = EventRegistrationStatus(registration_count=count)
        return status

    def event_to_user_event(
        self, event: EventDetails, is_registered: bool
    ) -> UserEvent:
        return UserEvent(
            name=event.name,
            time=event.time,
            location=event.location,
            description=event.description,
            public=event.public,
            registration_limit=event.registration_limit,
            can_register=event.can_register,
            organization_id=event.organization_id,
            id=event.id,
            is_registered=is_registered,
            organization=event.organization,
        )

    def get_by_id_with_registration_status(self, subject: User, id: int) -> UserEvent:
        """
        Get event by id with the logged in user's registration status

        Args:
            subject: The User making the request.
            id: an int representing the

        Returns:
            list[UserEvent]: list of valid UserRegistrationStatus models representing whether or not a user is registered for each event
        """
        event = self.get_by_id(id)
        registration = self.get_registration(subject, subject, event)

        is_registered = registration is not None

        return self.event_to_user_event(event, is_registered)

    def get_events_with_registration_status(
        self, subject: User, time_range: TimeRange
    ) -> list[UserEvent]:
        """
        Get events in the time range with the logged in user's registration status

        Args:
            subject: The User making the request.
            time_range: The period over which to search for event registrations.

        Returns:
            list[UserEvent]: list of valid UserEvent models representing whether or not a user is registered for each event
        """
        events = self.get_events_in_time_range(time_range)

        registered_events = self.get_registered_events_of_user(subject, time_range)

        events_with_status = []
        for event in events:
            is_registered = event in registered_events
            user_event = self.event_to_user_event(event, is_registered)
            events_with_status.append(user_event)

        return events_with_status

    def get_events_by_organization_with_registration_status(
        self, subject: User, organization: OrganizationDetails
    ) -> list[EventDetails]:
        """
        Get all the events hosted by an organization with slug

        Args:
            slug: a valid str representing a unique Organization slug

        Returns:
            list[EventDetail]: a list of valid EventDetails models
        """
        # Query the event with matching organization slug
        events = self.get_events_by_organization(organization)

        start = datetime.now()
        end = datetime.now() + timedelta(days=365)
        time_range = TimeRange(start=start, end=end)

        registered_events = self.get_registered_events_of_user(subject, time_range)

        events_with_status = []
        for event in events:
            is_registered = event in registered_events
            user_event = self.event_to_user_event(event, is_registered)
            events_with_status.append(user_event)

        # Convert entities to models and return
        return events_with_status
