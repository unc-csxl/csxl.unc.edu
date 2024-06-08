"""
APIs for academics for users.
"""

from itertools import groupby
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User
from ...models.academics.my_courses import (
    MyCourseItem,
    CourseOverview,
    SectionOverview,
    TermOverview,
    MyCourseTerms,
)
from ...entities.academics.term_entity import TermEntity
from ...entities.academics.section_entity import SectionEntity
from ...entities.academics.section_member_entity import SectionMemberEntity

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

    def get_user_courses(self, user: User) -> MyCourseTerms:
        """
        Get the courses for the current user.

        Returns:
            MyCourseTerms
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
        return MyCourseTerms(terms=self._group_by_term(section_member_entities))

    def _group_by_term(
        self, entities: list[SectionMemberEntity]
    ) -> dict[str, TermOverview]:
        """
        Group a list of SectionMemberEntity by term.

        Args:
            entities (list[SectionMemberEntity]): The SectionMemberEntity to group.

        Returns:
            dict[str, TermOverview]: The grouped SectionMemberEntity.
        """
        terms = {}
        for term, sections in groupby(entities, lambda x: x.section.term):
            terms[term.name] = TermOverview(
                id=term.id,
                name=term.name,
                start=term.start,
                end=term.end,
                courses=self._,
            )
            term_sections = list(sections)
            term_overview = self._to_term_overview(term_sections[0].section.term)
            term_overview.courses = [
                self._to_my_course_item(section) for section in term_sections
            ]
            terms[term] = term_overview
        return terms

    def _to_my_course_item(self, entity: SectionMemberEntity) -> MyCourseItem:
        """
        Convert a SectionEntity to a MyCourseItem.

        Args:
            entity (SectionEntity): The SectionEntity to convert.

        Returns:
            MyCourseItem: The converted MyCourseItem.
        """
        return MyCourseItem(
            section=self._to_section_overview(entity.section),
            role=entity.member_role.name,
        )

    def _to_section_overview(self, entity: SectionEntity) -> SectionOverview:
        """
        Convert a SectionEntity to a SectionOverview.

        Args:
            entity (SectionEntity): The SectionEntity to convert.

        Returns:
            SectionOverview: The converted SectionOverview.
        """
        return SectionOverview(
            id=entity.id,
            course=CourseOverview(
                id=entity.course.id,
                subject_code=entity.course.subject_code,
                number=entity.course.number,
                title=entity.course.title,
                description=entity.course.description,
            ),
            number=entity.number,
            term=TermOverview(
                id=entity.term.id,
                name=entity.term.name,
                start=entity.term.start,
                end=entity.term.end,
            ),
            meeting_pattern=entity.meeting_pattern,
            override_title=entity.override_title,
            override_description=entity.override_description,
        )
