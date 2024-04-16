"""Tests for `create()` in Office Hours Event Service."""

import pytest

from .....models.office_hours.event import OfficeHoursEvent

from .....services.office_hours.event import OfficeHoursEventService

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
    user__comp110_non_member,
)


__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_create_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be created by a UTA."""
    oh_event = oh_event_svc.create(
        user__comp110_uta_0, office_hours_data.comp110_event_draft
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.description == office_hours_data.comp110_event_draft.description


def test_create_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be created by an instructor."""
    oh_event = oh_event_svc.create(
        user__comp110_instructor, office_hours_data.comp110_event_draft
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.description == office_hours_data.comp110_event_draft.description


def test_create_exception_if_student(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an exception is raised when a student tries to create an OfficeHoursEvent."""
    with pytest.raises(PermissionError):
        oh_event_svc.create(
            user__comp110_student_0, office_hours_data.comp110_event_draft
        )
        pytest.fail(
            "Expected PermissionError was not raised."
        )  # Fail test if no error was thrown above


def test_create_exception_if_non_member(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an exception is raised when a non-member tries to create an OfficeHoursEvent."""
    with pytest.raises(PermissionError):
        oh_event_svc.create(
            user__comp110_non_member, office_hours_data.comp110_event_draft
        )
        pytest.fail(
            "Expected PermissionError was not raised."
        )  # Fail test if no error was thrown above
