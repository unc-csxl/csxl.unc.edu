"""
APIs for academics for users.
"""

from itertools import groupby
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    CourseOverview,
    SectionOverview,
    CourseOverview,
    TermOverview,
    CourseMemberOverview,
    CourseRosterOverview,
)
from ...entities.academics.course_entity import CourseEntity
from ...entities.academics.section_entity import SectionEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import ResourceNotFoundException, CoursePermissionException

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
                        role=memberships[0].member_role.name,
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
        self, user: User, term_id: str, course_id: str
    ) -> CourseRosterOverview:
        """
        Get the courses for the current user.

        Returns:
            list[TermOverview]
        """

        course_entity = self._session.query(CourseEntity).get(course_id)

        if course_entity is None:
            raise ResourceNotFoundException(f"No course found for ID: {course_id}.")

        member_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .where(
                SectionEntity.term_id == term_id,
                SectionEntity.course_id == course_id,
            )
            .options(joinedload(SectionMemberEntity.user))
        )

        section_member_entities = self._session.scalars(member_query).all()

        user_member = [
            entity for entity in section_member_entities if entity.user_id == user.id
        ]

        if len(user_member) == 0 or user_member[0].member_role == RosterRole.STUDENT:
            raise CoursePermissionException(
                "Not allowed to access the roster of a course you are not an instructor of."
            )

        return self._to_course_roster_overview(course_entity, section_member_entities)

    def _to_course_member_overview(
        self, section_member: SectionMemberEntity
    ) -> CourseMemberOverview:
        return CourseMemberOverview(
            pid=section_member.user.pid,
            first_name=section_member.user.first_name,
            last_name=section_member.user.last_name,
            email=section_member.user.email,
            pronouns=section_member.user.pronouns,
            role=section_member.member_role.name,
            section_number=section_member.section.number,
        )

    def _to_course_roster_overview(
        self, course: CourseEntity, members: list[SectionMemberEntity]
    ):
        return CourseRosterOverview(
            id=course.id,
            subject_code=course.subject_code,
            number=course.number,
            title=course.title,
            members=[self._to_course_member_overview(member) for member in members],
        )
