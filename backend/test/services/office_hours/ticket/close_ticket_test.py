"""Tests for `close_ticket()` in Office Hours Ticket Service."""

import pytest

from .....models.office_hours.ticket import OfficeHoursTicketPartial
from .....models.office_hours.ticket_details import OfficeHoursTicketDetails
from .....models.office_hours.ticket_state import TicketState

from .....services.exceptions import ResourceNotFoundException
from .....services.office_hours.ticket import OfficeHoursTicketService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_ticket_svc, oh_event_svc

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


def test_close_ticket(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for closing a ticket by a UTA."""
    closed_ticket = oh_ticket_svc.close_ticket(
        user__comp110_uta_0,
        OfficeHoursTicketPartial(id=office_hours_data.comp110_f23_called_ticket.id),
    )

    assert isinstance(closed_ticket, OfficeHoursTicketDetails)
    assert closed_ticket.state == TicketState.CLOSED
    assert closed_ticket.closed_at is not None


def test_close_ticket_exception_when_student_closes(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if student attempts to close a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.close_ticket(
            user__comp110_student_0,
            OfficeHoursTicketPartial(id=office_hours_data.comp110_f23_called_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_close_ticket_exception_if_ticket_not_called(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when trying to close a ticket that hasn't been called."""
    with pytest.raises(Exception):
        oh_ticket_svc.close_ticket(
            user__comp110_student_0,
            OfficeHoursTicketPartial(id=office_hours_data.comp110_f23_queued_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_close_ticket_exception_invalid_ticket_id(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when closing a ticket with an invalid ID."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.close_ticket(
            user__comp110_student_0,
            OfficeHoursTicketPartial(id=99),
        )
        pytest.fail()  # Fail test if no error was thrown above
