"""Tests for `create()` in Office Hours Ticket Service."""

import pytest

from backend.services.office_hours.office_hours import OfficeHoursEventService

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


def test_create_ticket(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to ensure a ticket is successfully created and is in QUEUED state."""
    ticket = oh_ticket_svc.create(
        user__comp110_student_0, office_hours_data.ticket_draft_current_term_comp110
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.QUEUED

    assert len(ticket.creators) == 1


def test_create_ticket_group(
    oh_ticket_svc: OfficeHoursTicketService, oh_event_svc: OfficeHoursEventService
):
    """Test case to ensure a group ticket (ticket with list of creators) is successfully created and is in QUEUED state."""
    ticket = oh_ticket_svc.create(
        user__comp110_student_0,
        office_hours_data.group_ticket_draft,
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.QUEUED

    assert len(ticket.creators) == 2


def test_create_ticket_exception_if_already_created_ticket_in_cooldown_period(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to ensure an exception if thrown if student calls a ticket in past hour."""

    with pytest.raises(PermissionError):
        oh_ticket_svc.create(
            user__comp110_student_1, office_hours_data.ticket_draft_f23
        )
        pytest.fail()


def test_create_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that creating a ticket by a non-section member raises PermissionError."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(
            user__comp110_non_member, office_hours_data.ticket_draft_f23
        )
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
        oh_ticket_svc.create(user__comp110_uta_0, office_hours_data.ticket_draft_f23)
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


def test_create_ticket_exception_if_queued_ticket_already(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that a student with a queued ticket attempting to creating a ticket raises PermissionError."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(
            user__comp110_student_0, office_hours_data.ticket_draft_f23
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_if_queued_ticket_already_group(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate that a student in a ticket group with a queued ticket attempting to creating a ticket raises PermissionError."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(
            user__comp110_student_0,
            office_hours_data.group_ticket_draft_comp_110_f23,
        )
        pytest.fail()  # Fail test if no error was thrown above
