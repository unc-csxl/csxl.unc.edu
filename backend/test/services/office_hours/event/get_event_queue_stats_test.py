"""Tests for `get_event_queue_stats()` in Office Hours Event Service."""

import pytest

from .....models.office_hours.event_status import OfficeHoursEventStatus

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


def test_get_event_queue_stats_by_student(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure queued and called OfficeHoursTickets can be retrieved by event for a student."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_f23_oh_event.id
    )
    status: OfficeHoursEventStatus = oh_event_svc.get_event_queue_stats(
        user__comp110_student_0, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 1
    assert status.queued_tickets_count == 1


def test_get_event_queue_stats_by_uta(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an office hours event ticket stats can be retrieved by an UTA."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_f23_oh_event.id
    )
    status: OfficeHoursEventStatus = oh_event_svc.get_event_queue_stats(
        user__comp110_uta_0, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 1
    assert status.queued_tickets_count == 1


def test_get_event_queue_stats_by_instructor(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an office hours event ticket stats can be retrieved by an instructor."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, office_hours_data.comp_110_f23_oh_event.id
    )
    status: OfficeHoursEventStatus = oh_event_svc.get_event_queue_stats(
        user__comp110_instructor, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 1
    assert status.queued_tickets_count == 1


def test_get_event_queue_stats_exception_for_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when non-member tries to retrieve an OH event queue stats."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_non_member, office_hours_data.comp_110_f23_oh_event.id
    )
    with pytest.raises(PermissionError):
        oh_event_svc.get_event_queue_stats(user__comp110_non_member, oh_event)
        pytest.fail()  # Fail test if no error was thrown above


def test_get_event_queue_stats_empty_queue(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure Event ticket stats can be retrieve for an empty queue."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, office_hours_data.comp_110_upcoming_oh_event.id
    )
    status: OfficeHoursEventStatus = oh_event_svc.get_event_queue_stats(
        user__comp110_instructor, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 0
    assert status.queued_tickets_count == 0
