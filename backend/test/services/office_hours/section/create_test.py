"""Tests for `create()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.section_details import OfficeHoursSectionDetails
from .....services.academics.section import SectionService
from .....services.permission import PermissionService
from .....services.exceptions import ResourceNotFoundException
from .....services.office_hours.section import OfficeHoursSectionService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc
from ..fixtures import oh_section_svc
from ...academics.fixtures import section_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ...core_data import setup_insert_data_fixture as insert_order_0
from ...room_data import fake_data_fixture as insert_order_1
from ...academics.term_data import fake_data_fixture as insert_order_2
from ...academics.course_data import fake_data_fixture as insert_order_3
from ...academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import office_hours_data
from ...user_data import root
from .....services.exceptions import UserPermissionException

from ...academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp301_instructor,
    user__comp301_uta,
    user__comp301_student,
    comp_301_001_current_term,
    comp_110_001_current_term,
    comp_210_001_current_term,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_create_by_root(
    oh_section_svc: OfficeHoursSectionService, section_svc: SectionService
):
    """Test case to validate creation of an office hours section by an instructor."""
    oh_section = oh_section_svc.create(
        root,
        office_hours_data.oh_section_draft,
        [comp_301_001_current_term.id],
    )

    assert isinstance(oh_section, OfficeHoursSectionDetails)
    assert oh_section.title == office_hours_data.oh_section_draft.title


def test_create_by_root_and_linked_to_academic_section(
    oh_section_svc: OfficeHoursSectionService, section_svc: SectionService
):
    """Test case to validate creation of an office hours section linked to an academic section by an instructor."""
    oh_section = oh_section_svc.create(
        root,
        office_hours_data.oh_section_draft,
        [comp_301_001_current_term.id],
    )

    assert isinstance(oh_section, OfficeHoursSectionDetails)

    # Check if OH Section Is Linked to Academic Section
    academic_section = section_svc.get_by_id(comp_301_001_current_term.id)
    assert oh_section.id == academic_section.office_hours_section.id


def test_create_by_root_multiple_academic_sections(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to validate creation of an office hours section with multiple academic sections by an instructor."""
    oh_section = oh_section_svc.create(
        root,
        office_hours_data.oh_section_draft,
        [comp_301_001_current_term.id, comp_210_001_current_term.id],
    )

    assert isinstance(oh_section, OfficeHoursSectionDetails)
    assert oh_section.title == office_hours_data.oh_section_draft.title


def test_create_by_root_multiple_academic_sections_and_linked_to_academic_section(
    oh_section_svc: OfficeHoursSectionService, section_svc: SectionService
):
    """Test case to validate creation of an office hours section with multiple academic sections
    and linked to those academic sections by an instructor."""
    oh_section = oh_section_svc.create(
        root,
        office_hours_data.oh_section_draft,
        [comp_301_001_current_term.id, comp_210_001_current_term.id],
    )

    assert isinstance(oh_section, OfficeHoursSectionDetails)
    assert oh_section.title == office_hours_data.oh_section_draft.title

    # Check if OH Section Is Linked to Academic Sections
    comp301 = section_svc.get_by_id(comp_301_001_current_term.id)
    comp210 = section_svc.get_by_id(comp_210_001_current_term.id)

    assert oh_section.id == comp301.office_hours_section.id
    assert oh_section.id == comp210.office_hours_section.id


def test_create_exception_if_student(oh_section_svc: OfficeHoursSectionService):
    """Test case to validate that creating an office hours section raises a PermissionError if the user is a student."""
    with pytest.raises(UserPermissionException):
        oh_section_svc.create(
            user__comp301_student,
            office_hours_data.oh_section_draft,
            [comp_301_001_current_term.id],
        )
        pytest.fail()


def test_create_exception_if_ta(oh_section_svc: OfficeHoursSectionService):
    """Test case to validate that creating an office hours section raises a PermissionError if the user is a teaching assistant."""
    with pytest.raises(UserPermissionException):
        oh_section_svc.create(
            user__comp301_uta,
            office_hours_data.oh_section_draft,
            [comp_301_001_current_term.id],
        )
        pytest.fail()


def test_create_exception_if_non_member(oh_section_svc: OfficeHoursSectionService):
    """Test case to validate that creating an office hours section raises a PermissionError if the user is not a member of the section."""
    with pytest.raises(UserPermissionException):
        oh_section_svc.create(
            user__comp110_student_0,
            office_hours_data.oh_section_draft,
            [comp_301_001_current_term.id],
        )
        pytest.fail()


def test_create_exception_if_oh_section_exists(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to validate that creating an office hours section raises an Exception if a duplicate section already exists."""
    with pytest.raises(Exception):
        oh_section_svc.create(
            root,
            office_hours_data.oh_section_draft,
            [comp_110_001_current_term.id],
        )
        pytest.fail()


def test_create_exception_if_one_oh_section_exists_and_other_does_not_have_one(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to validate that creating an office hours section raises an Exception if one section exists but the other doesn't."""
    with pytest.raises(Exception):
        oh_section_svc.create(
            root,
            office_hours_data.oh_section_draft,
            [comp_110_001_current_term.id, comp_301_001_current_term.id],
        )
        pytest.fail()


def test_create_exception_if_can_not_find_all_academic_sections(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to validate that creating an office hours section raises an ResourceNotFoundException if all academic sections are not found."""
    with pytest.raises(ResourceNotFoundException):
        oh_section_svc.create(
            root,
            office_hours_data.oh_section_draft,
            [comp_301_001_current_term.id, 99],
        )
        pytest.fail()
