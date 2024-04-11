"""Tests for Office Hours Ticket Service."""

import pytest

from ....models.office_hours.ticket import OfficeHoursTicketPartial
from ....models.office_hours.ticket_details import OfficeHoursTicketDetails
from ....models.office_hours.ticket_state import TicketState

from ....services.exceptions import ResourceNotFoundException
from ....services.office_hours.ticket import OfficeHoursTicketService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, oh_ticket_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..room_data import fake_data_fixture as insert_order_1
from ..academics.term_data import fake_data_fixture as insert_order_2
from ..academics.course_data import fake_data_fixture as insert_order_3
from ..academics.section_data import fake_data_fixture as insert_order_4
from .office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from . import office_hours_data
from ..academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_student_1,
    user__comp110_uta_0,
    user__comp110_uta_1,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_create_ticket(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to ensure a ticket is successfully created and is in QUEUED state."""
    ticket = oh_ticket_svc.create(
        user__comp110_student_0, office_hours_data.ticket_draft
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.QUEUED

    assert len(ticket.creators) == 1


def test_create_ticket_group(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to ensure a group ticket (ticket with list of creators) is successfully created and is in QUEUED state."""
    ticket = oh_ticket_svc.create(
        user__comp110_student_0, office_hours_data.group_ticket_draft
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.QUEUED

    assert len(ticket.creators) == 2


def test_create_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that creating a ticket by a non-section member raises PermissionError."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(user__comp110_non_member, office_hours_data.ticket_draft)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_for_non_section_member_group_ticket(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that creating a group ticket by a non-section member raises PermissionError."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(
            user__comp110_non_member, office_hours_data.group_ticket_draft_non_member
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_if_not_student(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that creating a ticket by a section member UTA raises PermissionError."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(user__comp110_uta_0, office_hours_data.ticket_draft)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_invalid_event(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that creating a ticket with an invalid event raises ResourceNotFoundException."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.create(
            user__comp110_non_member, office_hours_data.ticket_draft_invalid_event
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_get_ticket_by_id_student_creator(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to validate getting a ticket by ID returns correct ticket details."""
    ticket = oh_ticket_svc.get_ticket_by_id(
        user__comp110_student_0, office_hours_data.called_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.called_ticket.id
    assert ticket.state == office_hours_data.called_ticket.state


def test_get_ticket_by_id_for_section_uta(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to validate getting a ticket by ID for section UTA returns ticket correct ticket details."""
    ticket = oh_ticket_svc.get_ticket_by_id(
        user__comp110_uta_0, office_hours_data.pending_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.pending_ticket.id


def test_get_ticket_by_id_for_section_instructor(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate getting a ticket by ID for section Instructor returns ticket correct ticket details."""
    ticket = oh_ticket_svc.get_ticket_by_id(
        user__comp110_instructor, office_hours_data.pending_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.pending_ticket.id


def test_get_ticket_by_id_exception_when_ticket_id_does_not_exist(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate an exception is raised when retrieving a non-existing ticket by ID."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.get_ticket_by_id(user__comp110_student_0, 10)
        pytest.fail()  # Fail test if no error was thrown above


def test_get_ticket_by_id_exception_if_student_user_not_ticket_creator(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate a PermissionError exception is raised if a student user is not the ticket creator."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.get_ticket_by_id(
            user__comp110_student_1, office_hours_data.pending_ticket.id
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_get_ticket_by_id_exception_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate a PermissionError exception is raised when a non-section member tries to retrieve a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.get_ticket_by_id(
            user__comp110_non_member, office_hours_data.pending_ticket.id
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_called_state(oh_ticket_svc: OfficeHoursTicketService):
    """Test case for updating ticket to 'called' state."""
    ticket = oh_ticket_svc.update_called_state(
        subject=user__comp110_uta_0,
        oh_ticket=OfficeHoursTicketPartial(
            id=office_hours_data.pending_ticket.id,
        ),
    )

    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.CALLED


def test_update_called_state_exception_if_student_calls(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if a student attempts to update ticket state to 'called'."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.update_called_state(
            subject=user__comp110_student_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=office_hours_data.pending_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_called_state_exception_if_ticket_has_caller_already(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if a ticket already has a caller."""
    with pytest.raises(Exception):
        oh_ticket_svc.update_called_state(
            subject=user__comp110_uta_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=office_hours_data.called_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_called_state_exception_for_nonexisting_ticket_id(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when updating state of a non-existing ticket."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.update_called_state(
            subject=user__comp110_uta_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=10,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_called_state_exception_if_ticket_is_not_queued(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when trying to update state of a ticket that's not queued."""
    with pytest.raises(Exception):
        oh_ticket_svc.update_called_state(
            subject=user__comp110_uta_0,
            oh_ticket=OfficeHoursTicketPartial(
                id=office_hours_data.called_ticket.id,
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_cancel_ticket_for_uta(oh_ticket_svc: OfficeHoursTicketService):
    """Test case for cancellation of ticket by a UTA."""
    cancelled_ticket = oh_ticket_svc.cancel_ticket(
        user__comp110_uta_0,
        OfficeHoursTicketPartial(id=office_hours_data.pending_ticket.id),
    )

    assert isinstance(cancelled_ticket, OfficeHoursTicketDetails)
    assert cancelled_ticket.state == TicketState.CANCELED


def test_cancel_ticket_for_student(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for cancellation of ticket by a student."""
    cancelled_ticket = oh_ticket_svc.cancel_ticket(
        user__comp110_student_0,
        OfficeHoursTicketPartial(id=office_hours_data.pending_ticket.id),
    )

    assert isinstance(cancelled_ticket, OfficeHoursTicketDetails)
    assert cancelled_ticket.state == TicketState.CANCELED


def test_cancel_ticket_exception_for_non_student_creator(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if non-student attempts to cancel a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.cancel_ticket(
            user__comp110_student_1,
            OfficeHoursTicketPartial(id=office_hours_data.pending_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_cancel_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if non-section member attempts to cancel a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.cancel_ticket(
            user__comp110_non_member,
            OfficeHoursTicketPartial(id=office_hours_data.pending_ticket.id),
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
            OfficeHoursTicketPartial(id=office_hours_data.called_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_close_ticket(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for closing a ticket by a UTA."""
    closed_ticket = oh_ticket_svc.close_ticket(
        user__comp110_uta_0,
        OfficeHoursTicketPartial(id=office_hours_data.called_ticket.id),
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
            OfficeHoursTicketPartial(id=office_hours_data.called_ticket.id),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_close_ticket_exception_if_ticket_not_called(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised when trying to close a ticket that hasn't been called."""
    with pytest.raises(Exception):
        oh_ticket_svc.close_ticket(
            user__comp110_student_0,
            OfficeHoursTicketPartial(id=office_hours_data.pending_ticket.id),
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


def test_update_ticket_feedback(oh_ticket_svc: OfficeHoursTicketService):
    """Test case for updating ticket feedback by a UTA."""
    mock_have_concerns = False
    mock_caller_notes = "Great to work with!"
    ticket = oh_ticket_svc.update_ticket_feedback(
        user__comp110_uta_0,
        OfficeHoursTicketPartial(
            id=office_hours_data.closed_ticket.id,
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
                id=office_hours_data.closed_ticket.id,
                have_concerns=False,
                caller_notes="Great to work with!",
            ),
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_update_ticket_feedback_exception_if_not_ticket_caller(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case for exception raised if non-ticket caller tries to update feedback."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.update_ticket_feedback(
            user__comp110_uta_1,
            OfficeHoursTicketPartial(
                id=office_hours_data.closed_ticket.id,
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
                id=office_hours_data.pending_ticket.id,
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
                id=office_hours_data.closed_ticket.id,
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
