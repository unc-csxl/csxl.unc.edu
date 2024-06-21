"""Tests for `get_event_tickets()` in Office Hours Event Service."""

import pytest

from .....models.office_hours.ticket_details import OfficeHoursTicketDetails

from .....services.office_hours.office_hours import OfficeHoursEventService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_event_svc

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
    user__comp110_uta_0,
    user__comp110_non_member,
)


__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"
license__ = "MIT"


def test_get_event_tickets_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure fetching event tickets by UTAs, verifying type and count."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_current_oh_event.id
    )
    event_tickets = oh_event_svc.get_event_tickets(user__comp110_uta_0, oh_event)

    assert isinstance(event_tickets[0], OfficeHoursTicketDetails)
    assert len(event_tickets) == len(office_hours_data.comp110_current_term_tickets)


def test_get_event_tickets_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure fetching event tickets by instructors, verifying type and count."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, office_hours_data.comp_110_current_oh_event.id
    )
    event_tickets = oh_event_svc.get_event_tickets(user__comp110_instructor, oh_event)

    assert isinstance(event_tickets[0], OfficeHoursTicketDetails)
    assert len(event_tickets) == len(office_hours_data.comp110_current_term_tickets)


def test_get_event_tickets_exception_if_student(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure a PermissionError is raised when a student attempts to access event tickets."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_current_oh_event.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.get_event_tickets(user__comp110_student_0, oh_event)
        pytest.fail()


def test_get_event_tickets_exception_if_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure a PermissionError is raised when a non-member attempts to access event tickets."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_current_oh_event.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.get_event_tickets(user__comp110_non_member, oh_event)
        pytest.fail()
