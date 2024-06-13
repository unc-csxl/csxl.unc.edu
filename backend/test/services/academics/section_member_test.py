"""Tests for Section Member Service."""

import pytest

from ....models.office_hours.section_details import OfficeHoursSectionDetails
from ....models.office_hours.section_details import OfficeHoursSectionDetails
from ....models.academics.section_member import SectionMember
from ....models.roster_role import RosterRole
from ....models.pagination import PaginationParams

from ....services.academics.section_member import SectionMemberService
from ....services.academics.my_courses import MyCoursesService
from ....services.exceptions import (
    ResourceNotFoundException,
)
from ....services.office_hours.section import OfficeHoursSectionService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_member_svc, my_courses_svc
from ..office_hours.fixtures import oh_section_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from .term_data import fake_data_fixture as insert_order_1
from .course_data import fake_data_fixture as insert_order_2
from .section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from . import section_data
from .. import user_data
from ..office_hours import office_hours_data

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


def test_get_section_member_by_user_id_and_oh_section_id_instructor(
    section_member_svc: SectionMemberService,
):
    """Test case to retrieve a section member by user ID and section ID (instructor)."""
    section_member = section_member_svc.get_section_member_by_user_id_and_oh_section_id(
        section_data.user__comp110_instructor, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(section_member, SectionMember)
    assert section_member.id == section_data.comp110_instructor.id


def test_get_section_member_by_user_id_and_oh_section_id_student(
    section_member_svc: SectionMemberService,
):
    """Test case to retrieve a section member by user ID and section ID (student)."""
    section_member = section_member_svc.get_section_member_by_user_id_and_oh_section_id(
        section_data.user__comp110_student_0, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(section_member, SectionMember)
    assert section_member.id == section_data.comp110_student_0.id


def test_get_section_member_by_user_id_and_oh_section_id_exception_not_found(
    section_member_svc: SectionMemberService,
):
    """Test case to check if retrieving a section member for a non-member raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        section_member_svc.get_section_member_by_user_id_and_oh_section_id(
            section_data.user__comp110_non_member,
            office_hours_data.comp_110_oh_section.id,
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


def test_add_user_section_memberships_by_oh_sections(
    section_member_svc: SectionMemberService, oh_section_svc: OfficeHoursSectionService
):
    """Test case to add user section memberships by Office Hours sections."""
    target_oh_section = office_hours_data.comp_523_oh_section
    user_to_add = section_data.user__comp110_student_1

    section = oh_section_svc.get_section_by_id(user_to_add, target_oh_section.id)
    assert isinstance(section, OfficeHoursSectionDetails)

    sections: list[OfficeHoursSectionDetails] = [section]
    memberships = section_member_svc.add_user_section_memberships_by_oh_sections(
        user_to_add, sections
    )

    assert len(memberships) == 1
    assert isinstance(memberships[0], SectionMember)

    membership = section_member_svc.get_section_member_by_user_id_and_oh_section_id(
        user_to_add, target_oh_section.id
    )

    assert membership is not None


def test_add_user_section_memberships_by_oh_sections_multiple_sections(
    section_member_svc: SectionMemberService, oh_section_svc: OfficeHoursSectionService
):
    """Test case to add user section memberships with multiple Office Hours sections."""
    target_oh_section_0 = office_hours_data.comp_523_oh_section
    target_oh_section_1 = office_hours_data.comp_110_oh_section
    user_to_add = user_data.root

    comp_523_section_details = oh_section_svc.get_section_by_id(
        user_to_add, target_oh_section_0.id
    )

    assert comp_523_section_details is not None
    assert isinstance(comp_523_section_details, OfficeHoursSectionDetails)

    comp_110_section_details = oh_section_svc.get_section_by_id(
        user_to_add, target_oh_section_1.id
    )

    assert comp_110_section_details is not None
    assert isinstance(comp_110_section_details, OfficeHoursSectionDetails)

    sections = [comp_523_section_details, comp_110_section_details]

    memberships = section_member_svc.add_user_section_memberships_by_oh_sections(
        user_to_add, sections
    )

    assert len(memberships) == 2
    assert isinstance(memberships[0], SectionMember)

    for section in sections:
        membership = section_member_svc.get_section_member_by_user_id_and_oh_section_id(
            user_to_add, section.id
        )

        assert membership is not None


def test_add_user_section_memberships_by_oh_sections_exception_if_already_enrolled(
    section_member_svc: SectionMemberService, oh_section_svc: OfficeHoursSectionService
):
    """Test case to check if adding user section memberships fails if already enrolled."""
    target_oh_section = office_hours_data.comp_110_oh_section
    user_to_add = section_data.user__comp110_student_0

    comp_110_section_details = oh_section_svc.get_section_by_id(
        user_to_add, target_oh_section.id
    )

    assert comp_110_section_details is not None
    assert isinstance(comp_110_section_details, OfficeHoursSectionDetails)

    with pytest.raises(Exception):
        section_member_svc.add_user_section_memberships_by_oh_sections(
            user_to_add, comp_110_section_details
        )
        pytest.raises()


def test_add_user_section_memberships_by_oh_sections_exception_if_given_multiple_sections_and_already_enrolled_in_one(
    section_member_svc: SectionMemberService, oh_section_svc: OfficeHoursSectionService
):
    """Test case to check if adding user section memberships fails if already enrolled in one section."""
    target_oh_section_0 = office_hours_data.comp_523_oh_section
    target_oh_section_1 = office_hours_data.comp_110_oh_section
    user_to_add = section_data.user__comp110_student_0

    comp_523_section_details = oh_section_svc.get_section_by_id(
        user_to_add, target_oh_section_0.id
    )

    assert comp_523_section_details is not None
    assert isinstance(comp_523_section_details, OfficeHoursSectionDetails)

    comp_110_section_details = oh_section_svc.get_section_by_id(
        user_to_add, target_oh_section_1.id
    )

    assert comp_110_section_details is not None
    assert isinstance(comp_110_section_details, OfficeHoursSectionDetails)

    sections = [comp_523_section_details, comp_110_section_details]

    with pytest.raises(Exception):
        section_member_svc.add_user_section_memberships_by_oh_sections(
            user_to_add, sections
        )
        pytest.raises()


def test_add_user_section_memberships_by_oh_sections_exception_invalid_id(
    section_member_svc: SectionMemberService, oh_section_svc: OfficeHoursSectionService
):
    """Test case to check if adding user section memberships fails with an invalid section ID."""
    target_oh_section = office_hours_data.comp_110_oh_section
    user_to_add = section_data.user__comp110_student_0

    comp_110_section_details = oh_section_svc.get_section_by_id(
        user_to_add, target_oh_section.id
    )

    assert comp_110_section_details is not None
    assert isinstance(comp_110_section_details, OfficeHoursSectionDetails)

    comp_110_section_details.id = 99

    with pytest.raises(ResourceNotFoundException):
        section_member_svc.add_user_section_memberships_by_oh_sections(
            user_to_add, [comp_110_section_details]
        )
        pytest.raises()


def test_get_roster(my_courses_svc: MyCoursesService):
    my_courses_svc.get_course_roster(
        user_data.ambassador, "SSI24", "comp301", PaginationParams()
    )
