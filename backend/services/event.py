"""
The Event Service allows the API to manipulate event data in the database.
"""

from typing import Sequence

from fastapi import Depends
from sqlalchemy import func, select, and_, func, or_, exists, or_
from sqlalchemy.orm import Session, aliased
from backend.entities.user_entity import UserEntity
from backend.models.event_registration import EventRegistration
from ..models.public_user import PublicUser
from backend.models.organization_details import OrganizationDetails
from backend.models.pagination import Paginated, PaginationParams
from backend.models.registration_type import RegistrationType

from ..models import User, Event, EventDetails, Paginated, EventPaginationParams
from ..database import db_session
from backend.models.event import Event, DraftEvent, EventOverview
from backend.models.event_details import EventDetails
from backend.models.coworking.time_range import TimeRange
from ..entities import (
    EventEntity,
    EventRegistrationEntity,
)
from ..entities import EventEntity, OrganizationEntity
from .permission import PermissionService
from .exceptions import (
    ResourceNotFoundException,
    EventRegistrationException,
)
from . import UserService
from datetime import datetime

__authors__ = [
    "Ajay Gandecha",
    "Jade Keegan",
    "Brianna Ta",
    "Audrey Toney",
    "Kris Jordan",
]
__copyright__ = "Copyright 2024"
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

    def get_paginated_events(
        self,
        pagination_params: EventPaginationParams,
        subject: User | None = None,
    ) -> Paginated[EventOverview]:
        """List Events.

        Parameters:
            pagination_params: The pagination parameters.

        Returns:
            Paginated[Event]: The paginated list of events.
        """

        statement = select(EventEntity)
        length_statement = select(func.count()).select_from(EventEntity)
        if pagination_params.range_start != "":
            range_start = pagination_params.range_start
            range_end = pagination_params.range_end
            criteria = and_(
                EventEntity.time >= datetime.fromisoformat(range_start),
                EventEntity.time <= datetime.fromisoformat(range_end),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        if pagination_params.filter != "":
            query = pagination_params.filter

            criteria = or_(
                EventEntity.name.ilike(f"%{query}%"),
                EventEntity.description.ilike(f"%{query}%"),
                exists().where(
                    OrganizationEntity.id == EventEntity.organization_id,
                    OrganizationEntity.name.ilike(f"%{query}%"),
                ),
                exists().where(
                    OrganizationEntity.id == EventEntity.organization_id,
                    OrganizationEntity.slug.ilike(f"%{query}%"),
                ),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != "":
            statement = (
                statement.order_by(getattr(EventEntity, pagination_params.order_by))
                if pagination_params.ascending
                else statement.order_by(
                    getattr(EventEntity, pagination_params.order_by).desc()
                )
            )

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(
            items=[entity.to_overview_model(subject) for entity in entities],
            length=length,
            params=pagination_params,
        )

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
            "organization.events.create",
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
        for organizer in event.organizers:
            if organizer.id != None:
                self.set_event_organizer(
                    subject=subject, user_id=organizer.id, event=event_details
                )

        # Return added object
        # NOTE: Must re-convert the entity to a model again so that the registration
        # for the event organizer is automatically populated
        return event_entity.to_details_model(subject)

    def get_by_id(self, id: int, subject: User | None = None) -> EventDetails:
        """
        Get the event from an id
        If none retrieved, a debug description is displayed.

        Args:
            id: a valid int representing a unique event ID
            subject: The User making the request.

        Returns:
            EventDetails: a valid EventDetails model representing the event corresponding to the ID

        Raises:
            ResourceNotFoundException when event ID cannot be looked up
        """

        # Query the event with matching id
        entity = self._session.get(EventEntity, id)

        # Check if result is null
        if entity is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Convert entry to a model and return
        return entity.to_details_model(subject)

    def get_events_by_organization(
        self, organization: OrganizationDetails, subject: User | None = None
    ) -> list[EventDetails]:
        """
        Get all the events hosted by an organization with slug

        Args:
            slug: a valid str representing a unique Organization slug
            subject: The User making the request.

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
        return [event.to_details_model(subject) for event in events]

    def update(self, subject: User, event: Event) -> EventDetails:
        """
        Update the event

        Args:
            event: a valid Event model

        Returns:
            EventDetails: a valid EventDetails model representing the updated event object
        """

        # Query the event with matching id
        event_entity = self._session.get(EventEntity, event.id)

        # Check if result is null
        if event_entity is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Ensure that the user has appropriate permissions to update event information
        event_details = event_entity.to_details_model(subject)

        # If not organizer, enforce permissions
        if not event_details.is_organizer:
            self._permission.enforce(
                subject,
                "organization.events.update",
                f"organization/{event.organization_id}",
            )

        # Update event object
        event_entity.name = event.name
        event_entity.time = event.time
        event_entity.description = event.description
        event_entity.location = event.location
        event_entity.public = event.public
        event_entity.registration_limit = event.registration_limit

        # If attempting to edit organizers, enforce registration management permissions
        if event.organizers != event_details.organizers:
            self._permission.enforce(
                subject,
                "organization.events.manage_registrations",
                f"organization/{event.organization_id}",
            )
            # Remove organizers not in new organizers
            for organizer in event_details.organizers:
                if organizer not in event.organizers:
                    event_registration_entity = self._session.get(
                        EventRegistrationEntity, (event.id, organizer.id)
                    )
                    self._session.delete(event_registration_entity)

            # Add organizers not in current organizers
            for organizer in event.organizers:
                if organizer not in event_details.organizers:
                    event_registration_entity = self._session.get(
                        EventRegistrationEntity, (event.id, organizer.id)
                    )

                    if event_registration_entity is None:
                        if organizer.id != None:
                            self.set_event_organizer(
                                subject, organizer.id, event_details
                            )
                            continue

                    event_registration_entity.registration_type = (
                        RegistrationType.ORGANIZER
                    )

        # Save changes
        self._session.commit()

        # Return updated object
        return event_entity.to_details_model(subject)

    def delete(self, subject: User, id: int) -> None:
        """
        Delete the event based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Args:
            id: an int representing a unique event ID
        """

        # Find object to delete
        event = self._session.get(EventEntity, id)

        # Ensure object exists
        if event is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Ensure that the user has appropriate permissions to delete users
        self._permission.enforce(
            subject,
            "organization.events.delete",
            f"organization/{event.organization_id}",
        )

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
            PublicUser or None if no registration found

        Raises:
            UserPermissionException if subject does not have permission
        """
        # Administrative Permission: organization.events.view : organization/{id}
        if subject.id != attendee.id:
            self._permission.enforce(
                subject,
                "organization.events.manage_registrations",
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

    def get_registrations_of_event(
        self, subject: User, event: EventDetails
    ) -> list[PublicUser]:
        """
        List the registrations of an event.

        This API endpoint currently requires the subject to be registered as the
        organizer of an event or have administrative permission of action
        "organization.events.view" for "organization/{organization id}".

        Args:
            subject: The authenticated user making the request.
            event: The event whose registrations are being queried.

        Returns:
            list[PublicUser]

        Raises:
            UserPermissionException if user is not an event organizer or admin.
        """
        if not event.is_organizer:
            self._permission.enforce(
                subject,
                "organization.events.manage_registrations",
                f"organization/{event.organization.id}",
            )

        event_registration_entities = (
            self._session.query(EventRegistrationEntity)
            .where(EventRegistrationEntity.event_id == event.id)
            .all()
        )

        return [entity.to_flat_model() for entity in event_registration_entities]

    def set_event_organizer(
        self, subject: User, user_id: int, event: EventDetails
    ) -> PublicUser:
        """
        Set the organizer of an event.

        Args:
            subject: User making the registration request
            event: The EventDetails being registered for

        Returns:
            PublicUser

        """

        # Re-ensure that the user has the correct permissions to run this command
        self._permission.enforce(
            subject,
            "organization.events.manage_registrations",
            f"organization/{event.organization_id}",
        )

        # Add new object to table and commit changes
        event_registration_entity = EventRegistrationEntity(
            user_id=user_id,
            event_id=event.id,
            registration_type=RegistrationType.ORGANIZER,
        )
        self._session.add(event_registration_entity)
        self._session.commit()

        # Return registration
        return event_registration_entity.to_flat_model()

    def register(
        self, subject: User, attendee: User, event: EventDetails
    ) -> PublicUser:
        """
        Register a user for an event.

        Args:
            subject: User making the registration request
            attendee: The user being registered for the event
            event: The EventDetails being registered for

        Returns:
            PublicUser

        Raises:
            UserPermissionException if subject does not have permission to register user
            EventRegistrationException if the event is full
        """
        if subject.id != attendee.id and not event.is_organizer:
            self._permission.enforce(
                subject,
                "organization.events.manage_registrations",
                f"organization/{event.organization.id}",
            )

        # Get the registration status.
        # NOTE: It is preferred to use the service function rather than the list of
        # registrations passed in from `event` in the case that registrations are added
        # between when `event` was fetched and this function runs.

        # Raise exception if event is full.
        if event.registration_count >= event.registration_limit:
            raise EventRegistrationException(event.id)

        # Enable idemopotency in returning existing registration, if one exists.
        # Permission to manage / read registration is enforced in EventService#get_registration
        existing_registration = self.get_registration(subject, attendee, event)
        if existing_registration:
            return EventRegistrationEntity.from_model(
                existing_registration
            ).to_flat_model()

        # Add new object to table and commit changes
        event_registration_entity = EventRegistrationEntity(
            user_id=attendee.id,
            event_id=event.id,
            registration_type=RegistrationType.ATTENDEE,
        )
        self._session.add(event_registration_entity)
        self._session.commit()

        # Return registration
        return event_registration_entity.to_flat_model()

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

        # Ensure object exists and user is not organizer of event
        if (
            event_registration is None
            or event_registration.registration_type == RegistrationType.ORGANIZER
        ):
            return

        # Delete object and commit
        self._session.delete(
            self._session.get(
                EventRegistrationEntity,
                (event.id, attendee.id),
            )
        )
        self._session.commit()

    def get_registrations_of_user(
        self, subject: User, user: User, time_range: TimeRange
    ) -> Sequence[PublicUser]:
        """
        Get a user's registrations to events falling within a given time range.

        Args:
            subject: The User making the request.
            user: The User whose registrations are being requested.
            time_range: The period over which to search for event registrations.

        Returns:
            Sequence[PublicUser] event registrations

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

        return [entity.to_flat_model() for entity in registration_entities]

    def get_registered_users_of_event(
        self, subject: User, event_id: int, pagination_params: PaginationParams
    ) -> Paginated[User]:
        """
        Get registered users of event in a paginated list.

        Args:
            subject: The user performing the action.
            event_id: a valid int representing a unique Event
            pagination_params: The pagination parameters.

        Returns:
            Paginated[User]: The paginated list of users.

        Raises:
            PermissionException: If the subject does not have the required permission.
        """
        event_entity = self._session.get(EventEntity, event_id)
        event = event_entity.to_details_model(subject)

        # Ensure that the user has appropriate permissions to view event information
        if not event.is_organizer:
            self._permission.enforce(
                subject,
                "organization.events.manage_registrations",
                f"organization/{event.organization_id}",
            )

        # Create an alias for the EventRegistrationEntity to be used in join
        EventRegistrationAlias = aliased(EventRegistrationEntity)

        # Statement below corresponds to the following SQL Query (when executed)
        # Returns all UserEntity objects for EventRegistrations that match the event_id
        # SELECT UserEntity.*
        # FROM UserEntity JOIN EventRegistrationEntity ON EventRegistrationEntity.user_id == UserEntity.id
        # WHERE EventRegistrationEntity.event_id = :event_id
        statement = (
            select(UserEntity)
            .join(
                EventRegistrationAlias, EventRegistrationAlias.user_id == UserEntity.id
            )
            .where(
                EventRegistrationAlias.event_id == event_id,
                EventRegistrationAlias.registration_type == RegistrationType.ATTENDEE,
            )
        )

        # Statement to determine number of rows in query result
        length_statement = (
            select(func.count())
            .select_from(UserEntity)
            .join(
                EventRegistrationAlias, EventRegistrationAlias.user_id == UserEntity.id
            )
            .where(
                EventRegistrationAlias.event_id == event_id,
                EventRegistrationAlias.registration_type == RegistrationType.ATTENDEE,
            )
        )

        # Filter results by query
        if pagination_params.filter != "":
            query = pagination_params.filter
            criteria = or_(
                UserEntity.first_name.ilike(f"%{query}%"),
                UserEntity.last_name.ilike(f"%{query}%"),
                UserEntity.onyen.ilike(f"%{query}%"),
            )

            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        # Calculate where to begin retrieving rows and how many to retrieve
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        # Order results by order by attribute
        if pagination_params.order_by != "":
            statement = statement.order_by(
                getattr(UserEntity, pagination_params.order_by)
            )

        # Retrieve limited items
        statement = statement.offset(offset).limit(limit)

        # Execute statement and retrieve entities
        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        # Convert `UserEntity`s to model and return page
        return Paginated(
            items=[entity.to_model() for entity in entities],
            length=length,
            params=pagination_params,
        )
