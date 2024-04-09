from operator import or_
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...entities.office_hours.section_entity import OfficeHoursSectionEntity
from ...entities.academics.section_entity import SectionEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...models.roster_role import RosterRole
from ...services.office_hours.section import OfficeHoursSectionService
from ...models.office_hours.ticket_state import TicketState
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
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
    ) -> OfficeHoursEventDetails:
        """Creates a new office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDraft to add to table

        Returns:
            OfficeHoursEventDetails: Object added to table
        """
        # Permissions - Raises Exception if Permission Fails
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_event.oh_section.id
        )
        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a Student. User does not have permision to create event"
            )

        # Create new object
        oh_event_entity = OfficeHoursEventEntity.from_draft_model(oh_event)

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
        # TODO
        return None

    def delete(self, subject: User, oh_event: OfficeHoursEventDetails) -> None:
        """Deletes an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDetails to delete
        """
        # TODO

    def get_event_by_id(
        self, subject: User, oh_event_id: int
    ) -> OfficeHoursEventDetails:
        """Gets an office hour event based on OH event id.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: OfficeHoursEvent id to get the corresponding event for

        Returns:
            OfficeHoursEventDetails: OH event associated with the OH event id
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

        # Return the model
        return entity.to_details_model()

    def get_upcoming_events_by_user(
        self,
        subject: User,
        time_range: TimeRange,
    ) -> list[OfficeHoursEventDetails]:
        """Gets all upcoming office hours events for a user.

        Args:
            subject: a valid User model representing the currently logged in User
            time_range: Time range to retrieve events for

        Returns:
            list[OfficeHoursEventDetails]: upcoming OH events associated with a user
        """
        query = (
            select(OfficeHoursEventEntity)
            .where(SectionMemberEntity.user_id == subject.id)
            .where(SectionEntity.id == SectionMemberEntity.section_id)
            .where(OfficeHoursSectionEntity.id == SectionEntity.office_hours_id)
            .where(
                OfficeHoursEventEntity.office_hours_section_id
                == OfficeHoursSectionEntity.id
            )
            .where(OfficeHoursEventEntity.start_time < time_range.end)
        )

        entities = self._session.scalars(query).all()
        return [entity.to_details_model() for entity in entities]

    def get_event_tickets(
        self, subject: User, oh_event: OfficeHoursEventDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: the OfficeHoursEventDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent
        """

        section_member_entity = self._check_user_section_membership(
            subject.id, oh_event.oh_section.id
        )
        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a Student. User does not have permision to get all tickets"
            )

        query = (
            select(OfficeHoursTicketEntity)
            .where(OfficeHoursTicketEntity.oh_event_id == oh_event.id)
            .order_by(OfficeHoursTicketEntity.created_at.desc())
        )

        entities = self._session.scalars(query).all()
        return [entity.to_details_model() for entity in entities]

    def get_queued_and_called_event_tickets(
        self, subject: User, oh_event: OfficeHoursEventDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: the OfficeHoursEventDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent
        """

        section_member_entity = self._check_user_section_membership(
            subject.id, oh_event.oh_section.id
        )
        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a Student. User does not have permision to get queue tickets"
            )

        query = (
            select(OfficeHoursTicketEntity)
            .where(OfficeHoursTicketEntity.oh_event_id == oh_event.id)
            .where(
                or_(
                    OfficeHoursTicketEntity.state == TicketState.QUEUED,
                    OfficeHoursTicketEntity.state == TicketState.CALLED,
                )
            )
            .order_by(OfficeHoursTicketEntity.created_at.desc())
        )

        entities = self._session.scalars(query).all()
        return [entity.to_details_model() for entity in entities]

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
            raise ResourceNotFoundException(
                f"Unable To Find Section Member Entity for user with id:{user_id} in academic section with id:{academic_section_ids}"
            )

        return section_member_entity
