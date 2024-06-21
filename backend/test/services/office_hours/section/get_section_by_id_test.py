"""Tests for `get_section_by_id()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.course_site_details import OfficeHoursSectionDetails

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
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_section_by_id(oh_section_svc: OfficeHoursSectionService):
    """Test case for retrieving a section by its ID."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_section.id
    )

    assert isinstance(oh_section, OfficeHoursSectionDetails)
    assert oh_section.id == office_hours_data.comp_110_oh_section.id


def test_get_section_by_id_exception_invalid_section_id(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for raising an exception when retrieving a section with an invalid ID."""
    with pytest.raises(ResourceNotFoundException):
        oh_section_svc.get_section_by_id(user__comp110_student_0, 99)
