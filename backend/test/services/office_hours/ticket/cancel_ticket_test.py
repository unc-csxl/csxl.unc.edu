"""Tests for `cancel_ticket()` in Office Hours Ticket Service."""

import pytest

from .....models.office_hours.ticket import OfficeHoursTicketPartial
from .....models.office_hours.ticket_details import OfficeHoursTicket
from .....models.office_hours.ticket_state import TicketState

from .....services.exceptions import ResourceNotFoundException
from .....services.office_hours.ticket import OfficeHoursTicketService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_ticket_svc

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
    user__comp110_gta,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_cancel_ticket_for_uta(oh_ticket_svc: OfficeHoursTicketService):
    """Test case for cancellation of ticket by a UTA."""
    cancelled_ticket = oh_ticket_svc.cancel_ticket(
        user__comp110_uta_0,
        OfficeHoursTicketPartial(id=office_hours_data.comp110_queued_ticket.id),
    )

    assert isinstance(cancelled_ticket, OfficeHoursTicket)
    assert cancelled_ticket.state == TicketState.CANCELED


def test_cancel_ticket_for_student(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for cancellation of ticket by a student."""
    cancelled_ticket = oh_ticket_svc.cancel_ticket(
        user__comp110_student_0,
        OfficeHoursTicketPartial(id=office_hours_data.comp110_queued_ticket.id),
    )

    assert isinstance(cancelled_ticket, OfficeHoursTicket)
    assert cancelled_ticket.state == TicketState.CANCELED


def test_cancel_ticket_exception_for_non_student_creator(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if non-student attempts to cancel a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.cancel_ticket(
            user__comp110_student_1,
            OfficeHoursTicketPartial(id=office_hours_data.comp110_queued_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_cancel_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if non-section member attempts to cancel a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.cancel_ticket(
            user__comp110_non_member,
            OfficeHoursTicketPartial(id=office_hours_data.comp110_queued_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_cancel_ticket_exception_when_invalid_ticket_id(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised for canceling ticket with invalid ID."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.cancel_ticket(
            user__comp110_student_0, OfficeHoursTicketPartial(id=99)
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_cancel_ticket_exception_when_ticket_not_queued(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when trying to cancel a non-queued ticket."""
    with pytest.raises(Exception):
        oh_ticket_svc.cancel_ticket(
            user__comp110_student_0,
            OfficeHoursTicketPartial(id=office_hours_data.comp110_called_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above
