"""Tests for `get_event_by_id()` Office Hours Event Service."""

import pytest

from .....models.office_hours.office_hours import OfficeHoursEvent

from .....services.exceptions import ResourceNotFoundException
from .....services.office_hours.office_hours import OfficeHoursEventService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_event_svc

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
)


__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"
license__ = "MIT"


def test_get_event_by_id_by_student(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be retrieved by its ID by student."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_current_oh_event.id
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.id == office_hours_data.comp_110_current_oh_event.id


def test_get_event_by_id_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be retrieved by its ID by UTA."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_current_oh_event.id
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.id == office_hours_data.comp_110_current_oh_event.id


def test_get_event_by_id_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be retrieved by its ID by Instructor."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, office_hours_data.comp_110_current_oh_event.id
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.id == office_hours_data.comp_110_current_oh_event.id


def test_get_event_by_id_exception_non_existing_event(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when retrieving a non-existing OfficeHoursEvent by ID."""
    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.get_event_by_id(user__comp110_student_0, 99)
        pytest.fail()  # Fail test if no error was thrown above
