"""Application choices include instructors, including saved course preferences."""

from backend.entities.academics.course_entity import CourseEntity
from backend.entities.academics.section_entity import SectionEntity
from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.entities.user_entity import UserEntity
from backend.models.academics.section import CatalogSectionIdentity
from backend.models.roster_role import RosterRole


def test_section_choice_includes_only_instructor_last_names():
    section = SectionEntity(
        id=123,
        number="001",
        override_title="",
        course=CourseEntity(subject_code="COMP", number="110", title="Introduction"),
        members=[
            SectionMemberEntity(
                member_role=RosterRole.INSTRUCTOR, user=UserEntity(last_name="Zorlu")
            ),
            SectionMemberEntity(
                member_role=RosterRole.INSTRUCTOR, user=UserEntity(last_name="Lawson")
            ),
            SectionMemberEntity(
                member_role=RosterRole.STUDENT, user=UserEntity(last_name="Student")
            ),
        ],
    )
    choice = section.to_catalog_identity_model()
    assert choice.instructor_last_names == ["Lawson", "Zorlu"]
    assert choice.title == "Introduction"
    section.override_title = "Special Topic"
    section.members = []
    assert section.to_catalog_identity_model().instructor_last_names == []
    assert section.to_catalog_identity_model().title == "Special Topic"
    # Old clients can still submit section preferences without the display metadata.
    data = choice.model_dump(exclude={"instructor_last_names"})
    assert CatalogSectionIdentity(**data).instructor_last_names == []
