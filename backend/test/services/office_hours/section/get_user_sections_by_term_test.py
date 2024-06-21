"""Tests for `get_user_sections_by_term()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.course_site_details import OfficeHoursSectionDetails

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
from ... import user_data
from .. import office_hours_data
from ...academics import term_data


__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_user_sections_by_term(oh_section_svc: OfficeHoursSectionService):
    """Test case for retrieving user sections by term and validating details."""
    sections = oh_section_svc.get_user_sections_by_term(
        user_data.user, term_data.current_term.id
    )
    assert isinstance(sections[0], OfficeHoursSectionDetails)
    assert len(sections) == 1  # Only Enrolled in COMP 110 OH Section
    assert sections[0].id == office_hours_data.comp_110_oh_section.id


def test_get_user_sections_by_term_no_oh_sections(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving user sections by term when no OH sections exist."""
    sections = oh_section_svc.get_user_sections_by_term(
        user_data.root, term_data.current_term.id
    )
    assert len(sections) == 0


def test_get_user_sections_by_term_instructor(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving user sections by term for an instructor."""
    sections = oh_section_svc.get_user_sections_by_term(
        user_data.instructor, term_data.current_term.id
    )
    assert isinstance(sections[0], OfficeHoursSectionDetails)
    assert len(sections) == len(
        office_hours_data.current_term_oh_sections
    )  # COMP 110 and COMP 523OH Section


def test_get_user_sections_by_term_invalid_term_id_returns_empty_list(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving user sections by term with an invalid term ID, expecting an empty list."""
    sections = oh_section_svc.get_user_sections_by_term(user_data.instructor, "invalid")
    assert len(sections) == 0
