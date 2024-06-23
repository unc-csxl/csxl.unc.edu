"""Tests for the OfficeHoursTicketService."""

import pytest

from ....models.academics.my_courses import OfficeHourTicketOverview

from ....models.office_hours.ticket import TicketState

from ....services.office_hours import OfficeHourTicketService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import oh_ticket_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..academics.term_data import fake_data_fixture as insert_order_1
from ..academics.course_data import fake_data_fixture as insert_order_2
from ..academics.section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import user_data
from ..office_hours import office_hours_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


# Call Ticket Tests


def test_call_ticket(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that instructors can call tickets."""
    called = oh_ticket_svc.call_ticket(
        user_data.instructor, office_hours_data.comp_110_queued_ticket.id
    )
    assert called.state == TicketState.CALLED.to_string()
    name = user_data.instructor.first_name + " " + user_data.instructor.last_name
    assert called.caller == name


def test_call_ticket_already_called(oh_ticket_svc: OfficeHourTicketService):
    """Ensures an error is thrown when a ticket has already been called."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(
            user_data.instructor, office_hours_data.comp_110_called_ticket.id
        )
        pytest.fail()


def test_call_ticket_not_queued(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that only queued tickets can be called."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(
            user_data.instructor, office_hours_data.comp_110_closed_ticket.id
        )
        oh_ticket_svc.call_ticket(
            user_data.instructor, office_hours_data.comp_110_cancelled_ticket.id
        )
        pytest.fail()


def test_call_ticket_not_found(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that an error is thrown if attempting to call a ticket that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.call_ticket(user_data.instructor, 404)
        pytest.fail()


def test_call_ticket_not_member(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that non-members cannot call tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(
            user_data.ambassador, office_hours_data.comp_110_queued_ticket.id
        )
        pytest.fail()


def test_call_ticket_not_staff(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that non-staff members cannot call tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(
            user_data.student, office_hours_data.comp_110_queued_ticket.id
        )
        pytest.fail()


# Cancel Ticket Tests


def test_cancel_ticket(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that instructors can cancel tickets."""
    called = oh_ticket_svc.cancel_ticket(
        user_data.instructor, office_hours_data.comp_110_queued_ticket.id
    )
    assert called.state == TicketState.CANCELED.to_string()


def test_cancel_ticket_not_found(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that an error is thrown if attempting to cancel a ticket that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.cancel_ticket(user_data.instructor, 404)
        pytest.fail()


def test_cancel_ticket_not_member(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that non-members cannot cancel tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.cancel_ticket(
            user_data.ambassador, office_hours_data.comp_110_queued_ticket.id
        )
        pytest.fail()


def test_cancel_ticket_student(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that students can cancel tickets."""
    called = oh_ticket_svc.cancel_ticket(
        user_data.student, office_hours_data.comp_110_queued_ticket.id
    )
    assert called.state == TicketState.CANCELED.to_string()


# Close Ticket Tests


def test_close_ticket(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that instructors can close tickets."""
    called = oh_ticket_svc.close_ticket(
        user_data.instructor, office_hours_data.comp_110_called_ticket.id
    )
    assert called.state == TicketState.CLOSED.to_string()


def test_close_ticket_not_called(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that only called tickets can be closed."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.close_ticket(
            user_data.instructor, office_hours_data.comp_110_queued_ticket.id
        )
        oh_ticket_svc.close_ticket(
            user_data.instructor, office_hours_data.comp_110_closed_ticket.id
        )
        oh_ticket_svc.close_ticket(
            user_data.instructor, office_hours_data.comp_110_cancelled_ticket.id
        )
        pytest.fail()


def test_close_ticket_not_found(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that an error is thrown if attempting to close a ticket that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.close_ticket(user_data.instructor, 404)
        pytest.fail()


def test_close_ticket_not_member(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that non-members cannot close tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.close_ticket(
            user_data.ambassador, office_hours_data.comp_110_called_ticket.id
        )
        pytest.fail()


def test_close_ticket_not_staff(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that non-staff members cannot close tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.close_ticket(
            user_data.student, office_hours_data.comp_110_called_ticket.id
        )
        pytest.fail()


def test_create_ticket(oh_ticket_svc: OfficeHourTicketService):
    """Ensurs that students can create new tickets."""
    created = oh_ticket_svc.create_ticket(user_data.user, office_hours_data.new_ticket)
    assert created is not None
    assert isinstance(created, OfficeHourTicketOverview)
    assert created.state == TicketState.QUEUED.to_string()


def test_create_ticket_with_one_in_queue(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that users can only create one ticket at a time."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(user_data.student, office_hours_data.new_ticket)
        pytest.fail()


def test_create_ticket_not_member(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that non-members cannot create tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(user_data.ambassador, office_hours_data.new_ticket)
        pytest.fail()


def test_create_ticket_not_student(oh_ticket_svc: OfficeHourTicketService):
    """Ensures that only students can create tickets."""
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(user_data.instructor, office_hours_data.new_ticket)
        pytest.fail()
