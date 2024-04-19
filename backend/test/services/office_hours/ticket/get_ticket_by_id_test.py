"""Tests for `get_ticket_by_id()` in Office Hours Ticket Service."""

import pytest

from .....models.office_hours.ticket import OfficeHoursTicketPartial
from .....models.office_hours.ticket_details import OfficeHoursTicketDetails
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


def test_get_ticket_by_id_student_creator(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to validate getting a ticket by ID returns correct ticket details."""
    ticket = oh_ticket_svc.get_ticket_by_id(
        user__comp110_student_0, office_hours_data.comp110_called_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.comp110_called_ticket.id
    assert ticket.state == office_hours_data.comp110_called_ticket.state


def test_get_ticket_by_id_for_section_uta(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to validate getting a ticket by ID for section UTA returns ticket correct ticket details."""
    ticket = oh_ticket_svc.get_ticket_by_id(
        user__comp110_uta_0, office_hours_data.comp110_queued_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.comp110_queued_ticket.id


def test_get_ticket_by_id_for_section_instructor(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate getting a ticket by ID for section Instructor returns ticket correct ticket details."""
    ticket = oh_ticket_svc.get_ticket_by_id(
        user__comp110_instructor, office_hours_data.comp110_queued_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.comp110_queued_ticket.id


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
            user__comp110_student_1, office_hours_data.comp110_queued_ticket.id
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_get_ticket_by_id_exception_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to validate a PermissionError exception is raised when a non-section member tries to retrieve a ticket."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.get_ticket_by_id(
            user__comp110_non_member, office_hours_data.comp110_queued_ticket.id
        )
        pytest.fail()  # Fail test if no error was thrown above
