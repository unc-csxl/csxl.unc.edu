"""
APIs for working with course sites.
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
    CourseSiteOverview,
    SectionOverview,
    TermOverview,
    CourseMemberOverview,
    OfficeHoursOverview,
    TicketState,
    TeachingSectionOverview,
)
from ...models.office_hours.course_site import (
    CourseSite,
    NewCourseSite,
    UpdatedCourseSite,
)
from ...models.office_hours.course_site_details import CourseSiteDetails
from ...models.academics.section_member import SectionMemberDraft
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import OfficeHoursEntity, CourseSiteEntity
from ...entities.user_entity import UserEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException

__authors__ = ["Ajay Gandecha", "Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class CourseSiteService:
    """
    Service that performs all of the actions on the `Section` table
    """

    def __init__(self, session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session

    def get_user_course_sites(self, user: User) -> list[TermOverview]:
        """
        Get the course sites for the current user.

        Returns:
            list[TermOverview]
        """
        query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .options(
                joinedload(SectionMemberEntity.section).joinedload(
                    SectionEntity.course_site
                ),
                joinedload(SectionMemberEntity.section).joinedload(SectionEntity.term),
                joinedload(SectionMemberEntity.section).joinedload(
                    SectionEntity.course
                ),
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
        entities.sort(key=lambda x: x.section.term.start)
        for term, term_memberships in groupby(entities, lambda x: x.section.term):

            # Since the output `term_memberships` is an iterator, we cannot iterate over the list
            # more than once, which we need to do below. So, this copies the original iterator
            # into a standard list so that we can iterate over it twice.
            memberships = list(term_memberships)

            course_sites = []
            teaching_no_site = [
                self._to_teaching_section_overview(membership.section)
                for membership in memberships
                if membership.member_role == RosterRole.INSTRUCTOR
                and membership.section.course_site_id == None
            ]

            for (course_site, course), course_memberships in groupby(
                memberships,
                lambda membership: (
                    membership.section.course_site,
                    membership.section.course,
                ),
            ):
                if course_site:
                    memberships = list(course_memberships)
                    course_sites.append(
                        CourseSiteOverview(
                            id=course_site.id,
                            term_id=course_site.term_id,
                            subject_code=course.subject_code,
                            number=course.number,
                            title=memberships[0].section.override_title or course.title,
                            role=memberships[0].member_role.value,
                            sections=[
                                self._to_section_overview(membership.section)
                                for membership in memberships
                            ],
                            gtas=[],
                            utas=[],
                        )
                    )

            terms.append(
                TermOverview(
                    id=term.id,
                    name=term.name,
                    start=term.start,
                    end=term.end,
                    sites=course_sites,
                    teaching_no_site=teaching_no_site,
                )
            )
        return terms

    def _to_section_overview(self, section: SectionEntity) -> SectionOverview:
        return SectionOverview(
            id=section.id,
            number=section.number,
            meeting_pattern=section.meeting_pattern,
            course_site_id=section.course_site_id,
            subject_code=section.course.subject_code,
            course_number=section.course.number,
            section_number=section.number,
        )

    def _to_teaching_section_overview(
        self, section: SectionEntity
    ) -> TeachingSectionOverview:
        return TeachingSectionOverview(
            id=section.id,
            subject_code=section.course.subject_code,
            course_number=section.course.number,
            section_number=section.number,
            title=section.override_description or section.course.title,
        )

    def get_course_site_roster(
        self,
        user: User,
        site_id: int,
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
            .where(SectionEntity.course_site_id == site_id)
            .options(joinedload(SectionMemberEntity.section))
            .options(joinedload(SectionMemberEntity.user))
        )

        # Add order by sort from pagination parameters
        if pagination_params.order_by != "":
            member_query = member_query.order_by(
                getattr(UserEntity, pagination_params.order_by)
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

        # Add filtering by inputted pagination parameters
        if pagination_params.filter != "":
            query = pagination_params.filter
            criteria = or_(
                UserEntity.first_name.ilike(f"%{query}%"),
                UserEntity.last_name.ilike(f"%{query}%"),
                UserEntity.onyen.ilike(f"%{query}%"),
            )
            member_query = member_query.where(criteria)

        # Count the number of rows before applying pagination and filter.
        count_query = select(func.count()).select_from(member_query.subquery())
        length = self._session.scalar(count_query)

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
        self, user: User, site_id: int
    ) -> list[OfficeHoursOverview]:
        """
        Get the overview for a course's currenet office hour events.

        Returns:
            list[OfficeHoursOverview]
        """

        # Start building the query
        event_query = self._create_oh_event_query(user, site_id)

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
        site_id: int,
        pagination_params: PaginationParams,
    ) -> Paginated[OfficeHoursOverview]:
        """
        Gets the future office hours events, paginated.

        Returns:
            Paginated[OfficeHoursOverview]
        """

        # Start building the query
        event_query = self._create_oh_event_query(user, site_id)

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
        site_id: int,
        pagination_params: PaginationParams,
    ) -> Paginated[OfficeHoursOverview]:
        """
        Gets the past office hours events, paginated.

        Returns:
            Paginated[OfficeHoursOverview]
        """

        # Start building the query
        event_query = self._create_oh_event_query(user, site_id)

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

    def _create_oh_event_query(self, user: User, site_id: int):
        # Start building the query
        event_query = (
            select(OfficeHoursEntity).where(OfficeHoursEntity.course_site_id == site_id)
            # .options(joinedload(OfficeHoursEntity.room))
            # .options(joinedload(OfficeHoursEntity.tickets))
            # .options(
            #     joinedload(OfficeHoursEntity.course_site)
            #     .joinedload(CourseSiteEntity.sections)
            #     .joinedload(SectionEntity.members)
            # )
        )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(
                SectionMemberEntity.section_id.in_(
                    select(SectionEntity.id).where(
                        SectionEntity.course_site_id == site_id
                    )
                )
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
        # TODO: Evaluate whether we think this is ever a concern? It seems more likely
        # that two different instructors will have two different course sites. Removing
        # for now, but there was some code here in first implementation.

        return event_query

    def _to_oh_event_overview(self, oh_event: OfficeHoursEntity) -> OfficeHoursOverview:
        return OfficeHoursOverview(
            id=oh_event.id,
            type=oh_event.type.to_string(),
            mode=oh_event.mode.to_string(),
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
            recurrence_pattern_id=oh_event.recurrence_pattern_id,
        )

    def create(self, user: User, new_site: NewCourseSite) -> CourseSite:
        """
        Creates a course site for an instructor with sections.
        """

        # Find all the user's section memberships for the term and sections inputted
        membership_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .where(SectionMemberEntity.section_id.in_(new_site.section_ids))
            .where(SectionEntity.term_id == new_site.term_id)
            .options(joinedload(SectionMemberEntity.section))
        )

        membership_entities = self._session.scalars(membership_query).all()
        section_entities = [membership.section for membership in membership_entities]

        # This check fails the creation of a course site if the sections inputted are either not in the term, or if
        # a user is not a member of the course.
        if len(membership_entities) != len(new_site.section_ids):
            raise CoursePermissionException(
                "You cannot add sections to a course site that you are not an instructor for, or sections in different terms."
            )

        # This check ensures that the user is an instructor for every section inputted.
        for membership in membership_entities:
            if membership.member_role != RosterRole.INSTRUCTOR:
                raise CoursePermissionException(
                    "You cannot add sections to a course site that you are not an instructor for."
                )

        # Ensure that sections provided are not already in a course site.
        for section in section_entities:
            if section.course_site_id != None:
                raise CoursePermissionException(
                    f"Section with ID: { section.id} is already in another course site."
                )

        # Create the course site, add, and save so the id field populates.
        course_site_entity = CourseSiteEntity.from_new_model(new_site)
        self._session.add(course_site_entity)
        self._session.commit()

        # Update the sections to add to the course site.
        for section_entity in section_entities:
            section_entity.course_site_id = course_site_entity.id

        # Save changes
        self._session.commit()

        # Return the model
        return course_site_entity.to_model()

    def update(self, user: User, updated_site: UpdatedCourseSite) -> CourseSite:
        """
        Update a course site.
        """
        # Get the site entity
        course_site_query = (
            select(CourseSiteEntity)
            .join(SectionEntity)
            .join(SectionMemberEntity)
            .where(CourseSiteEntity.id == updated_site.id)
            .options(
                joinedload(CourseSiteEntity.sections),
                joinedload(CourseSiteEntity.sections).joinedload(SectionEntity.members),
            )
        )
        course_site_entity = (
            self._session.scalars(course_site_query).unique().one_or_none()
        )

        # Complete error handling
        if course_site_entity is None:
            raise ResourceNotFoundException(
                f"Course site with ID: {updated_site.id} not found."
            )

        # Compelete error handling for existing sections
        old_section_entities = [section for section in course_site_entity.sections]
        for section in old_section_entities:
            members = [
                member
                for member in section.members
                if member.user_id == user.id
                and member.member_role == RosterRole.INSTRUCTOR
            ]
            if len(members) == 0:
                raise CoursePermissionException(
                    "Cannot modify a course page containing a section you are not an instructor for."
                )

        # Find all the user's section memberships for the term and sections inputted
        membership_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .where(SectionMemberEntity.section_id.in_(updated_site.section_ids))
            .where(SectionEntity.term_id == updated_site.term_id)
            .options(joinedload(SectionMemberEntity.section))
        )

        membership_entities = self._session.scalars(membership_query).all()
        new_section_entities = [
            membership.section for membership in membership_entities
        ]

        # This check fails the creation of a course site if the sections inputted are either not in the term, or if
        # a user is not a member of the course.
        if len(membership_entities) != len(updated_site.section_ids):
            raise CoursePermissionException(
                "You cannot add sections to a course site that you are not an instructor for, or sections in different terms."
            )

        # This check ensures that the user is an instructor for every section inputted.
        for membership in membership_entities:
            if membership.member_role != RosterRole.INSTRUCTOR:
                raise CoursePermissionException(
                    "You cannot add sections to a course site that you are not an instructor for."
                )

        # Complete the updates
        course_site_entity.title = updated_site.title
        course_site_entity.max_tickets_per_day = updated_site.max_tickets_per_day if updated_site.max_tickets_per_day else 100
        course_site_entity.minimum_ticket_cooldown = updated_site.minimum_ticket_cooldown if updated_site.minimum_ticket_cooldown else 0

        # Edit the selected sections
        for section in old_section_entities:
            section.course_site_id = None

        for section in new_section_entities:
            if section.course_site_id:
                raise CoursePermissionException(
                    f"Section with ID: { section.id} is already in another course site."
                )

            section.course_site_id = updated_site.id

        # Edit the staff - GTAs
        # 1. Remove all GTAs, then add new ones.
        gta_query = (
            select(SectionMemberEntity)
            .where(
                SectionMemberEntity.section_id.in_(
                    [section.id for section in course_site_entity.sections]
                ),
                SectionMemberEntity.user_id.not_in(
                    [gta.id for gta in updated_site.gtas]
                ),
            )
            .where(SectionMemberEntity.member_role == RosterRole.GTA)
        )
        gta_entities = self._session.scalars(gta_query).all()
        for gta_entity in gta_entities:
            self._session.delete(gta_entity)

        # 2. Add new ones
        for gta in updated_site.gtas:
            for section in course_site_entity.sections:
                existing_query = select(SectionMemberEntity).where(
                    SectionMemberEntity.section_id == section.id,
                    SectionMemberEntity.user_id == gta.id,
                )
                existing_entity = self._session.scalars(existing_query).one_or_none()
                if existing_entity is None:
                    draft = SectionMemberDraft(
                        user_id=gta.id,
                        section_id=section.id,
                        member_role=RosterRole.GTA,
                    )
                    section_member_entity = SectionMemberEntity.from_draft_model(draft)
                    self._session.add(section_member_entity)
                else:
                    if existing_entity.member_role != RosterRole.INSTRUCTOR:
                        existing_entity.member_role == RosterRole.GTA

        # Edit the staff - UTAs
        # 1. Remove all UTAs, then add new ones.
        uta_query = (
            select(SectionMemberEntity)
            .where(
                SectionMemberEntity.section_id.in_(
                    [section.id for section in course_site_entity.sections]
                ),
                SectionMemberEntity.user_id.not_in(
                    [uta.id for uta in updated_site.utas]
                ),
            )
            .where(SectionMemberEntity.member_role == RosterRole.UTA)
        )
        uta_entities = self._session.scalars(uta_query).all()
        for uta_entity in uta_entities:
            self._session.delete(uta_entity)

        # 2. Add new ones
        for uta in updated_site.utas:
            for section in course_site_entity.sections:
                existing_query = select(SectionMemberEntity).where(
                    SectionMemberEntity.section_id == section.id,
                    SectionMemberEntity.user_id == uta.id,
                )
                existing_entity = self._session.scalars(existing_query).one_or_none()
                if existing_entity is None:
                    draft = SectionMemberDraft(
                        user_id=uta.id,
                        section_id=section.id,
                        member_role=RosterRole.UTA,
                    )
                    section_member_entity = SectionMemberEntity.from_draft_model(draft)
                    self._session.add(section_member_entity)
                else:
                    if existing_entity.member_role != RosterRole.INSTRUCTOR:
                        existing_entity.member_role == RosterRole.UTA

        # Save all changes in one commit
        self._session.commit()

        # Return updated site
        return course_site_entity.to_model()

    def get(self, user: User, site_id: int) -> UpdatedCourseSite:
        """
        Returns a course site overview.
        """
        # Get the site entity
        course_site_query = select(CourseSiteEntity).where(
            CourseSiteEntity.id == site_id
        )

        course_site_entity = (
            self._session.scalars(course_site_query).unique().one_or_none()
        )

        # Complete error handling
        if course_site_entity is None:
            raise CoursePermissionException(f"Cannot access course with ID: {site_id}")

        # Find all the user's section memberships for the term and sections inputted
        membership_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .where(
                SectionMemberEntity.section_id.in_(
                    [section.id for section in course_site_entity.sections]
                )
            )
            .where(SectionEntity.term_id == course_site_entity.term_id)
            .options(joinedload(SectionMemberEntity.section))
        )

        membership_entities = self._session.scalars(membership_query).all()

        # This check ensures that the user is an instructor for every section inputted.
        for membership in membership_entities:
            if membership.member_role != RosterRole.INSTRUCTOR:
                raise CoursePermissionException(
                    "You cannot add sections to a course site that you are not an instructor for."
                )

        # Get GTAs and UTAs
        staff_query = (
            select(SectionMemberEntity)
            .where(
                SectionMemberEntity.section_id.in_(
                    [section.id for section in course_site_entity.sections]
                )
            )
            .where(
                SectionMemberEntity.member_role.in_([RosterRole.GTA, RosterRole.UTA])
            )
        )
        staff_entities = self._session.scalars(staff_query).all()

        # Return overview
        return UpdatedCourseSite(
            id=course_site_entity.id,
            title=course_site_entity.title,
            term_id=course_site_entity.term_id,
            section_ids=[section.id for section in course_site_entity.sections],
            gtas=list(
                set(
                    [
                        staff.user.to_public_model()
                        for staff in staff_entities
                        if staff.member_role == RosterRole.GTA
                    ]
                )
            ),
            utas=list(
                set(
                    [
                        staff.user.to_public_model()
                        for staff in staff_entities
                        if staff.member_role == RosterRole.UTA
                    ]
                )
            ),
            minimum_ticket_cooldown=course_site_entity.minimum_ticket_cooldown,
            max_tickets_per_day=course_site_entity.max_tickets_per_day,
        )
