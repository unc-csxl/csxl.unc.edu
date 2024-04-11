from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.entities.academics.section_entity import SectionEntity
from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from backend.models.office_hours.event_status import OfficeHoursEventStatus
from backend.models.office_hours.ticket_state import TicketState
from backend.models.roster_role import RosterRole

from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...database import db_session
from ...entities.office_hours import OfficeHoursEventEntity
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.event import OfficeHoursEvent, OfficeHoursEventDraft
from ...models.office_hours.event_details import OfficeHoursEventDetails
from ...models.user import User

from ..exceptions import ResourceNotFoundException
from ..permission import PermissionService


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
    ) -> OfficeHoursEvent:
        """Creates a new office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDraft to add to table

        Returns:
            OfficeHoursEvent: Object added to table
        """
        # Permissions - Raises Exception if Permission Fails
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_event.oh_section.id
        )

        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                "User is a Student In Section and Do Not Have Permissions to Create an OH Event."
            )
        # Create new object
        oh_event_entity = OfficeHoursEventEntity.from_draft_model(oh_event)

        # Add new object to table and commit changes
        self._session.add(oh_event_entity)
        self._session.commit()

        # Return added object
        return oh_event_entity.to_details_model()

    def update(self, subject: User, oh_event: OfficeHoursEvent) -> OfficeHoursEvent:
        """Updates an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEvent to update in the table

        Returns:
            OfficeHoursEvent: Updated object in table
        """
        # TODO
        return None

    def delete(self, subject: User, oh_event: OfficeHoursEvent) -> None:
        """Deletes an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEvent to delete
        """
        # TODO

    def get_event_by_id(self, subject: User, oh_event_id: int) -> OfficeHoursEvent:
        """Gets an office hour event based on OH event id.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: OfficeHoursEvent id to get the corresponding event for

        Returns:
            OfficeHoursEvent: OH event associated with the OH event id
        """
        # TODO
        # Select all entries in the `Course` table and sort by end date
        query = select(OfficeHoursEventEntity).filter(
            OfficeHoursEventEntity.id == oh_event_id
        )
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(
                f"Event with id: {oh_event_id} does not exist."
            )

        # Good to Go - return the model
        return entity.to_model()

    def get_upcoming_events_by_user(
        self, subject: User, time_range: TimeRange
    ) -> list[OfficeHoursEvent]:
        """Gets all upcoming office hours events for a user.

        Args:
            subject: a valid User model representing the currently logged in User
            time_range: Time range to retrieve events for

        Returns:
            list[OfficeHoursEvent]: upcoming OH events associated with a user
        """
        # TODO
        return None

    def get_event_tickets(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: the OfficeHoursEvent to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent
        """
        # TODO
        return None

    def get_queued_helped_stats_by_oh_event(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> OfficeHoursEventStatus:
        """
        Retrieve queued and called ticket statistics for a specific office hours event.

        Args:
            subject (User): The user object representing the authenticated user making the request.
            oh_event (OfficeHoursEvent): The details of the office hours event.

        Returns:
            OfficeHoursEventStatus: An `OfficeHoursEventStatus` object representing the statistics
                (queued and called ticket counts) for the specified office hours event.

        Raises:
            PermissionError: Raised if the authenticated user (`subject`) is not a member of
                the office hours section associated with the event (`oh_event`).
        """
        # PERMISSIONS: Check If User is an OH Section Member - Exception If Not.
        self._check_user_section_membership(subject.id, oh_event.id)

        # Fetch Queued Tickets and Count
        queued_tickets_query = (
            select(OfficeHoursTicketEntity)
            .filter(OfficeHoursTicketEntity.oh_event_id == oh_event.id)
            .filter(OfficeHoursTicketEntity.state == TicketState.QUEUED)
        )

        queued_ticket_entities = self._session.scalars(queued_tickets_query).all()
        queued_ticket_count = len(queued_ticket_entities)

        # Fetch Called Tickets and Count
        called_tickets_query = (
            select(OfficeHoursTicketEntity)
            .filter(OfficeHoursTicketEntity.oh_event_id == oh_event.id)
            .filter(OfficeHoursTicketEntity.state == TicketState.CALLED)
        )

        called_ticket_entities = self._session.scalars(called_tickets_query).all()
        called_ticket_count = len(called_ticket_entities)

        # Build Event Status Status
        event_status = OfficeHoursEventStatus(
            open_tickets_count=called_ticket_count,
            queued_tickets_count=queued_ticket_count,
        )

        return event_status

    def _check_user_section_membership(
        self,
        user_id: int,
        oh_section_id: int,
    ) -> SectionMemberEntity:
        """Checks if a given user is a member in academic sections that are a part of an office hours section.

           Note: An Office Hours section can have multiple academic sections assoicated with it.

        Args:
            user_id: The id of given User of interest
            oh_section_id: The id of office hours section.
        Returns:
            SectionMemberEntity: `SectionMemberEntity` associated with a given user and academic section

        Raises:
            ResourceNotFoundException if cannot user is not a member in given academic section.
            PermissionError if user creating event is not a UTA/GTA/Instructor
        """

        # Find Academic Section and Their IDs
        academic_sections = (
            self._session.query(SectionEntity)
            .filter(SectionEntity.office_hours_id == oh_section_id)
            .all()
        )

        academic_section_ids = [section.id for section in academic_sections]

        # Find User Academic Section Entity
        section_member_entity = (
            self._session.query(SectionMemberEntity)
            .filter(SectionMemberEntity.user_id == user_id)
            .filter(SectionMemberEntity.section_id.in_(academic_section_ids))
            .first()
        )

        if section_member_entity is None:
            raise PermissionError(
                f"Unable To Find Section Member Entity for user with id:{user_id} in academic section with id:{academic_section_ids}"
            )

        return section_member_entity
