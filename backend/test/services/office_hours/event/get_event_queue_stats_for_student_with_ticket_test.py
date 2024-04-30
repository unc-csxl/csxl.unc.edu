"""Tests for `get_event_queue_stats_for_student_with_ticket()` in Office Hours Event Service function."""

import pytest

from .....models.office_hours.event_status import (
    StudentOfficeHoursEventStatus,
)

from .....services.exceptions import ResourceNotFoundException
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
    user__comp110_student_1,
    user__comp110_uta_0,
    user__comp110_non_member,
)


__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_queued_helped_stats_by_oh_event_for_student(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure fetching queued and helped stats for an event by a student."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_f23_oh_event.id
    )
    student_ticket_status = oh_event_svc.get_event_queue_stats_for_student_with_ticket(
        user__comp110_student_0,
        oh_event,
        office_hours_data.comp110_f23_queued_ticket.id,
    )

    assert isinstance(student_ticket_status, StudentOfficeHoursEventStatus)
    assert student_ticket_status.queued_tickets_count == 1
    assert student_ticket_status.ticket_position == 1


def test_get_queued_helped_stats_by_oh_event_for_student_exception_invalid_ticket_id(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure a ResourceNotFoundException is raised for an invalid ticket ID."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_f23_oh_event.id
    )

    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.get_event_queue_stats_for_student_with_ticket(
            user__comp110_student_0, oh_event, 99
        )
        pytest.fail()


def test_get_queued_helped_stats_by_oh_event_for_student_exception_ticket_not_in_event(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when the ticket does not belong to the specified event."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_upcoming_oh_event.id
    )

    with pytest.raises(Exception):
        oh_event_svc.get_event_queue_stats_for_student_with_ticket(
            user__comp110_student_0,
            oh_event,
            office_hours_data.comp110_f23_queued_ticket.id,
        )
        pytest.fail()


def test_get_queued_helped_stats_by_oh_event_for_student_exception_ticket_not_queued(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when attempting to get stats for a ticket not in the queued state."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_f23_oh_event.id
    )

    with pytest.raises(Exception):
        oh_event_svc.get_event_queue_stats_for_student_with_ticket(
            user__comp110_student_0,
            oh_event,
            office_hours_data.comp110_f23_called_ticket.id,
        )
        pytest.fail()


def test_get_queued_helped_stats_by_oh_event_for_student_exception_if_not_ticket_creator(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised if a student attemps to view for a student ticket queue stats for a ticket_id did not create."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_f23_oh_event.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.get_event_queue_stats_for_student_with_ticket(
            user__comp110_student_1,
            oh_event,
            office_hours_data.comp110_f23_called_ticket.id,
        )
        pytest.fail()
