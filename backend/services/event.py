"""
The Event Service allows the API to manipulate event data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from ..database import db_session
from backend.models.event import Event
from backend.models.event_details import EventDetails
from backend.models.event_registration import EventRegistration, NewEventRegistration
from ..entities import (
    EventEntity,
    OrganizationEntity,
    EventRegistrationEntity,
    UserEntity,
)
from .permission import PermissionService
from .exceptions import ResourceNotFoundException, UserPermissionException
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

    def create(self, subject: User, event: Event) -> EventDetails:
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

        # Checks if the event already exists in the table
        if event.id:
            event.id = None

        # Otherwise, create new object
        event_entity = EventEntity.from_model(event)

        # Add new object to table and commit changes
        self._session.add(event_entity)
        self._session.commit()

        # Return added object
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

    def get_events_from_organization(self, slug: str) -> list[EventDetails]:
        """
        Get all the events hosted by an organization with slug

        Args:
            slug: a valid str representing a unique Organization slug

        Returns:
            list[EventDetail]: a list of valid EventDetails models
        """

        # Query the organization with the matching slug
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == slug)
            .one_or_none()
        )

        # Ensure that the organization exists
        if organization is None:
            return []

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

    def register(
        self, subject: User, user: User, event: EventDetails
    ) -> EventRegistration:
        """
        Register a user for an event.

        Args:
            subject: User making the registration request
            user: The user being registered for the event
            event: The EventDetails being registered for

        Returns:
            EventRegistration

        Raises:
            UserPermissionException if subject does not have permission to register user
        """

        # Enforce feature-specific authorization of a user being permitted
        # to register for an event for themselves. Otherwise, an administrator
        # can register on behalf of another user with organization events management
        # permission.
        if subject.id != user.id:
            self._permission.enforce(
                subject,
                "organization.events.manage",
                f"organization/{event.organization.id}",
            )

        # Add new object to table and commit changes
        event_registration_entity = EventRegistrationEntity(
            user_id=user.id, event_id=event.id
        )
        self._session.add(event_registration_entity)
        self._session.commit()

        # Return registration
        return event_registration_entity.to_model()

    def unregister(self, subject: User, id: int) -> None:
        """
        Delete an event registration based on the provided ID.

        Args:
            subject: User performing the unregister action
            id: an int representing a unique registration ID

        Returns:
            None in a successful invocation

        Raises:
            ResourceNotFoundException when the registration ID is not found
            UserPermissionException when the user is not authorized to delete registration
        """

        # Find object to delete
        event_registration = self._session.get(EventRegistrationEntity, id)

        # Ensure object exists
        if event_registration is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Ensure that the user has appropriate permissions to delete an event registration
        # Feature-specific authorization: User is unregistering themself
        # Administrative Permission: organization.events.manage : organization/{id}
        if subject.id != event_registration.user_id:
            self._permission.enforce(
                subject,
                "organization.events.manage",
                f"organization/{event_registration.event.organization_id}",
            )

        # Delete object and commit
        self._session.delete(event_registration)

        # Save changes
        self._session.commit()
