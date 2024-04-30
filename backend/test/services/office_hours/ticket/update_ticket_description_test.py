"""Tests for `update_description()` in Office Hours Ticket Service."""

import pytest

from .....models.office_hours.ticket import OfficeHoursTicketPartial
from .....models.office_hours.ticket_details import OfficeHoursTicket

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


def test_update_ticket_description(oh_ticket_svc: OfficeHoursTicketService):
    """Test case to update the description of an office hours ticket."""
    updated_description = "New Description"
    target_ticket = office_hours_data.comp110_queued_ticket

    delta = OfficeHoursTicketPartial(
        id=target_ticket.id, description=updated_description
    )

    # Check Original
    ticket = oh_ticket_svc.get_ticket_by_id(user__comp110_student_0, target_ticket.id)
    assert ticket is not None
    assert ticket.description != updated_description

    # Update
    updated_ticket = oh_ticket_svc.update_ticket_description(
        user__comp110_student_0, delta
    )

    assert isinstance(updated_ticket, OfficeHoursTicket)
    assert updated_ticket.description == updated_description

    # Verify
    ticket = oh_ticket_svc.get_ticket_by_id(user__comp110_student_0, target_ticket.id)
    assert ticket is not None
    assert ticket.description == updated_description


def test_update_ticket_description_exception_not_creator(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to check if updating a ticket description raises an exception when attempted by a non-creator."""
    updated_description = "New Description"
    target_ticket = office_hours_data.comp110_queued_ticket

    delta = OfficeHoursTicketPartial(
        id=target_ticket.id, description=updated_description
    )

    with pytest.raises(PermissionError):
        oh_ticket_svc.update_ticket_description(user__comp110_student_1, delta)
        pytest.fail()


def test_update_ticket_description_exception_if_ticket_not_queued(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to check if updating a ticket description raises an exception when the ticket is not in the queued state."""
    updated_description = "New Description"
    target_ticket = office_hours_data.comp110_called_ticket

    delta = OfficeHoursTicketPartial(
        id=target_ticket.id, description=updated_description
    )

    with pytest.raises(PermissionError):
        oh_ticket_svc.update_ticket_description(user__comp110_student_0, delta)
        pytest.fail()


def test_update_ticket_description_exception_invalid_ticket_id(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to check if updating a ticket description raises an exception for an invalid ticket ID."""
    updated_description = "New Description"

    delta = OfficeHoursTicketPartial(id=99, description=updated_description)

    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.update_ticket_description(user__comp110_student_0, delta)
        pytest.fail()


def test_update_ticket_description_exception_missing_description(
    oh_ticket_svc: OfficeHoursTicketService,
):
    """Test case to check if updating a ticket description raises an exception when description is missing."""
    delta = OfficeHoursTicketPartial(id=99, description=None)

    with pytest.raises(Exception):
        oh_ticket_svc.update_ticket_description(user__comp110_student_0, delta)
        pytest.fail()
