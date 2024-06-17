"""
APIs for academics for users.
"""

from datetime import datetime
from itertools import groupby
from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User
from ...models.pagination import PaginationParams, Paginated
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    CourseOverview,
    SectionOverview,
    CourseOverview,
    TermOverview,
    CourseMemberOverview,
    CourseOfficeHourEventOverview,
    OfficeHourTicketOverview,
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)
from ...models.office_hours.ticket import TicketState, OfficeHoursTicket
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import (
    OfficeHoursSectionEntity,
    OfficeHoursEventEntity,
    OfficeHoursTicketEntity,
)
from ...entities.user_entity import UserEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class MyCoursesService:
    """
    Service that performs all of the actions on the `Section` table
    """

    def __init__(self, session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session

    def get_user_courses(self, user: User) -> list[TermOverview]:
        """
        Get the courses for the current user.

        Returns:
            list[TermOverview]
        """
        query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .options(
                joinedload(SectionMemberEntity.section).joinedload(
                    SectionEntity.course
                ),
                joinedload(SectionMemberEntity.section).joinedload(SectionEntity.term),
            )
        )
        section_member_entities = self._session.scalars(query).all()
        return self._group_by_term(section_member_entities)

    def _group_by_term(self, entities: list[SectionMemberEntity]) -> list[TermOverview]:
        """
        Group a list of SectionMemberEntity by term.

        Args:
            entities (list[SectionMemberEntity]): The SectionMemberEntity to group.

        Returns:
            list[TermOverview]: The grouped SectionMemberEntity.
        """
        terms = []
        for term, term_memberships in groupby(entities, lambda x: x.section.term):
            courses = []
            for course, course_memberships in groupby(
                term_memberships, lambda membership: membership.section.course
            ):
                memberships = list(course_memberships)
                courses.append(
                    CourseOverview(
                        id=course.id,
                        subject_code=course.subject_code,
                        number=course.number,
                        title=memberships[0].section.override_title or course.title,
                        role=memberships[0].member_role.value,
                        sections=[
                            self._to_section_overview(membership.section)
                            for membership in memberships
                        ],
                    )
                )

            terms.append(
                TermOverview(
                    id=term.id,
                    name=term.name,
                    start=term.start,
                    end=term.end,
                    courses=courses,
                )
            )
        return terms

    def _to_section_overview(self, section: SectionEntity) -> SectionOverview:
        return SectionOverview(
            number=section.number,
            meeting_pattern=section.meeting_pattern,
            oh_section_id=section.office_hours_id,
        )

    def get_course_roster(
        self,
        user: User,
        term_id: str,
        course_id: str,
        pagination_params: PaginationParams,
    ) -> Paginated[CourseMemberOverview]:
        """
        Get a paginated list of members for a course.

        Returns:
            Paginated[CourseMemberOverview]
        """

        # Start building the query
        member_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .join(UserEntity)
            .where(
                SectionEntity.term_id == term_id,
                SectionEntity.course_id == course_id,
            )
            .options(joinedload(SectionMemberEntity.section))
            .options(joinedload(SectionMemberEntity.user))
        )

        # Add order by sort from pagination parameters
        if pagination_params.order_by != "":
            member_query = member_query.order_by(
                getattr(SectionMemberEntity, pagination_params.order_by)
            )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = member_query.where(SectionMemberEntity.user_id == user.id)
        user_members = self._session.scalars(user_member_query).all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0:
            raise CoursePermissionException(
                "Not allowed to access the roster of a course you are not a member of."
            )

        # Determines if a user is a student
        # NOTE: This can be used to limit roster data a user can see compared to
        # an instructor in the future.
        is_student = user_members[0].member_role == RosterRole.STUDENT

        # In the cases where sections are taught by different instructors, ensure that
        # the roster data only includes sections that the user has permissions for.
        section_ids = [member.section_id for member in user_members]
        member_query = member_query.where(SectionEntity.id.in_(section_ids))

        # Count the number of rows before applying pagination and filter.
        count_query = select(func.count()).select_from(member_query.subquery())
        length = self._session.scalar(count_query)

        # Add filtering by inputted pagination parameters
        if pagination_params.filter != "":
            query = pagination_params.filter
            criteria = or_(
                UserEntity.first_name.ilike(f"%{query}%"),
                UserEntity.last_name.ilike(f"%{query}%"),
                UserEntity.onyen.ilike(f"%{query}%"),
            )
            member_query = member_query.where(criteria)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        member_query = (
            member_query.offset(offset)
            .limit(limit)
            .order_by(SectionEntity.id)
            .order_by(UserEntity.first_name)
            .order_by(SectionMemberEntity.member_role)
        )

        # Load the final query
        section_member_entities = self._session.scalars(member_query).all()

        # Create paginated representation of data and return
        return Paginated(
            items=[
                self._to_course_member_overview(member, is_student)
                for member in section_member_entities
            ],
            length=length,
            params=pagination_params,
        )

    def _to_course_member_overview(
        self, section_member: SectionMemberEntity, is_student: bool
    ) -> CourseMemberOverview:
        return CourseMemberOverview(
            pid=section_member.user.pid,
            first_name=section_member.user.first_name,
            last_name=section_member.user.last_name,
            email=section_member.user.email,
            pronouns=section_member.user.pronouns,
            role=section_member.member_role.value,
            section_number=section_member.section.number,
        )

    def get_current_office_hour_events(
        self, user: User, term_id: str, course_id: str
    ) -> list[CourseOfficeHourEventOverview]:
        """
        Get the overview for a course's currenet office hour events.

        Returns:
            list[CourseOfficeHourEventOverview]
        """

        # Start building the query
        event_query = self._create_oh_event_query(user, term_id, course_id)

        # Only load current events
        event_query = event_query.where(
            OfficeHoursEventEntity.start_time < datetime.today(),
            datetime.today() < OfficeHoursEventEntity.end_time,
        )

        # Load office hours data
        office_hour_event_entities = self._session.scalars(event_query).unique().all()

        return [
            self._to_oh_event_overview(event) for event in office_hour_event_entities
        ]

    def get_future_office_hour_events(
        self,
        user: User,
        term_id: str,
        course_id: str,
        pagination_params: PaginationParams,
    ) -> Paginated[CourseOfficeHourEventOverview]:
        """
        Gets the future office hours events, paginated.

        Returns:
            Paginated[CourseOfficeHourEventOverview]
        """

        # Start building the query
        event_query = self._create_oh_event_query(user, term_id, course_id)

        # Only load future events
        event_query = event_query.where(
            datetime.today() < OfficeHoursEventEntity.start_time
        )

        # Count the number of rows before applying pagination and filter
        count_query = select(func.count()).select_from(
            event_query.distinct(OfficeHoursEventEntity.id).subquery()
        )
        length = self._session.scalar(count_query)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        event_query = (
            event_query.offset(offset)
            .limit(limit)
            .order_by(OfficeHoursEventEntity.start_time)
        )

        # Load office hours data
        office_hour_event_entities = self._session.scalars(event_query).unique().all()

        # Create paginated representation of data and return
        return Paginated(
            items=[
                self._to_oh_event_overview(event)
                for event in office_hour_event_entities
            ],
            length=length,
            params=pagination_params,
        )

    def get_past_office_hour_events(
        self,
        user: User,
        term_id: str,
        course_id: str,
        pagination_params: PaginationParams,
    ) -> Paginated[CourseOfficeHourEventOverview]:
        """
        Gets the past office hours events, paginated.

        Returns:
            Paginated[CourseOfficeHourEventOverview]
        """

        # Start building the query
        event_query = self._create_oh_event_query(user, term_id, course_id)

        # Only load future events
        event_query = event_query.where(
            OfficeHoursEventEntity.end_time < datetime.today()
        )

        # Count the number of rows before applying pagination and filter
        count_query = select(func.count()).select_from(
            event_query.distinct(OfficeHoursEventEntity.id).subquery()
        )
        length = self._session.scalar(count_query)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        event_query = (
            event_query.offset(offset)
            .limit(limit)
            .order_by(OfficeHoursEventEntity.start_time)
        )

        # Load office hours data
        office_hour_event_entities = self._session.scalars(event_query).unique().all()

        # Create paginated representation of data and return
        return Paginated(
            items=[
                self._to_oh_event_overview(event)
                for event in office_hour_event_entities
            ],
            length=length,
            params=pagination_params,
        )

    def _create_oh_event_query(self, user: User, term_id: str, course_id: str):
        # Start building the query
        event_query = (
            select(OfficeHoursEventEntity)
            .join(OfficeHoursSectionEntity)
            .join(SectionEntity)
            .join(SectionMemberEntity)
            .where(
                SectionEntity.term_id == term_id,
                SectionEntity.course_id == course_id,
            )
            .options(joinedload(OfficeHoursEventEntity.room))
            .options(joinedload(OfficeHoursEventEntity.tickets))
            .options(
                joinedload(OfficeHoursEventEntity.office_hours_section)
                .joinedload(OfficeHoursSectionEntity.sections)
                .joinedload(SectionEntity.members)
            )
        )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .join(UserEntity)
            .where(
                SectionEntity.term_id == term_id,
                SectionEntity.course_id == course_id,
            )
            .where(SectionMemberEntity.user_id == user.id)
        )
        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0:
            raise CoursePermissionException(
                "Not allowed to access the roster of a course you are not a member of."
            )

        # In the cases where sections are taught by different instructors, ensure that
        # the roster data only includes sections that the user has permissions for.
        section_ids = [member.section_id for member in user_members]
        event_query = event_query.where(SectionEntity.id.in_(section_ids))

        return event_query

    def _to_oh_event_overview(
        self, oh_event: OfficeHoursEventEntity
    ) -> CourseOfficeHourEventOverview:
        return CourseOfficeHourEventOverview(
            id=oh_event.id,
            type=oh_event.type.value,
            mode=oh_event.mode.value,
            description=oh_event.description,
            location=f"{oh_event.room.building} {oh_event.room.room}",
            location_description=oh_event.location_description,
            start_time=oh_event.start_time,
            end_time=oh_event.end_time,
            queued=len(
                [
                    ticket
                    for ticket in oh_event.tickets
                    if ticket.state == TicketState.QUEUED
                ]
            ),
            total_tickets=len(oh_event.tickets),
        )

    def get_office_hour_queue(
        self, user: User, oh_event_id: int
    ) -> OfficeHourQueueOverview:
        """
        Loads all of the data relevant to an office hour queue.

        Returns:
            OfficeHourQueueOverview
        """
        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(OfficeHoursSectionEntity)
            .join(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == oh_event_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or user_members[0].member_role == RosterRole.STUDENT:
            raise CoursePermissionException(
                "Not allowed to access the queue of a course you are not a UTA, GTA, or instructor for."
            )

        # Start building the query
        queue_query = (
            select(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == oh_event_id)
            .options(
                joinedload(OfficeHoursEventEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.caller)
                .joinedload(SectionMemberEntity.user)
            )
            .options(
                joinedload(OfficeHoursEventEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.creators)
                .joinedload(SectionMemberEntity.user)
            )
        )

        # Load data
        queue_entity = self._session.scalars(queue_query).unique().one_or_none()

        if not queue_entity:
            raise ResourceNotFoundException(
                f"No office hours event for id: {oh_event_id}"
            )

        # Return data
        return self._to_oh_queue_overview(user, queue_entity)

    def get_office_hour_get_help_overview(
        self, user: User, oh_event_id: int
    ) -> OfficeHourGetHelpOverview:
        """
        Loads all of the data relevant for getting help in office hours.

        Returns:
            OfficeHourGetHelpOverview
        """
        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(OfficeHoursSectionEntity)
            .join(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == oh_event_id)
            .options(joinedload(SectionMemberEntity.created_oh_tickets))
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        # If the user is not a member of the looked up course, throw an error
        if not user_member or user_member.member_role != RosterRole.STUDENT:
            raise CoursePermissionException(
                "You cannot access office hours for a class you are not enrolled in."
            )

        # Locate tickets
        user_member.created_oh_tickets

        # Start building the query
        queue_query = (
            select(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == oh_event_id)
            .options(
                joinedload(OfficeHoursEventEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.caller)
                .joinedload(SectionMemberEntity.user)
            )
            .options(
                joinedload(OfficeHoursEventEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.creators)
                .joinedload(SectionMemberEntity.user)
            )
        )

        # Load data
        queue_entity = self._session.scalars(queue_query).unique().one_or_none()

        if not queue_entity:
            raise ResourceNotFoundException(
                f"No office hours event for id: {oh_event_id}"
            )

        # Get ticket for user, if any
        active_tickets = [
            ticket
            for ticket in queue_entity.tickets
            if user_member.id in [creator.id for creator in ticket.creators]
            and ticket.state in [TicketState.QUEUED, TicketState.CALLED]
        ]

        active_ticket = active_tickets[0] if len(active_tickets) > 0 else None

        # Find queue position
        queue_tickets = [
            ticket
            for ticket in queue_entity.tickets
            if ticket.state == TicketState.QUEUED
        ]

        queue_position = (
            queue_tickets.index(active_ticket) + 1
            if active_ticket and active_ticket.state == TicketState.QUEUED
            else -1
        )

        # Return data
        return OfficeHourGetHelpOverview(
            event_type=queue_entity.type.value,
            event_start_time=queue_entity.start_time,
            event_end_time=queue_entity.end_time,
            ticket=(
                self._to_oh_ticket_overview(active_ticket) if active_ticket else None
            ),
            queue_position=queue_position,
        )

    def _to_oh_ticket_overview(
        self, ticket: OfficeHoursTicketEntity
    ) -> OfficeHourTicketOverview:
        return OfficeHourTicketOverview(
            id=ticket.id,
            created_at=ticket.created_at,
            called_at=ticket.called_at,
            state=ticket.state.value,
            type=ticket.type.value,
            description=ticket.description,
            creators=[
                f"{creator.user.first_name} {creator.user.last_name}"
                for creator in ticket.creators
            ],
            caller=(
                f"{ticket.caller.user.first_name} {ticket.caller.user.last_name}"
                if ticket.caller
                else None
            ),
        )

    def _to_oh_queue_overview(
        self, user: User, oh_event: OfficeHoursEventEntity
    ) -> OfficeHourQueueOverview:
        active_tickets = [
            ticket
            for ticket in oh_event.tickets
            if ticket.state == TicketState.CALLED
            and ticket.caller
            and ticket.caller.user_id == user.id
        ]
        called_tickets = [
            ticket
            for ticket in oh_event.tickets
            if ticket.state == TicketState.CALLED
            and ticket.caller
            and ticket.caller.user_id != user.id
        ]
        queued_tickets = [
            ticket for ticket in oh_event.tickets if ticket.state == TicketState.QUEUED
        ]
        return OfficeHourQueueOverview(
            id=oh_event.id,
            type=oh_event.type.value,
            start_time=oh_event.start_time,
            end_time=oh_event.end_time,
            active=(
                self._to_oh_ticket_overview(active_tickets[0])
                if len(active_tickets) > 0
                else None
            ),
            other_called=[
                self._to_oh_ticket_overview(ticket) for ticket in called_tickets
            ],
            queue=[self._to_oh_ticket_overview(ticket) for ticket in queued_tickets],
        )

    def call_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Calls a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        if ticket_entity.state != TicketState.QUEUED:
            raise CoursePermissionException(
                "Cannot call a ticket that is not in the queue."
            )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(OfficeHoursSectionEntity)
            .join(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == ticket_entity.oh_event_id)
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        # If the user is not a member of the looked up course, throw an error
        if not user_member or user_member.member_role == RosterRole.STUDENT:
            raise CoursePermissionException(
                "Not allowed to call if a ticket if you are not a UTA, GTA, or instructor for."
            )

        # Call the ticket
        ticket_entity.caller_id = user_member.id
        ticket_entity.called_at = datetime.now()
        ticket_entity.state = TicketState.CALLED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return self._to_oh_ticket_overview(ticket_entity)

    def cancel_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Cancels a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(OfficeHoursSectionEntity)
            .join(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == ticket_entity.oh_event_id)
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        # If the user is not a member of the looked up course, throw an error
        if not user_member or (
            user_member.member_role == RosterRole.STUDENT
            and user_member.user_id
            not in [creator.id for creator in ticket_entity.creators]
        ):
            raise CoursePermissionException(
                "Not allowed to cancel if a ticket if you are not a UTA, GTA, or instructor for it, or you did not open it."
            )

        # Cancel the ticket
        ticket_entity.state = TicketState.CANCELED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return self._to_oh_ticket_overview(ticket_entity)

    def close_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Closes a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        if ticket_entity.state != TicketState.CALLED:
            raise CoursePermissionException(
                "Cannot close a ticket that has not been called."
            )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(OfficeHoursSectionEntity)
            .join(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == ticket_entity.oh_event_id)
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        # If the user is not a member of the looked up course, throw an error
        if not user_member or (user_member.member_role == RosterRole.STUDENT):
            raise CoursePermissionException(
                "Not allowed to call if a ticket if you are not a UTA, GTA, or instructor for."
            )

        # Close the ticket
        ticket_entity.closed_at = datetime.now()
        ticket_entity.state = TicketState.CLOSED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return self._to_oh_ticket_overview(ticket_entity)

    def get_oh_event_role(
        self, user: User, oh_event_id: int
    ) -> OfficeHourEventRoleOverview:
        """
        Returns the user's role for an event.

        Returns:
            OfficeHourEventRoleOverview
        """
        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(OfficeHoursSectionEntity)
            .join(OfficeHoursEventEntity)
            .where(OfficeHoursEventEntity.id == oh_event_id)
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        if not user_member:
            raise CoursePermissionException(
                "User is not a member of the office hour event."
            )

        return OfficeHourEventRoleOverview(role=user_member.member_role.value)
