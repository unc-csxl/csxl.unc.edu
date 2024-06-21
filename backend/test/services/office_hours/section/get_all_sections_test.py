"""Tests for `get_all_sections()` in Office Hours Section Service."""

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
from .. import office_hours_data
from ... import user_data

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_all_sections(oh_section_svc: OfficeHoursSectionService):
    """Test case for retrieving all office hours sections."""
    sections = oh_section_svc.get_all_sections(user_data.student)

    assert isinstance(sections[0], OfficeHoursSectionDetails)
    assert len(sections) == len(office_hours_data.oh_sections)
