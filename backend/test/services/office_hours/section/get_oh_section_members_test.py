"""Tests for `get_oh_section_members()` in Office Hours Section Service."""

import pytest

from .....models.academics.section_member import SectionMember
from .....models.office_hours.section import OfficeHoursSectionPartial

from .....services.exceptions import ResourceNotFoundException
from .....services.office_hours.section import OfficeHoursSectionService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_section_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ...core_data import setup_insert_data_fixture as insert_order_0
from ...room_data import fake_data_fixture as insert_order_1
from ...academics.term_data import fake_data_fixture as insert_order_2
from ...academics.course_data import fake_data_fixture as insert_order_3
from ...academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import office_hours_data
from ...academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_uta_0,
    user__comp110_non_member,
    comp110_members,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_oh_section_members_by_uta(oh_section_svc: OfficeHoursSectionService):
    """Test case to retrieve members of an office hours section by UTA."""
    delta = OfficeHoursSectionPartial(id=office_hours_data.comp_110_oh_section.id)
    section_members = oh_section_svc.get_oh_section_members(user__comp110_uta_0, delta)

    assert isinstance(section_members[0], SectionMember)
    assert len(section_members) == len(comp110_members)


def test_get_oh_section_members_by_instructor(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to retrieve members of an office hours section by instructor."""
    delta = OfficeHoursSectionPartial(id=office_hours_data.comp_110_oh_section.id)
    section_members = oh_section_svc.get_oh_section_members(
        user__comp110_instructor, delta
    )

    assert isinstance(section_members[0], SectionMember)
    assert len(section_members) == len(comp110_members)


def test_get_oh_section_members_exception_if_student(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to check if retrieving section members raises an exception when called by a student."""
    delta = OfficeHoursSectionPartial(id=office_hours_data.comp_110_oh_section.id)

    with pytest.raises(PermissionError):
        oh_section_svc.get_oh_section_members(user__comp110_student_0, delta)


def test_get_oh_section_members_exception_if_invalid_section_id(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to check if retrieving section members raises an exception for an invalid section ID."""
    delta = OfficeHoursSectionPartial(id=99)

    with pytest.raises(ResourceNotFoundException):
        oh_section_svc.get_oh_section_members(user__comp110_uta_0, delta)
        pytest.fail()


def test_get_oh_section_members_exception_if_non_member(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to check if retrieving section members raises an exception for a non-member."""
    delta = OfficeHoursSectionPartial(id=99)

    with pytest.raises(ResourceNotFoundException):
        oh_section_svc.get_oh_section_members(user__comp110_non_member, delta)
        pytest.fail()
