from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models.office_hours.oh_ticket_details import OfficeHoursTicketDetails
from ...database import db_session
from ...entities.office_hours.oh_event_entity import OfficeHoursEventEntity
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.oh_event import OfficeHoursEvent, OfficeHoursEventDraft
from ...models.office_hours.oh_event_details import OfficeHoursEventDetails
from ...models.user import User

from ...services.exceptions import ResourceNotFoundException
from ...services.permission import PermissionService


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventService:
    """Service that performs all of the actions on the `OfficeHoursEvent` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def create(
        self, subject: User, oh_event: OfficeHoursEventDraft
    ) -> OfficeHoursEventDetails:
        """Creates a new office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDraft to add to table

        Returns:
            OfficeHoursEventDetails: Object added to table
        """
        #TODO: Add Permissions

        # Create new object
        oh_event_entity = OfficeHoursEventEntity.from_model(oh_event)

        # Add new object to table and commit changes
        self._session.add(oh_event_entity)
        self._session.commit()

        # Return added object
        return oh_event_entity.to_details_model()

    def update(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> OfficeHoursEventDetails:
        """Updates an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEvent to update in the table

        Returns:
            OfficeHoursEventDetails: Updated object in table
        """
        #TODO: Permissions

        # Find the entity to update
        oh_event_entity = self._session.get(OfficeHoursEventEntity, oh_event.id)

        # Raise an error if no entity was found
        if oh_event_entity is None:
            raise ResourceNotFoundException(
                f"Event with id: {oh_event.id} does not exist."
            )

        # Update the entity
        oh_event_entity.type = oh_event.type
        oh_event_entity.description = oh_event.description
        oh_event_entity.location_description = oh_event.location_description
        oh_event_entity.date = oh_event.date
        oh_event_entity.start_time = oh_event.start_time
        oh_event_entity.end_time = oh_event.end_time
        oh_event_entity.room_id = oh_event.room_id

        # Commit changes
        self._session.commit()

        # Return edited object
        return oh_event_entity.to_details_model()

    def delete(self, subject: User, oh_event: OfficeHoursEventDetails) -> None:
        """Deletes an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDetails to delete
        """
        # TODO: Permissions

        # Find the entity to delete
        oh_event_entity = self._session.get(OfficeHoursEventEntity, oh_event.id)

        # Raise an error if no entity was found
        if oh_event_entity is None:
            raise ResourceNotFoundException(f"Event with id: {oh_event.id} does not exist.")

        # Delete and commit changes
        self._session.delete(oh_event_entity)
        self._session.commit()

    def get_oh_event_by_id(
        self, subject: User, oh_event_id: int
    ) -> OfficeHoursEventDetails:
        """Gets an office hour event based on OH event id.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: OfficeHoursEvent id to get the corresponding event for

        Returns:
            OfficeHoursEventDetails: OH event associated with the OH event id
        """
        # Select the event with the corresponding id
        oh_event_entity = self._session.get(OfficeHoursEventEntity, oh_event_id)

        # Raise an error if no entity was found.
        if oh_event_entity is None:
            raise ResourceNotFoundException(f"Event with id: {oh_event_id} does not exist.")

        # Return the details model
        return oh_event_entity.to_details_model()

    def get_upcoming_oh_events_by_user(
        self, subject: User, time_range: TimeRange
    ) -> list[OfficeHoursEventDetails]:
        """Gets all upcoming office hours events for a user.

        Args:
            subject: a valid User model representing the currently logged in User
            time_range: Time range to retrieve events for

        Returns:
            list[OfficeHoursEventDetails]: upcoming OH events associated with a user
        """
        # TODO
        return None

    def get_oh_event_tickets(
        self, subject: User, oh_event: OfficeHoursEventDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: the OfficeHoursEventDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent
        """
        # TODO
        return None
