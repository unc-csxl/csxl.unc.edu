"""Tests for Section Member Service."""

import pytest

from ....models.academics.section_member import SectionMember
from ....models.roster_role import RosterRole
from ....services.academics.section_member import SectionMemberService
from ....services.exceptions import (
    ResourceNotFoundException,
)

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_member_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from .term_data import fake_data_fixture as insert_order_1
from .course_data import fake_data_fixture as insert_order_2
from .section_data import fake_data_fixture as insert_order_3

# Import the fake model data in a namespace for test assertions
from . import section_data
from .. import user_data

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_section_member_by_id(section_member_svc: SectionMemberService):
    """Test case to retrieve a section member by ID."""
    section_member = section_member_svc.get_section_member_by_id(id=1)

    assert isinstance(section_member, SectionMember)
    assert section_member.id == section_data.comp110_instructor.id


def test_get_section_member_by_id_exception_if_invalid_id(
    section_member_svc: SectionMemberService,
):
    """Test case to check if retrieving a section member by an invalid ID raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        section_member_svc.get_section_member_by_id(id=99)
        pytest.fail()


def test_get_section_member_by_user_id_and_section_id_instructor(
    section_member_svc: SectionMemberService,
):
    """Test case to retrieve a section member by user ID and section ID (instructor)."""
    section_member = section_member_svc.get_section_member_by_user_id_and_oh_section_id(
        section_data.user__comp110_instructor, section_data.comp_101_001.id
    )

    assert isinstance(section_member, SectionMember)
    assert section_member.id == section_data.comp110_instructor.id


def test_get_section_member_by_user_id_and_section_id_student(
    section_member_svc: SectionMemberService,
):
    """Test case to retrieve a section member by user ID and section ID (student)."""
    section_member = section_member_svc.get_section_member_by_user_id_and_oh_section_id(
        section_data.user__comp110_student_0, section_data.comp_101_001.id
    )

    assert isinstance(section_member, SectionMember)
    assert section_member.id == section_data.comp110_student_0.id


def test_get_section_member_by_user_id_and_section_id_exception_not_found(
    section_member_svc: SectionMemberService,
):
    """Test case to check if retrieving a section member for a non-member raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        section_member_svc.get_section_member_by_user_id_and_oh_section_id(
            section_data.user__comp110_non_member, section_data.comp_101_001.id
        )


def test_search_instructor_memberships(section_member_svc: SectionMemberService):
    """Test case to search for instructor memberships."""
    memberships = section_member_svc.search_instructor_memberships(user_data.instructor)

    assert len(memberships) > 0
    assert isinstance(memberships[0], SectionMember)

    for membership in memberships:
        assert membership.member_role == RosterRole.INSTRUCTOR


def test_search_instructor_memberships_non_instructor(
    section_member_svc: SectionMemberService,
):
    """Test case to search for instructor memberships with a non-instructor user."""
    memberships = section_member_svc.search_instructor_memberships(user_data.student)

    assert len(memberships) == 0


# TODO: add_user_section_memberships_by_oh_sections()
