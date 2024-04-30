"""Tests for `get_ticket_details_by_id()` in Office Hours Ticket Service."""

import pytest

from .....models.office_hours.ticket import OfficeHoursTicket
from .....models.office_hours.ticket_details import (
    OfficeHoursTicket,
    OfficeHoursTicketDetails,
)
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


def test_get_ticket_details_by_id_by_uta(oh_ticket_svc: OfficeHoursTicketService):
    """Test to get ticket details by ID as a UTA."""
    ticket = oh_ticket_svc.get_ticket_details_by_id(
        user__comp110_uta_0, office_hours_data.comp110_f23_called_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.comp110_f23_called_ticket.id
    assert ticket.state == office_hours_data.comp110_f23_called_ticket.state


def test_get_ticket_details_by_id_by_instructor(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test to get ticket details by ID as an instructor."""
    ticket = oh_ticket_svc.get_ticket_details_by_id(
        user__comp110_instructor, office_hours_data.comp110_closed_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.comp110_closed_ticket.id
    assert ticket.state == office_hours_data.comp110_closed_ticket.state


def test_get_ticket_details_by_id_by_gta(oh_ticket_svc: OfficeHoursTicketService):
    """Test to get ticket details by ID as a GTA."""
    ticket = oh_ticket_svc.get_ticket_details_by_id(
        user__comp110_gta, office_hours_data.comp110_closed_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.comp110_closed_ticket.id
    assert ticket.state == office_hours_data.comp110_closed_ticket.state


def test_get_ticket_details_by_id_exception_if_student(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test to check if getting ticket details by ID as a student raises an exception."""
    with pytest.raises(PermissionError):
        oh_ticket_svc.get_ticket_details_by_id(
            user__comp110_student_0, office_hours_data.comp110_closed_ticket.id
        )
        pytest.fail()


def test_get_ticket_details_by_id_exception_if_invalid_id(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test to check if getting ticket details by an invalid ID raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.get_ticket_details_by_id(user__comp110_student_0, 99)
        pytest.fail()
