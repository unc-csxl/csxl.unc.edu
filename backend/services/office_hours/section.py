from datetime import datetime
from fastapi import Depends
from sqlalchemy import and_, not_, select, select, outerjoin, and_, not_
from sqlalchemy import select, not_, and_, union
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session

from ...models.academics.section_member import SectionMember
from ...models.academics.section_member_details import SectionMemberDetails
from ...entities.office_hours.event_entity import OfficeHoursEventEntity
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...entities.academics.section_member_entity import SectionMemberEntity

from ...models.roster_role import RosterRole
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.event import OfficeHoursEvent
from ...models.office_hours.event_details import OfficeHoursEvent
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

        # PERMISSIONS

        # 1. Checks If User Has Proper Role to Create and If is a Member in a Section
        section_member_entity = self._check_membership_and_edit_permissions(
            subject.id, academic_ids
        )

        if section_member_entity.member_role != RosterRole.INSTRUCTOR:
            raise PermissionError(
                f"Section Member is not an Instructor. User Does Not Have Permisions Create an Office Hours Section."
            )
        # 2. Check If Give Academic Sections Already Have an Office Hours Event
        # Query and Execution to Update All Academic Section With New OH Section ID
        query = select(SectionEntity).where(SectionEntity.id.in_(academic_ids))
        academic_section_entities = self._session.scalars(query).all()

        for entity in academic_section_entities:
            if entity.office_hours_id is not None:
                raise Exception("Office Hours Section Already Exists!")

        # Check If All Academic Sections Were Queried
        if len(academic_section_entities) != len(academic_ids):
            raise ResourceNotFoundException(
                f"Unable to Fetch All Academic Sections. Only {len(academic_section_entities)} out of {len(academic_ids)} was found."
            )

        # Create new object
        oh_section_entity = OfficeHoursSectionEntity.from_draft_model(oh_section)

        # Add new object to table and commit changes
        self._session.add(oh_section_entity)

        # Save Changes To Get OH Section ID
        self._session.commit()

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

        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section_id
        )
        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section_id}"
            )

        return entity.to_details_model()

    def get_past_events_by_section(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDetails,
    ) -> list[OfficeHoursEvent]:
        """Returns all events for a given office hours section

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to get all the events of
        Returns:
            list[OfficeHoursEvent]: list of all past office hours events for the given section
        """

        # PERMISSIONS

        # 1. Checks If User Has Proper Role to Get and If is a Member in a Section
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a student. User Does Not Have Permision to get past section events."
            )

        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section.id}"
            )

        oh_events = entity.to_details_model().events
        return [
            oh_event for oh_event in oh_events if oh_event.end_time < datetime.now()
        ]

    def get_upcoming_events_by_section(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDetails,
        time_range: TimeRange,
    ) -> list[OfficeHoursEvent]:
        """Returns all events for a given office hours section

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to get all the events of
            time_range: a TimeRange in which the events should be
        Returns:
            list[OfficeHoursEvent]: list of all upcoming office hours events for the given section
        """
        # Throws exception if user is not a member
        self._check_user_section_membership(subject.id, oh_section.id)

        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section.id}"
            )

        oh_events = entity.to_details_model().events

        return [
            oh_event
            for oh_event in oh_events
            if (
                oh_event.start_time >= time_range.start
                and oh_event.start_time < time_range.end
            )
        ]

    def get_current_events_by_section(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDetails,
    ) -> list[OfficeHoursEvent]:
        """Returns all events for a given office hours section

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to get all current events of
        Returns:
            list[OfficeHoursEvent]: list of all current office hours events for the given section
        """
        # Throws exception if user is not a member
        self._check_user_section_membership(subject.id, oh_section.id)

        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section.id}"
            )

        oh_events = entity.to_details_model().events

        # return all events that have started but haven't ended
        return [
            oh_event
            for oh_event in oh_events
            if (
                oh_event.start_time <= datetime.now()
                and oh_event.end_time > datetime.now()
            )
        ]

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
            .distinct()
        )
        entities = self._session.scalars(query).all()

        # Return the model
        return [entity.to_details_model() for entity in entities]

    def get_user_sections_by_term(
        self, subject: User, term_id: str
    ) -> list[OfficeHoursSectionDetails]:
        """Retrieves all office hours sections from the table by a term and specific user.
        Args:
            subject: a valid User model representing the currently logged in User
            term_id: ID of the term to query by.
        Returns:
            list[OfficeHoursSectionDetails]: List of all `OfficeHoursSectionDetails`
        """
        # TODO: Permission

        query = (
            select(OfficeHoursSectionEntity)
            .where(SectionMemberEntity.user_id == subject.id)
            .where(SectionEntity.id == SectionMemberEntity.section_id)
            .where(SectionEntity.term_id == term_id)
            .where(OfficeHoursSectionEntity.id == SectionEntity.office_hours_id)
            .distinct()
        )

        entities = self._session.scalars(query).all()
        return [entity.to_details_model() for entity in entities]

    def get_user_not_enrolled_sections(self, subject: User) -> list[OfficeHoursSection]:
        """Retrieves all office hours sections user not a member of.
        Args:
            subject (User): a valid User model representing the currently logged in User

        Returns:
            list[OfficeHoursSection]: List of all `OfficeHoursSection`

        """
        user_oh_sections_ids_query = (
            select(OfficeHoursSectionEntity.id)
            .where(SectionMemberEntity.user_id == subject.id)
            .where(SectionMemberEntity.section_id == SectionEntity.id)
            .where(OfficeHoursSectionEntity.id == SectionEntity.office_hours_id)
            .distinct()
        )

        query_user_not_enrolled_sections = select(OfficeHoursSectionEntity).filter(
            not_(OfficeHoursSectionEntity.id.in_(user_oh_sections_ids_query))
        )

        sections_not_in = self._session.scalars(query_user_not_enrolled_sections).all()

        return [entity.to_model() for entity in sections_not_in]

    def get_user_not_enrolled_sections_by_term(
        self, subject: User, term_id: str
    ) -> list[OfficeHoursSection]:
        """Retrieves all office hours sections user not a member of by term.
        Args:
            subject (User): a valid User model representing the currently logged in User
            term_id: ID of the term to query by.

        Returns:
            list[OfficeHoursSection]: List of all `OfficeHoursSection`

        """
        user_sections = self.get_user_sections_by_term(subject, term_id)
        user_section_ids = [row.id for row in user_sections]

        query = (
            select(OfficeHoursSectionEntity)
            .filter(OfficeHoursSectionEntity.id.not_in(user_section_ids))
            .join(SectionEntity)
            .filter(SectionEntity.term_id == term_id)
            .distinct()
        )

        user_not_enrolled_oh_sections = self._session.scalars(query).all()

        return [entity.to_model() for entity in user_not_enrolled_oh_sections]

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
        # PERMISSIONS

        # Checks If User Has Proper Role to Get and If is a Member in a Section
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a student. User Does Not Have Permision to get all tickets in section with id {oh_section.id}."
            )

        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section.id}"
            )

        # Get the tickets that are linked to the events which are linked to the section
        ticket_entities = [
            ticket for event in entity.events for ticket in event.tickets
        ]

        # Return the details model of those tickets
        return [entity.to_details_model() for entity in ticket_entities]

    def get_user_section_created_tickets(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all of the subject's created office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all of a user's created `OfficeHoursTicketDetails` in an OHsection
        """

        # PERMISSIONS

        # Throws exception if user is not a member
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        # Selects tickets from a certain section with the subject's id as one of the creators
        user_ticket_entities = (
            self._session.query(OfficeHoursTicketEntity)
            .join(OfficeHoursEventEntity)
            .join(OfficeHoursSectionEntity)
            .filter(
                OfficeHoursSectionEntity.id == oh_section.id,
                OfficeHoursTicketEntity.creators.any(
                    SectionMemberEntity.id == section_member_entity.id
                ),
            )
            .order_by(OfficeHoursTicketEntity.created_at.desc())
            .all()
        )

        return [entity.to_details_model() for entity in user_ticket_entities]

    def get_user_section_called_tickets(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all of the subject's called office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all of a user's called `OfficeHoursTicketDetails` in an OHsection
        """

        # PERMISSIONS

        # Throws exception if user is not a member
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        # Selects tickets from a certain section with the subject's id as the caller
        user_ticket_entities = (
            self._session.query(OfficeHoursTicketEntity)
            .join(OfficeHoursEventEntity)
            .join(OfficeHoursSectionEntity)
            .filter(
                OfficeHoursSectionEntity.id == oh_section.id,
                OfficeHoursTicketEntity.caller_id == section_member_entity.id,
            )
            .order_by(OfficeHoursTicketEntity.created_at.desc())
            .all()
        )

        return [entity.to_details_model() for entity in user_ticket_entities]

    def get_oh_section_members(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[SectionMember]:
        """Retrieves all of the subject's called office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[SectionMemberDetails]: List of all `SectionMemberDetails` in an OHsection
        """
        # PERMISSIONS

        # Throws exception if user is not a member
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        # Raises PermissionError if user trying to fetch all members is a Student
        if section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"Section Member is a Student. User Does Not Have Permission to Get Section Members."
            )

        # Select OH Section by id
        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section.id}"
            )

        # Get the members that are linked to the academic sections which are linked to the OH section
        member_entities = [
            member for section in entity.sections for member in section.members
        ]

        # Return the model version of those members
        return [entity.to_flat_model() for entity in member_entities]

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
            ResourceNotFoundException if user is not a member in given academic section.
            PermissionError if user creating event is not a Instructor
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

        return section_member_entity

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
