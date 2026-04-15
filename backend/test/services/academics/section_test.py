"""Tests for Courses Section Service."""

from types import SimpleNamespace
from unittest.mock import create_autospec
import pytest
import backend.services.academics.section as section_service_module
from sqlalchemy.orm import Session
from backend.models.roster_role import RosterRole
from backend.models.public_user import PublicUser
from backend.models.academics.section import EditedSection
from backend.services.exceptions import (
    CourseDataScrapingException,
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import SectionService, SectionMemberService
from ....models.academics import SectionDetails, CatalogSection

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_svc, section_member_svc
from .scenario import AcademicsScenario, arrange_academics_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def academics_scenario(session) -> AcademicsScenario:
    return arrange_academics_scenario(session)


def public_user_for(user) -> PublicUser:
    return PublicUser(
        id=user.id,
        onyen=user.onyen,
        first_name=user.first_name,
        last_name=user.last_name,
        pronouns=user.pronouns,
        email=user.email,
    )


def test_get_by_term(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    sections = section_svc.get_by_term(academics_scenario.current_term.id)

    assert len(sections) == len(academics_scenario.current_term_sections)
    assert isinstance(sections[0], CatalogSection)


def test_get_by_term_not_found(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    sections = section_svc.get_by_term(academics_scenario.future_term.id)

    assert len(sections) == 0


def test_get_by_id(section_svc: SectionService, academics_scenario: AcademicsScenario):
    if academics_scenario.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    section = section_svc.get_by_id(academics_scenario.comp_110_001_current_term.id)

    assert section.id == academics_scenario.comp_110_001_current_term.id


def test_get_by_id_not_found(section_svc: SectionService):
    with pytest.raises(ResourceNotFoundException):
        section = section_svc.get_by_id(0)
        pytest.fail()  # Fail test if no error was thrown above


def test_get(section_svc: SectionService, academics_scenario: AcademicsScenario):
    section = section_svc.get("COMP", "210", "001")

    assert isinstance(section, CatalogSection)
    assert section.id == academics_scenario.comp_210_001_current_term.id


def test_get_not_found(section_svc: SectionService):
    with pytest.raises(ResourceNotFoundException):
        section = section_svc.get("COMP", "888", "001")
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.create(
        academics_scenario.auth.root,
        academics_scenario.new_section.model_copy(deep=True),
    )

    permission_svc.enforce.assert_called_with(
        academics_scenario.auth.root, "academics.section.create", "section/"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == academics_scenario.new_section.id


def test_create_with_lecture_room(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.create(
        academics_scenario.auth.root,
        academics_scenario.new_section_with_lecture_room.model_copy(deep=True),
    )

    permission_svc.enforce.assert_called_with(
        academics_scenario.auth.root, "academics.section.create", "section/"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == academics_scenario.new_section_with_lecture_room.id


def test_create_with_instructors(
    section_svc: SectionService,
    section_member_svc: SectionMemberService,
    academics_scenario: AcademicsScenario,
):
    section_svc._section_member_svc = section_member_svc
    section = academics_scenario.new_section.model_copy(deep=True)
    section.instructors = [public_user_for(academics_scenario.auth.instructor)]

    created = section_svc.create(academics_scenario.auth.root, section)

    instructors = [
        member for member in created.members if member.member_role == RosterRole.INSTRUCTOR
    ]
    assert len(instructors) == 1
    assert instructors[0].user_id == academics_scenario.auth.instructor.id


def test_create_as_user(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    with pytest.raises(UserPermissionException):
        section = section_svc.create(
            academics_scenario.auth.user,
            academics_scenario.new_section.model_copy(deep=True),
        )
        pytest.fail()


def test_update_as_root(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.update(
        academics_scenario.auth.root,
        academics_scenario.edited_comp_110.model_copy(deep=True),
    )

    permission_svc.enforce.assert_called_with(
        academics_scenario.auth.root,
        "academics.section.update",
        f"section/{section.id}",
    )
    assert isinstance(section, SectionDetails)
    assert section.id == academics_scenario.edited_comp_110.id


def test_update_with_lecture_room_with_previous_assignment(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.update(
        academics_scenario.auth.root,
        academics_scenario.edited_comp_110_with_room.model_copy(deep=True),
    )

    permission_svc.enforce.assert_called_with(
        academics_scenario.auth.root,
        "academics.section.update",
        f"section/{section.id}",
    )
    assert isinstance(section, SectionDetails)
    assert section.id == academics_scenario.edited_comp_110_with_room.id


def test_update_with_lecture_room_without_previous_assignment(
    section_svc: SectionService,
    academics_scenario: AcademicsScenario,
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.update(
        academics_scenario.auth.root,
        academics_scenario.edited_comp_301_with_room.model_copy(deep=True),
    )

    permission_svc.enforce.assert_called_with(
        academics_scenario.auth.root,
        "academics.section.update",
        f"section/{section.id}",
    )
    assert isinstance(section, SectionDetails)
    assert section.id == academics_scenario.edited_comp_301_with_room.id


def test_update_replaces_instructors(
    section_svc: SectionService,
    section_member_svc: SectionMemberService,
    academics_scenario: AcademicsScenario,
):
    section_svc._section_member_svc = section_member_svc
    edited_section = academics_scenario.edited_comp_110.model_copy(deep=True)
    edited_section.instructors = [public_user_for(academics_scenario.auth.root)]

    updated = section_svc.update(academics_scenario.auth.root, edited_section)

    instructors = [
        member for member in updated.members if member.member_role == RosterRole.INSTRUCTOR
    ]
    assert [instructor.user_id for instructor in instructors] == [
        academics_scenario.auth.root.id
    ]


def test_update_replaces_existing_current_term_instructor(
    section_svc: SectionService,
    section_member_svc: SectionMemberService,
    academics_scenario: AcademicsScenario,
):
    section_svc._section_member_svc = section_member_svc
    edited_section = EditedSection(
        id=academics_scenario.comp_110_001_current_term.id,
        course_id=academics_scenario.comp_110_001_current_term.course_id,
        number=academics_scenario.comp_110_001_current_term.number,
        term_id=academics_scenario.comp_110_001_current_term.term_id,
        meeting_pattern=academics_scenario.comp_110_001_current_term.meeting_pattern,
        lecture_room=academics_scenario.comp_110_001_current_term.lecture_room,
        override_title=academics_scenario.comp_110_001_current_term.override_title,
        override_description=academics_scenario.comp_110_001_current_term.override_description,
        enrolled=academics_scenario.comp_110_001_current_term.enrolled,
        total_seats=academics_scenario.comp_110_001_current_term.total_seats,
        instructors=[public_user_for(academics_scenario.auth.root)],
    )

    updated = section_svc.update(academics_scenario.auth.root, edited_section)

    instructors = [
        member for member in updated.members if member.member_role == RosterRole.INSTRUCTOR
    ]
    assert [instructor.user_id for instructor in instructors] == [
        academics_scenario.auth.root.id
    ]


def test_update_as_root_not_found(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        section = section_svc.update(
            academics_scenario.auth.root,
            academics_scenario.new_section.model_copy(deep=True),
        )
        pytest.fail()


def test_update_as_user(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    with pytest.raises(UserPermissionException):
        section = section_svc.create(
            academics_scenario.auth.user,
            academics_scenario.edited_comp_110.model_copy(deep=True),
        )
        pytest.fail()


def test_delete_as_root(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    if academics_scenario.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section_svc.delete(
        academics_scenario.auth.root,
        academics_scenario.comp_110_001_current_term.id,
    )

    permission_svc.enforce.assert_called_with(
        academics_scenario.auth.root,
        "academics.section.delete",
        f"section/{academics_scenario.comp_110_001_current_term.id}",
    )


def test_delete_as_root_not_found(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        if academics_scenario.new_section.id is None:
            raise ResourceNotFoundException("Invalid ID for section.")

        section = section_svc.delete(
            academics_scenario.auth.root, academics_scenario.new_section.id
        )
        pytest.fail()


def test_delete_as_user(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    if academics_scenario.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    with pytest.raises(UserPermissionException):
        section = section_svc.delete(
            academics_scenario.auth.user,
            academics_scenario.comp_110_001_current_term.id,
        )
        pytest.fail()


def test_root_add_section_member(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    membership = section_member_svc.add_section_member(
        subject=academics_scenario.auth.root,
        section_id=academics_scenario.comp_101_001.id,
        user_id=academics_scenario.auth.root.id,
        member_role=RosterRole.INSTRUCTOR,
    )
    assert membership is not None


def test_user_add_section_member(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    with pytest.raises(UserPermissionException):
        section_member_svc.add_section_member(
            subject=academics_scenario.auth.student,
            section_id=academics_scenario.comp_101_001.id,
            user_id=academics_scenario.auth.root.id,
            member_role=RosterRole.INSTRUCTOR,
        )
        pytest.fail()


def test_update_enrollments(
    section_svc: SectionService, academics_scenario: AcademicsScenario
):
    section_svc.update_enrollment_totals(academics_scenario.auth.root)


def test_update_enrollments_raises_on_scrape_failure(
    monkeypatch,
    section_svc: SectionService,
    academics_scenario: AcademicsScenario,
):
    def explode(_url: str):
        raise RuntimeError("boom")

    monkeypatch.setattr(section_service_module.requests, "get", explode)

    with pytest.raises(CourseDataScrapingException):
        section_svc.update_enrollment_totals(academics_scenario.auth.root)
        pytest.fail()


def test_update_enrollments_updates_matching_sections(
    monkeypatch, academics_scenario: AcademicsScenario
):
    html = b"""
    <div class='card'>
      <h2>COMP - 110 001</h2>
      <p class='card-available-seats'>10/20 seats</p>
    </div>
    """
    section_entity = SimpleNamespace(course_id="comp110", number="001", enrolled=0, total_seats=0)
    session = create_autospec(Session)
    session.scalars.side_effect = [
        SimpleNamespace(all=lambda: [section_entity]),
        SimpleNamespace(all=lambda: []),
    ]
    service = SectionService(
        session,
        create_autospec(PermissionService),
        create_autospec(SectionMemberService),
    )

    monkeypatch.setattr(
        section_service_module.requests,
        "get",
        lambda _url: SimpleNamespace(content=html),
    )

    service.update_enrollment_totals(academics_scenario.auth.root)

    assert section_entity.enrolled == 10
    assert section_entity.total_seats == 20
