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
from ....models.academics import SectionDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_svc, section_member_svc

# Import core data to ensure all data loads for the tests.
from ..core_data import setup_insert_data_fixture

# Import the fake model data in a namespace for test assertions
from . import term_data
from . import section_data
from .. import user_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_all(section_svc: SectionService):
    sections = section_svc.all()

    assert len(sections) == len(section_data.sections)
    assert isinstance(sections[0], SectionDetails)


def test_get_by_term(section_svc: SectionService):
    sections = section_svc.get_by_term(term_data.current_term.id)

    assert len(sections) == len(section_data.current_term_sections)
    assert isinstance(sections[0], SectionDetails)


def test_get_by_term_not_found(section_svc: SectionService):
    sections = section_svc.get_by_term(term_data.sp_23.id)

    assert len(sections) == 0


def test_get_by_subject(section_svc: SectionService):
    sections = section_svc.get_by_subject("COMP")

    assert len(sections) == len(section_data.sections)
    assert isinstance(sections[0], SectionDetails)


def test_get_by_subject_not_found(section_svc: SectionService):
    sections = section_svc.get_by_subject("INLS")

    assert len(sections) == 0


def test_get_by_id(section_svc: SectionService):
    if section_data.comp_110_001_current_term.id is None:
        raise ResourceNotFoundException("Invalid ID for section.")

    section = section_svc.get_by_id(section_data.comp_110_001_current_term.id)

    assert isinstance(section, SectionDetails)
    assert section.id == section_data.comp_110_001_current_term.id


def test_get_by_id_not_found(section_svc: SectionService):
    with pytest.raises(ResourceNotFoundException):
        section = section_svc.get_by_id(0)
        pytest.fail()  # Fail test if no error was thrown above


def test_get(section_svc: SectionService):
    section = section_svc.get("COMP", "210", "001")

    assert isinstance(section, SectionDetails)
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

    sections = section_svc.all()
    assert len(sections) == len(section_data.sections) - 1


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


def test_get_sections_with_no_office_hours_by_term(section_svc: SectionService):

    sections_with_no_oh = section_svc.get_sections_with_no_office_hours_by_term(
        term_data.current_term.id
    )

    assert len(sections_with_no_oh) > 0
    assert isinstance(sections_with_no_oh[0], SectionDetails)


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
