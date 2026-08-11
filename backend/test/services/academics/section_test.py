"""Tests for Courses Section Service."""

from unittest.mock import Mock, create_autospec
import pytest
from backend.models.roster_role import RosterRole
import backend.services.academics.section as section_service_module
from backend.services.academics.section import _parse_enrollment_data
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import SectionService, SectionMemberService
from ....models.academics import SectionDetails, CatalogSection

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_svc, section_member_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from .term_data import fake_data_fixture as insert_order_1
from .course_data import fake_data_fixture as insert_order_2
from .section_data import fake_data_fixture as insert_order_3

# Import the fake model data in a namespace for test assertions
from . import term_data
from . import section_data
from .. import user_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


UNC_TILED_RESULTS = b"""
<div class="card text-center">
    <div class="card-header">
        <h2 tabindex="0">COMP  110 001</h2>
        <p class="card-available-seats mb-0 text-a11y-green">
            12/250 available seats
        </p>
    </div>
    <div class="card-body p-2"><p>2026 Fall</p></div>
</div>
<div class="card text-center">
    <div class="card-header">
        <h2 tabindex="0">COMP   89 144</h2>
        <p class="card-available-seats mb-0 text-required-red">
            0/24 available seats
        </p>
    </div>
    <div class="card-body p-2"><p>2026 Fall</p></div>
</div>
"""


def test_get_by_term(section_svc: SectionService):
    sections = section_svc.get_by_term(term_data.current_term.id)

    assert len(sections) == len(section_data.current_term_sections)
    assert isinstance(sections[0], CatalogSection)


def test_get_by_term_not_found(section_svc: SectionService):
    sections = section_svc.get_by_term(term_data.future_term.id)

    assert len(sections) == 0


def test_get_by_id(section_svc: SectionService):
    if section_data.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    section = section_svc.get_by_id(section_data.comp_110_001_current_term.id)

    assert section.id == section_data.comp_110_001_current_term.id


def test_get_by_id_not_found(section_svc: SectionService):
    with pytest.raises(ResourceNotFoundException):
        section = section_svc.get_by_id(0)
        pytest.fail()  # Fail test if no error was thrown above


def test_get(section_svc: SectionService):
    section = section_svc.get("COMP", "210", "001")

    assert isinstance(section, CatalogSection)
    assert section.id == section_data.comp_210_001_current_term.id


def test_get_not_found(section_svc: SectionService):
    with pytest.raises(ResourceNotFoundException):
        section = section_svc.get("COMP", "888", "001")
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.create(user_data.root, section_data.new_section)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.section.create", "section/"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == section_data.new_section.id


def test_create_with_lecture_room(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.create(
        user_data.root, section_data.new_section_with_lecture_room
    )

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.section.create", "section/"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == section_data.new_section_with_lecture_room.id


def test_create_as_user(section_svc: SectionService):
    with pytest.raises(UserPermissionException):
        section = section_svc.create(user_data.user, section_data.new_section)
        pytest.fail()


def test_update_as_root(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.update(user_data.root, section_data.edited_comp_110)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.section.update", f"section/{section.id}"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == section_data.edited_comp_110.id


def test_update_with_lecture_room_with_previous_assignment(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.update(user_data.root, section_data.edited_comp_110_with_room)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.section.update", f"section/{section.id}"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == section_data.edited_comp_110_with_room.id


def test_update_with_lecture_room_without_previous_assignment(
    section_svc: SectionService,
):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section = section_svc.update(user_data.root, section_data.edited_comp_301_with_room)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.section.update", f"section/{section.id}"
    )
    assert isinstance(section, SectionDetails)
    assert section.id == section_data.edited_comp_301_with_room.id


def test_update_as_root_not_found(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        section = section_svc.update(user_data.root, section_data.new_section)
        pytest.fail()


def test_update_as_user(section_svc: SectionService):
    with pytest.raises(UserPermissionException):
        section = section_svc.create(user_data.user, section_data.edited_comp_110)
        pytest.fail()


def test_delete_as_root(section_svc: SectionService):
    if section_data.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section_svc.delete(user_data.root, section_data.comp_110_001_current_term.id)

    permission_svc.enforce.assert_called_with(
        user_data.root,
        "academics.section.delete",
        f"section/{section_data.comp_110_001_current_term.id}",
    )


def test_delete_as_root_not_found(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        if section_data.new_section.id is None:
            raise ResourceNotFoundException("Invalid ID for section.")

        section = section_svc.delete(user_data.root, section_data.new_section.id)
        pytest.fail()


def test_delete_as_user(section_svc: SectionService):
    if section_data.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    with pytest.raises(UserPermissionException):
        section = section_svc.delete(
            user_data.user, section_data.comp_110_001_current_term.id
        )
        pytest.fail()


def test_root_add_section_member(section_member_svc: SectionMemberService):
    membership = section_member_svc.add_section_member(
        subject=user_data.root,
        section_id=section_data.comp_101_001.id,
        user_id=user_data.root.id,
        member_role=RosterRole.INSTRUCTOR,
    )
    assert membership is not None


def test_user_add_section_member(section_member_svc: SectionMemberService):
    with pytest.raises(UserPermissionException):
        section_member_svc.add_section_member(
            subject=user_data.student,
            section_id=section_data.comp_101_001.id,
            user_id=user_data.root.id,
            member_role=RosterRole.INSTRUCTOR,
        )
        pytest.fail()


def test_parse_current_unc_enrollment_format():
    updates = _parse_enrollment_data(UNC_TILED_RESULTS, "2026 Fall")

    assert updates[("comp110", "001")].enrolled == 238
    assert updates[("comp110", "001")].total_seats == 250
    assert updates[("comp89", "144")].enrolled == 24


def test_update_enrollments(
    section_svc: SectionService, monkeypatch: pytest.MonkeyPatch
):
    response = Mock(content=UNC_TILED_RESULTS)
    get = Mock(return_value=response)
    monkeypatch.setattr(section_service_module.requests, "get", get)
    monkeypatch.setattr(
        section_service_module,
        "AVAILABLE_TERMS",
        {"2026 Fall": term_data.current_term.id},
    )

    section_svc.update_enrollment_totals(user_data.root)

    section = section_svc.get_by_id(section_data.comp_110_001_current_term.id)
    assert section.enrolled == 238
    assert section.total_seats == 250
    response.raise_for_status.assert_called_once_with()
