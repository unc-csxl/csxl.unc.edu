from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.entities.academics.section_entity import SectionEntity
from backend.entities.academics.section_member_entity import SectionMemberEntity
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
    ) -> OfficeHoursEventDetails:
        """Creates a new office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDraft to add to table

        Returns:
            OfficeHoursEventDetails: Object added to table
        """
        # Permissions - Raises Exception if Permission Fails
        self._check_user_section_membership(subject.id, oh_event.oh_section.id)

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
        # TODO
        return None

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

        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a Student. User does not have permision to create event"
            )

        return section_member_entity
