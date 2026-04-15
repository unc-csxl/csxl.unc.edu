"""Tests for Courses Section Service."""

from unittest.mock import create_autospec
import pytest
from backend.models.roster_role import RosterRole
from backend.services.exceptions import (
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


def test_get_by_term(section_svc: SectionService, academics_scenario: AcademicsScenario):
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
