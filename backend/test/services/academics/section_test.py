"""Tests for Courses Section Service."""

from unittest.mock import create_autospec
import pytest
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import SectionService
from ....models.academics import SectionDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .section_data import fake_data_fixture as insert_section_fake_data

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
    sections = section_svc.get_by_term(term_data.f_23.id)

    assert len(sections) == len(section_data.sections)
    assert isinstance(sections[0], SectionDetails)


def test_get_by_term_not_found(section_svc: SectionService):
    sections = section_svc.get_by_term(term_data.sp_24.id)

    assert len(sections) == 0


def test_get_by_subject(section_svc: SectionService):
    sections = section_svc.get_by_subject("COMP")

    assert len(sections) == len(section_data.sections)
    assert isinstance(sections[0], SectionDetails)


def test_get_by_subject_not_found(section_svc: SectionService):
    sections = section_svc.get_by_subject("INLS")

    assert len(sections) == 0


def test_get_by_id(section_svc: SectionService):
    section = section_svc.get_by_id(section_data.comp_101_001.id)

    assert isinstance(section, SectionDetails)
    assert section.id == section_data.comp_101_001.id


def test_get_by_id_not_found(section_svc: SectionService):
    with pytest.raises(ResourceNotFoundException):
        section = section_svc.get_by_id(0)
        pytest.fail()  # Fail test if no error was thrown above


def test_get(section_svc: SectionService):
    section = section_svc.get("COMP", "110", "001")

    assert isinstance(section, SectionDetails)
    assert section.id == section_data.comp_101_001.id


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
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    section_svc.delete(user_data.root, section_data.comp_101_001)

    permission_svc.enforce.assert_called_with(
        user_data.root,
        "academics.section.delete",
        f"section/{section_data.comp_101_001.id}",
    )

    sections = section_svc.all()
    assert len(sections) == len(section_data.sections) - 1


def test_delete_as_root_not_found(section_svc: SectionService):
    permission_svc = create_autospec(PermissionService)
    section_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        section = section_svc.delete(user_data.root, section_data.new_section)
        pytest.fail()


def test_delete_as_user(section_svc: SectionService):
    with pytest.raises(UserPermissionException):
        section = section_svc.delete(user_data.user, section_data.comp_101_001)
        pytest.fail()
