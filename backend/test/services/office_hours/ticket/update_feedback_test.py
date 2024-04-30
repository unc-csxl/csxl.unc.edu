"""Tests for `update_feedback()` in Office Hours Ticket Service."""

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


def test_update_ticket_feedback(oh_ticket_svc: OfficeHoursTicketService):
    """Test case for updating ticket feedback by a UTA."""
    mock_have_concerns = False
    mock_caller_notes = "Great to work with!"
    ticket = oh_ticket_svc.update_ticket_feedback(
        user__comp110_uta_0,
        OfficeHoursTicketPartial(
            id=office_hours_data.comp110_closed_ticket.id,
            have_concerns=mock_have_concerns,
            caller_notes=mock_caller_notes,
        ),
    )

    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.CLOSED
    assert ticket.have_concerns == mock_have_concerns
    assert ticket.caller_notes == mock_caller_notes


def test_update_ticket_feedback_exception_if_student(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if student tries to update ticket feedback."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.update_ticket_feedback(
            user__comp110_student_0,
            OfficeHoursTicketPartial(
                id=office_hours_data.comp110_closed_ticket.id,
                have_concerns=False,
                caller_notes="Great to work with!",
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_ticket_feedback_exception_if_ticket_not_closed(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if trying to update feedback on a non-closed ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.update_ticket_feedback(
            user__comp110_uta_0,
            OfficeHoursTicketPartial(
                id=office_hours_data.comp110_f23_queued_ticket.id,
                have_concerns=False,
                caller_notes="Great to work with!",
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_ticket_feedback_exception_if_missing_feedback(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if feedback is missing during update."""
    with pytest.raises(Exception):
        oh_ticket_svc.update_ticket_feedback(
            user__comp110_uta_0,
            OfficeHoursTicketPartial(
                id=office_hours_data.comp110_closed_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_ticket_feedback_exception_for_nonexisting_ticket(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised for updating feedback on a non-existing ticket."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.update_ticket_feedback(
            user__comp110_uta_0,
            OfficeHoursTicketPartial(
                id=99,
                have_concerns=False,
                caller_notes="Great to work with!",
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above
