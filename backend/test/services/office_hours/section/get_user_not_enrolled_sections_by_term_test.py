"""Tests for `get_user_not_enrolled_sections_by_term()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.course_site import OfficeHoursSection

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
from ...academics import term_data
from ...academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_uta_0,
    user__comp301_instructor,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_user_not_enrolled_sections_by_term_student(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to retrieve sections not enrolled by a student for a specific term."""
    oh_sections = oh_section_svc.get_user_not_enrolled_sections_by_term(
        user__comp110_student_0, term_data.current_term.id
    )

    assert isinstance(oh_sections[0], OfficeHoursSection)
    # Student By Default Is Enrolled in One OH Section
    assert len(oh_sections) == len(office_hours_data.current_term_oh_sections) - 1


def test_get_user_not_enrolled_sections_by_term_uta(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to retrieve sections not enrolled by a UTA for a specific term."""
    oh_sections = oh_section_svc.get_user_not_enrolled_sections_by_term(
        user__comp110_uta_0, term_data.current_term.id
    )

    assert isinstance(oh_sections[0], OfficeHoursSection)
    # By Default Is Enrolled in One OH Section - Only Existing OH Section
    assert len(oh_sections) == len(office_hours_data.current_term_oh_sections) - 1


def test_get_user_not_enrolled_sections_by_term_enrolled_in_none(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case to retrieve sections not enrolled by a non-member for a specific term."""
    oh_sections = oh_section_svc.get_user_not_enrolled_sections_by_term(
        user__comp110_non_member, term_data.f_23.id
    )

    assert isinstance(oh_sections[0], OfficeHoursSection)
    # By Default Is Enrolled in One OH Section - Only Existing OH Section
    assert len(oh_sections) == len(office_hours_data.f23_oh_sections)
