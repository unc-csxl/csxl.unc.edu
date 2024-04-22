"""Tests for `get_sections_by_term()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.section_details import OfficeHoursSectionDetails

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
    user__comp110_student_0,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_sections_by_term(oh_section_svc: OfficeHoursSectionService):
    """Test case for retrieving sections by term and validating section details and count."""

    sections = oh_section_svc.get_sections_by_term(
        user__comp110_student_0, term_data.f_23.id
    )
    assert isinstance(
        sections[0], OfficeHoursSectionDetails
    )  # Check type of first section.
    assert len(sections) == len(
        office_hours_data.f23_oh_sections
    )  # Ensure correct number of sections returned.


def test_get_sections_by_term_no_sections(oh_section_svc: OfficeHoursSectionService):
    """Test case for retrieving sections by term when no sections are expected to be found."""

    sections = oh_section_svc.get_sections_by_term(
        user__comp110_student_0, term_data.sp_23.id
    )
    assert len(sections) == 0  # Assert no sections are returned.


def test_get_sections_by_term_empty_if_invalid_term_id(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving sections by term with an invalid term ID, expecting an empty result."""

    sections = oh_section_svc.get_sections_by_term(user__comp110_student_0, "none")
    assert len(sections) == 0  # Ensure no sections are returned for an invalid term ID.
