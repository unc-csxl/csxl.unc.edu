"""Tests for Office Hours Ticket Service."""

from unittest.mock import create_autospec
import pytest

from backend.models.office_hours.ticket_details import OfficeHoursTicketDetails
from backend.services.exceptions import ResourceNotFoundException
from ....services.office_hours import OfficeHoursTicketService

from .fixtures import permission_svc, oh_ticket_svc

# # Imported fixtures provide dependencies injected for the tests as parameters.
# from .fixtures import seat_svc

# # Import the setup_teardown fixture explicitly to load entities in database
# from ..room_data import fake_data_fixture as insert_room_fake_data
# from .seat_data import fake_data_fixture as insert_seat_fake_data

# # Import the fake model data in a namespace for test assertions
# from . import seat_data
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..room_data import fake_data_fixture as insert_order_1
from ..academics.term_data import fake_data_fixture as insert_order_2
from ..academics.course_data import fake_data_fixture as insert_order_3
from ..academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5


from .. import user_data
from . import office_hours_data

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_create_ticket(oh_ticket_svc: OfficeHoursTicketService):
    ticket = oh_ticket_svc.create(user_data.user, office_hours_data.draft_ticket)

    assert isinstance(ticket, OfficeHoursTicketDetails)


def test_create_ticket_exception_for_non_section_member(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.create(user_data.root, office_hours_data.draft_ticket)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_ticket_exception_for_cannot_find_event(
    oh_ticket_svc: OfficeHoursTicketService,
):
    with pytest.raises(ResourceNotFoundException):
        section = oh_ticket_svc.create(
            user_data.root, office_hours_data.draft_ticket_with_non_existing_event
        )
        pytest.fail()  # Fail test if no error was thrown above
    return
