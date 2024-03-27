from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...entities.academics.section_member_entity import SectionMemberEntity
from ...models.roster_role import RosterRole
from ...models.coworking.time_range import TimeRange

from ...models.office_hours.event_details import OfficeHoursEventDetails
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...database import db_session
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import OfficeHoursSectionEntity
from ...models.office_hours.section import (
    OfficeHoursSection,
    OfficeHoursSectionDraft,
)
from ...models.office_hours.section_details import OfficeHoursSectionDetails
from ...models.user import User
from ..exceptions import ResourceNotFoundException


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursSectionService:
    """Service that performs all of the actions on the `OfficeHoursSection` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initializes the database session."""
        self._session = session

    def create(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDraft,
        academic_ids: list[int],
    ) -> OfficeHoursSectionDetails:
        """Creates a new office hours section.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSection to add to table

        Returns:
            OfficeHoursSectionDetails: Object added to table
        """

        # Permissions - Checks If User Has Proper Role to Create and If a Member in a Section
        self._check_membership_and_edit_permissions(subject.id, academic_ids)

        # Create new object
        oh_section_entity = OfficeHoursSectionEntity.from_draft_model(oh_section)

        # Add new object to table and commit changes
        self._session.add(oh_section_entity)

        # Save Changes To Get OH Section ID
        self._session.commit()

        # Query and Execution to Update All Academic Section With New OH Section ID
        query = select(SectionEntity).where(SectionEntity.id.in_(academic_ids))
        academic_section_entities = self._session.scalars(query).all()

        # Check If All Academic Sections Were Queried
        if len(academic_section_entities) != len(academic_ids):
            raise ResourceNotFoundException(
                f"Unable to Fetch All Academic Sections. Only {len(academic_section_entities)} out of {len(academic_ids)} was found."
            )

        # Now Update Office Hours ID
        for entity in academic_section_entities:
            entity.office_hours_id = oh_section_entity.id

        self._session.commit()

        # Return added object
        return oh_section_entity.to_details_model()

    def get_all_sections(self, subject: User) -> list[OfficeHoursSectionDetails]:
        """Fetches All Office Hours Sections.

        Args:
            subject: a valid User model representing the currently logged in User

        Returns:
            list[OfficeHoursSectionDetails]: List of all Office Hours Sections
        """
        query = select(OfficeHoursSectionEntity)
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def get_section_by_id(
        self, subject: User, oh_section_id: int
    ) -> OfficeHoursSectionDetails:
        """Returns the office hours section from the table by an OH section id

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section_id: ID of the office hours section to query by.
        Returns:
            OfficeHoursSectionDetails: the office hours section with the given id
        """
        # TODO
        return None

    def get_events_by_section(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDetails,
        time_range: TimeRange | None = None,
    ) -> list[OfficeHoursEventDetails]:
        """Returns all events for a given office hours section

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to get all the events of
        Returns:
            list[OfficeHoursEventDetails]: list of all office hours events for the given section
        """
        # TODO
        # make sure to check if time range is None
        # if time range is not None, you are retrieving upcoming events
        return None

    def get_sections_by_term(
        self, subject: User, term_id: int
    ) -> list[OfficeHoursSectionDetails]:
        """Retrieves all office hours sections from the table by a term.

        Args:
            subject: a valid User model representing the currently logged in User
            term_id: ID of the term to query by.
        Returns:
            list[OfficeHoursSectionDetails]: List of all `OfficeHoursSectionDetails`
        """
        # TODO: this is a WIP!
        # Select all entries in the `OfficeHoursSection` table where their section(s)'s term id == term_id
        query = (
            select(OfficeHoursSectionEntity)
            .join(SectionEntity)
            .where(SectionEntity.term_id == term_id)
            .order_by(OfficeHoursSectionEntity.title)
        )
        entities = self._session.scalars(query).all()

        # Return the model
        return [entity.to_details_model() for entity in entities]

    def get_user_sections_by_term(
        self, subject: User, term_id: int
    ) -> list[OfficeHoursSectionDetails]:
        """Retrieves all office hours sections from the table by a term and specific user.
        Args:
            subject: a valid User model representing the currently logged in User
            term_id: ID of the term to query by.
        Returns:
            list[OfficeHoursSectionDetails]: List of all `OfficeHoursSectionDetails`
        """
        # TODO
        return []

    def get_section_tickets(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets from the table by a section.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHsection
        """
        # TODO
        return None

    def get_user_section_tickets(
        self, subject: User, oh_section_id: int
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all of the subject's office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all of a user's `OfficeHoursTicketDetails` in an OHsection
        """
        # TODO
        return None

    def update(
        self, subject: User, oh_section: OfficeHoursSection
    ) -> OfficeHoursSectionDetails:
        """Updates an OfficeHoursSection.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the updated OfficeHoursSection
        Returns:
            OfficeHoursSectionDetails: updated OfficeHoursSectionDetails
        """
        # TODO
        return None

    def delete(self, subject: User, oh_section: int) -> None:
        """Deletes an office hours section.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to delete
        """
        # TODO

    def _check_membership_and_edit_permissions(
        self,
        user_id: int,
        section_ids: list[int],
    ) -> SectionMemberEntity:
        """Checks if a given user is a member in academic sections and has oh section edit permissions. A UTA/GTA/Instructor has this permission.
        Note: An Office Hours section can have multiple academic sections assoicated with it.
        Args:
            user_id: The id of given User of interest
            section_ids: List of ids of academic section.
        Returns:
            SectionMemberEntity: `SectionMemberEntity` associated with a given user and academic section
        Raises:
            ResourceNotFoundException if cannot user is not a member in given academic section.
            PermissionError if user creating event is not a UTA/GTA/Instructor
        """

        query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user_id)
            .where(SectionMemberEntity.section_id.in_(section_ids))
        )
        # Find User Academic Section Entity
        section_member_entity = self._session.scalars(query).one_or_none()

        if section_member_entity is None:
            raise ResourceNotFoundException(
                f"User has to be a Section Member to Create OH Section. Unable To Find Section Member Entity for User with id: {user_id} in the following Academic Sections of ids: {section_ids}"
            )

        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a Student. User Does not have Permision Create an Office Hours Section."
            )

        return section_member_entity
