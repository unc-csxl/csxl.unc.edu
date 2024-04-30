"""Tests for `call_ticket()` in Office Hours Ticket Service."""

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


def test_call_ticket(oh_ticket_svc: OfficeHoursTicketService):
    """Test case for updating ticket to 'called' state."""
    ticket = oh_ticket_svc.call_ticket(
        subject=user__comp110_uta_0,
        oh_ticket=OfficeHoursTicketPartial(
            id=office_hours_data.comp110_queued_ticket.id,
        ),
    )

    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.CALLED


def test_call_ticket_exception_if_student_calls(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if a student attempts to update ticket state to 'called'."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.call_ticket(
            subject=user__comp110_student_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=office_hours_data.comp110_queued_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_call_ticket_exception_if_ticket_has_caller_already(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if a ticket already has a caller."""
    with pytest.raises(Exception):
        oh_ticket_svc.call_ticket(
            subject=user__comp110_uta_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=office_hours_data.comp110_called_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_call_ticket_exception_for_nonexisting_ticket_id(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when updating state of a non-existing ticket."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.call_ticket(
            subject=user__comp110_uta_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=10,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_call_ticket_exception_if_ticket_is_not_queued(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when trying to update state of a ticket that's not queued."""
    with pytest.raises(Exception):
        oh_ticket_svc.call_ticket(
            subject=user__comp110_uta_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=office_hours_data.comp110_called_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above
