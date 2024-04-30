"""Tests for `check_student_in_queue_status()` in Office Hours Event Service."""

import pytest

from .....models.office_hours.event_status import StudentQueuedTicketStatus

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
    user__comp110_gta,
    user__comp110_non_member,
    user__comp110_student_0,
    user__comp110_student_1,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_check_student_in_queue_status(oh_event_svc: OfficeHoursEventService):
    """Test case to check the student queue status for an ongoing event with an active ticket."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_f23_oh_event.id
    )
    status = oh_event_svc.check_student_in_queue_status(
        user__comp110_student_0, oh_event
    )

    assert isinstance(status, StudentQueuedTicketStatus)
    assert status.ticket_id == office_hours_data.comp110_f23_queued_ticket.id


def test_check_student_in_queue_status_no_active_ticket(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to check the student queue status for an ongoing event when no active tickets created."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_1, office_hours_data.comp_110_current_oh_event.id
    )
    status = oh_event_svc.check_student_in_queue_status(
        user__comp110_student_1, oh_event
    )

    assert isinstance(status, StudentQueuedTicketStatus)
    assert status.ticket_id is None


def test_test_check_student_in_queue_status_exception_if_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to check an expection is raised if a non member."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_gta, office_hours_data.comp_110_current_oh_event.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.check_staff_helping_status(user__comp110_non_member, oh_event)
        pytest.fail()
