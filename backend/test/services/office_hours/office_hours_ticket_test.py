"""Tests for Courses Section Service."""

from unittest.mock import create_autospec
import pytest
from backend.models.office_hours.ticket_details import OfficeHoursTicketDetails
from backend.models.office_hours.ticket_state import TicketState
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.office_hours.ticket import OfficeHoursTicketService
from backend.services.permission import PermissionService


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
from .. import user_data
from ..academics import section_data


# TODO: Add Comments
def test_create_ticket(oh_ticket_svc: OfficeHoursTicketService):
    ticket = oh_ticket_svc.create(user_data.user, office_hours_data.ticket_draft)
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.QUEUED


def test_create_ticket_group(oh_ticket_svc: OfficeHoursTicketService):
    ticket = oh_ticket_svc.create(user_data.user, office_hours_data.group_ticket_draft)
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.state == TicketState.QUEUED


def test_create_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(user_data.root, office_hours_data.ticket_draft)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_for_non_section_member_group_ticket(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(
            user_data.root, office_hours_data.group_ticket_draft_non_member
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_invalid_event(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.create(
            user_data.root, office_hours_data.ticket_draft_invalid_event
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_get_ticket_by_id(oh_ticket_svc: OfficeHoursTicketService):
    ticket = oh_ticket_svc.get_ticket_by_id(
        user_data.user, office_hours_data.called_ticket.id
    )
    assert isinstance(ticket, OfficeHoursTicketDetails)
    assert ticket.id == office_hours_data.called_ticket.id


def test_get_ticket_by_id_exception_when_id_does_not_exist(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.get_ticket_by_id(user_data.user, 10)
        pytest.fail()  # Fail test if no error was thrown above
