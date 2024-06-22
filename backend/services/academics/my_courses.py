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
    TicketState,
)
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import OfficeHoursEntity, CourseSiteEntity
from ...entities.user_entity import UserEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException

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
            course_site_id=section.course_site_id,
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
            OfficeHoursEntity.start_time < datetime.today(),
            datetime.today() < OfficeHoursEntity.end_time,
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
        event_query = event_query.where(datetime.today() < OfficeHoursEntity.start_time)

        # Count the number of rows before applying pagination and filter
        count_query = select(func.count()).select_from(
            event_query.distinct(OfficeHoursEntity.id).subquery()
        )
        length = self._session.scalar(count_query)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        event_query = (
            event_query.offset(offset)
            .limit(limit)
            .order_by(OfficeHoursEntity.start_time)
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
        event_query = event_query.where(OfficeHoursEntity.end_time < datetime.today())

        # Count the number of rows before applying pagination and filter
        count_query = select(func.count()).select_from(
            event_query.distinct(OfficeHoursEntity.id).subquery()
        )
        length = self._session.scalar(count_query)

        # Calculate offset and limit for pagination
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        event_query = (
            event_query.offset(offset)
            .limit(limit)
            .order_by(OfficeHoursEntity.start_time)
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
            select(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .join(SectionEntity)
            .join(SectionMemberEntity)
            .where(
                SectionEntity.term_id == term_id,
                SectionEntity.course_id == course_id,
            )
            .options(joinedload(OfficeHoursEntity.room))
            .options(joinedload(OfficeHoursEntity.tickets))
            .options(
                joinedload(OfficeHoursEntity.course_site)
                .joinedload(CourseSiteEntity.sections)
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
        self, oh_event: OfficeHoursEntity
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
