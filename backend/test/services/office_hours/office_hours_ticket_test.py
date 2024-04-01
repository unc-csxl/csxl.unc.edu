"""Tests for Office Hours Ticket Service."""

from unittest.mock import create_autospec
import pytest

from ....models.office_hours.ticket_details import OfficeHoursTicketDetails
from ....services.exceptions import ResourceNotFoundException
from ....services.office_hours import OfficeHoursTicketService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, oh_ticket_svc


# # Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..room_data import fake_data_fixture as insert_order_1
from ..academics.term_data import fake_data_fixture as insert_order_2
from ..academics.course_data import fake_data_fixture as insert_order_3
from ..academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import user_data
from . import office_hours_data

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


# TODO: Add Comments
def test_create_ticket(oh_ticket_svc: OfficeHoursTicketService):
    ticket = oh_ticket_svc.create(user_data.user, office_hours_data.draft_ticket)
    assert isinstance(ticket, OfficeHoursTicketDetails)


def test_create_ticket_group_creators(oh_ticket_svc: OfficeHoursTicketService):

    # Add Section Member

    ticket = oh_ticket_svc.create(user_data.user, office_hours_data.draft_ticket_group)

    assert isinstance(ticket, OfficeHoursTicketDetails)
    return


def test_create_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(PermissionError):
        oh_ticket_svc.create(user_data.root, office_hours_data.draft_ticket)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_for_cannot_find_event(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.create(
            user_data.root, office_hours_data.draft_ticket_with_non_existing_event
        )
        pytest.fail()  # Fail test if no error was thrown above
    return


# TODO: Check If User Is Added To Table
