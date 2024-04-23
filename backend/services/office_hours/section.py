from datetime import datetime, timedelta
import statistics
from fastapi import Depends
from sqlalchemy import and_, not_, select, select, outerjoin, and_, not_
from sqlalchemy import select, not_, and_, union
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session

from ...models.office_hours.ticket import OfficeHoursTicket
from ...models.office_hours.section_data import OfficeHoursSectionTrailingWeekData
from ...models.academics.section_member import SectionMember, SectionMemberPartial
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

        # Return details model version of added object
        return oh_section_entity.to_details_model()

    def get_all_sections(self, subject: User) -> list[OfficeHoursSectionDetails]:
        """Fetches All Office Hours Sections.

        Args:
            subject: a valid User model representing the currently logged in User

        Returns:
            list[OfficeHoursSectionDetails]: List of all Office Hours Sections
        """
        # Select all sections from the database
        query = select(OfficeHoursSectionEntity)
        entities = self._session.scalars(query).all()

        # Return the details models
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
        # Select OHSection by id
        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section_id
        )
        entity = self._session.scalars(query).one_or_none()

        # Raise ResourceNotFoundException if section with given id was not found
        if entity is None:
            raise ResourceNotFoundException(
                f"Unable to find section with id {oh_section_id}"
            )

        # Return details model
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

        oh_events = oh_section.events

        # Return OH Event models which ended in the past
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

        oh_events = oh_section.events

        # Return OH Event models which start within the given time_range
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

        oh_events = oh_section.events

        # Return OH Event models that have started and have not ended
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
        # Select all entries in the `OfficeHoursSection` table where their section(s)'s term id == term_id
        query = (
            select(OfficeHoursSectionEntity)
            .join(SectionEntity)
            .where(SectionEntity.term_id == term_id)
            .order_by(OfficeHoursSectionEntity.title)
            .distinct()
        )
        entities = self._session.scalars(query).all()

        # Return the details models
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

        # Select OH Section entities the user is a part of in the given term
        query = (
            select(OfficeHoursSectionEntity)
            .where(SectionMemberEntity.user_id == subject.id)
            .where(SectionEntity.id == SectionMemberEntity.section_id)
            .where(SectionEntity.term_id == term_id)
            .where(OfficeHoursSectionEntity.id == SectionEntity.office_hours_id)
            .distinct()
        )

        entities = self._session.scalars(query).all()

        # Return details models
        return [entity.to_details_model() for entity in entities]

    def get_user_not_enrolled_sections(self, subject: User) -> list[OfficeHoursSection]:
        """Retrieves all office hours sections the user is not a member of.
        Args:
            subject (User): a valid User model representing the currently logged in User

        Returns:
            list[OfficeHoursSection]: List of all `OfficeHoursSection` the user is not enrolled in.

        """
        # TODO: add more comments here
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

        # Return details models
        return [entity.to_model() for entity in sections_not_in]

    def get_user_not_enrolled_sections_by_term(
        self, subject: User, term_id: str
    ) -> list[OfficeHoursSection]:
        """Retrieves all office hours sections user not a member of by term.
        Args:
            subject (User): a valid User model representing the currently logged in User
            term_id: ID of the term to query by.

        Returns:
            list[OfficeHoursSection]: List of all `OfficeHoursSection` the user is not enrolled in in the given term.

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

        # Return details models
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

        # Get the tickets that are linked to the events which are linked to the section
        ticket_entities = [
            ticket for event in entity.events for ticket in event.tickets
        ]

        # Return the details model of those tickets
        return [entity.to_details_model() for entity in ticket_entities]

    def get_user_section_created_tickets(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[OfficeHoursTicket]:
        """Retrieves all of the subject's created office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicket]: List of all of a user's created `OfficeHoursTicket` in an OHsection
        """

        # PERMISSIONS

        # Raises exception if user is not a member
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        # Take Created Ticket Relationship From SectionMemberEntity
        created_tickets = [
            entity.to_model() for entity in section_member_entity.created_tickets
        ]

        # Order so lastest is first
        created_tickets.sort(key=lambda x: x.created_at, reverse=True)
        return created_tickets

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

        # Raises exception if user is not a member
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        # Selects tickets from a certain section with the subject's id as the caller
        called_tickets = [
            entity.to_details_model()
            for entity in section_member_entity.called_tickets
            if entity.called_at is not None
        ]

        # Order with Lastest First, return
        called_tickets.sort(key=lambda x: x.called_at, reverse=True)

        return called_tickets

    def get_section_tickets_with_concerns(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets that were flagged for concern from the table by a section.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all concerning `OfficeHoursTicketDetails` in an OHsection
        """

        # Checks If User Has Proper Role to Get and If is a Member in a Section
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        if (
            section_member_entity.member_role != RosterRole.INSTRUCTOR
            and section_member_entity.member_role != RosterRole.GTA
        ):
            raise PermissionError(
                f"Section Member is not an Instructor or GTA. User Does Not Have Permision to get concerning tickets in section with id {oh_section.id}."
            )

        # Selects the section entity based on the ID
        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        # Get the tickets that are linked to the events which are linked to the section
        ticket_entities = [
            ticket for event in entity.events for ticket in event.tickets
        ]

        # Access the details models of those tickets
        ticket_details_models = [
            entity.to_details_model() for entity in ticket_entities
        ]

        # Order the tickets so the most recent one is on top
        ticket_details_models.sort(key=lambda x: x.created_at, reverse=True)

        # Return ticket details models where have_concerns is True
        return [ticket for ticket in ticket_details_models if ticket.have_concerns]

    def get_section_trailing_week_data(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> OfficeHoursSectionTrailingWeekData:
        """Retrieves all trailing week statistics in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            OfficeHoursSectionTrailingWeekData: Model of all trailing week statistics for the given OH section
        """

        # PERMISSIONS

        # Throws exception if user is not a member of the given section
        section_member_entity = self._check_user_section_membership(
            subject.id, oh_section.id
        )

        # Raises PermissionError if user trying to fetch data is not an Instructor or GTA
        if (
            section_member_entity.member_role != RosterRole.INSTRUCTOR
            and section_member_entity.member_role != RosterRole.GTA
        ):
            raise PermissionError(
                f"Section Member is not an Instructor or GTA. User Does Not Have Permission to Get data in section with id {oh_section.id}."
            )

        # Select OH Section by id
        query = select(OfficeHoursSectionEntity).where(
            OfficeHoursSectionEntity.id == oh_section.id
        )

        entity = self._session.scalars(query).one_or_none()

        # Get the tickets from the past week that are linked to the events which are linked to the section
        filtered_ticket_entities = [
            ticket
            for event in entity.events
            for ticket in event.tickets
            if ticket.created_at > datetime.now() - timedelta(days=7)
        ]

        # Get unique creators
        unique_ticket_creators = {
            creator
            for ticket in filtered_ticket_entities
            for creator in ticket.creators
        }

        # --- Get wait time statistics ---
        # Calculate wait times in minutes for each ticket with a called time filled in
        wait_times = [
            (ticket.called_at - ticket.created_at).total_seconds() / 60
            for ticket in filtered_ticket_entities
            if ticket.called_at
        ]

        # Compute the average
        avg_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0.0

        # Compute the standard deviation of wait times; handle if built in stdev raises Error
        try:
            std_dev_wait_time = statistics.stdev(wait_times)
        except statistics.StatisticsError:
            std_dev_wait_time = 0.0

        # --- Get ticket duration statistics ---
        # Calculate ticket duration in minutes for each ticket with a called time filled in
        ticket_duration_times = [
            (ticket.closed_at - ticket.called_at).total_seconds() / 60
            for ticket in filtered_ticket_entities
            if (ticket.closed_at and ticket.called_at)
        ]

        # Compute the average
        avg_duration_time = (
            sum(ticket_duration_times) / len(ticket_duration_times)
            if ticket_duration_times
            else 0.0
        )

        # Compute the standard deviation of duration times; handle if built in stdev raises Error
        try:
            std_dev_duration_time = statistics.stdev(ticket_duration_times)
        except statistics.StatisticsError:
            std_dev_duration_time = 0.0

        # --- Round floats to two decimal places, construct the model and return it ---
        return OfficeHoursSectionTrailingWeekData(
            number_of_tickets=len(filtered_ticket_entities),
            number_of_students=len(unique_ticket_creators),
            average_wait_time=round(avg_wait_time, 2),
            standard_deviation_wait_time=round(std_dev_wait_time, 2),
            average_ticket_duration=round(avg_duration_time, 2),
            standard_deviation_ticket_duration=round(std_dev_duration_time, 2),
        )

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

        # Get the members that are linked to the academic sections which are linked to the OH section
        member_entities = [
            member for section in entity.sections for member in section.members
        ]

        # Return the model version of those members
        return [entity.to_flat_model() for entity in member_entities]

    def update_oh_section_member_role(
        self, subject: User, user_to_modify: SectionMemberPartial, oh_section_id: int
    ) -> SectionMember:
        """
        Allows a GTA or Instructor to update a section member's Roster Role.

        Args:
            subject (User): The user object representing the user attempting to change a role.
            user_to_modify (SectionMemberPartial): The SectionMemberPartial whose role is being changed.
            oh_section_id: The id of the OH section where the SectionMember role is being changed.

        Returns:
            SectionMember: The updated SectionMember object
        """

        # PERMISSIONS:
        subject_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_id
        )

        # Ensure only instructors and GTAs can change roles
        if (
            subject_section_member_entity.member_role == RosterRole.STUDENT
            or subject_section_member_entity.member_role == RosterRole.UTA
        ):
            raise PermissionError(
                f"Section Member is not an Instructor or GTA. User Does Not Have Permision to change member roles in OH section {oh_section_id}."
            )

        # Do not allow changing roles to instructor so that students cannot create courses
        if user_to_modify.member_role == RosterRole.INSTRUCTOR:
            raise PermissionError(
                f"Section Members cannot be elevated to the Instructor role."
            )

        # Select SectionMember to modify
        query = select(SectionMemberEntity).where(
            SectionMemberEntity.id == user_to_modify.id
        )
        section_member_entity = self._session.scalars(query).one_or_none()
        if section_member_entity is None:
            raise ResourceNotFoundException(
                f"SectionMember with id {user_to_modify.id} not found."
            )

        # Ensure that instructors are not demoted
        if (
            section_member_entity.member_role == RosterRole.INSTRUCTOR
            and user_to_modify.member_role != RosterRole.INSTRUCTOR
        ):
            raise PermissionError(f"Instructors' roles cannot be modified.")

        # Raise error if member to update isn't a member of the OH section
        self._check_user_section_membership(
            section_member_entity.user_id, oh_section_id
        )

        # Change role and return model
        section_member_entity.member_role = user_to_modify.member_role
        self._session.commit()
        return section_member_entity.to_flat_model()

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
        # Select SectionMembers where the user id and section id match the given ones
        query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user_id)
            .where(SectionMemberEntity.section_id.in_(section_ids))
        )
        # Find User Academic Section Entity
        section_member_entity = self._session.scalars(query).one_or_none()

        if section_member_entity is None:
            raise PermissionError(
                f"User has to be a Section Member to Create OH Section. Unable To Find Section Member Entity for User with id: {user_id} in the following Academic Sections of ids: {section_ids}"
            )

        # Return entity
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
            raise PermissionError(
                f"Unable To Find Section Member Entity for user with id:{user_id} in academic section with id:{academic_section_ids}"
            )

        # Return the entity
        return section_member_entity
