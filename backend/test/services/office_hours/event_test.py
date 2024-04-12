"""Tests for Office Hours Event Service."""

import pytest

from ....models.office_hours.ticket_details import OfficeHoursTicketDetails
from ....models.office_hours.event import OfficeHoursEvent
from ....models.office_hours.event_status import (
    OfficeHoursEventStatus,
    StudentOfficeHoursEventStatus,
)

from ....services.exceptions import ResourceNotFoundException
from ....services.office_hours.event import OfficeHoursEventService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, oh_event_svc

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
    user__comp110_uta_0,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_create_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be created by a UTA."""
    oh_event = oh_event_svc.create(
        user__comp110_uta_0, office_hours_data.comp110_event_draft
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.description == office_hours_data.comp110_event_draft.description


def test_create_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be created by an instructor."""
    oh_event = oh_event_svc.create(
        user__comp110_instructor, office_hours_data.comp110_event_draft
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.description == office_hours_data.comp110_event_draft.description


def test_create_exception_if_student(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an exception is raised when a student tries to create an OfficeHoursEvent."""
    with pytest.raises(PermissionError):
        oh_event_svc.create(
            user__comp110_student_0, office_hours_data.comp110_event_draft
        )
        pytest.fail(
            "Expected PermissionError was not raised."
        )  # Fail test if no error was thrown above


def test_create_exception_if_non_member(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an exception is raised when a non-member tries to create an OfficeHoursEvent."""
    with pytest.raises(PermissionError):
        oh_event_svc.create(
            user__comp110_non_member, office_hours_data.comp110_event_draft
        )
        pytest.fail(
            "Expected PermissionError was not raised."
        )  # Fail test if no error was thrown above


def test_get_event_by_id(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be retrieved by its ID."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )
    assert isinstance(oh_event, OfficeHoursEvent)
    assert oh_event.id == office_hours_data.comp_110_oh_event_1.id


def test_get_event_by_id_exception_non_existing_event(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when retrieving a non-existing OfficeHoursEvent by ID."""
    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.get_event_by_id(user__comp110_student_0, 99)
        pytest.fail()  # Fail test if no error was thrown above


def test_get_queued_and_called_oh_tickets_by_event_by_student(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure queued and called OfficeHoursTickets can be retrieved by event for a student."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_student_0, 1)
    status: OfficeHoursEventStatus = oh_event_svc.get_queued_helped_stats_by_oh_event(
        user__comp110_student_0, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 1
    assert status.queued_tickets_count == 1


def test_get_queued_and_called_oh_tickets_by_event_by_uta(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure queued and called OfficeHoursTickets can be retrieved by event for a UTA."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, 1)
    status: OfficeHoursEventStatus = oh_event_svc.get_queued_helped_stats_by_oh_event(
        user__comp110_uta_0, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 1
    assert status.queued_tickets_count == 1


def test_get_queued_and_called_oh_tickets_by_event_by_instructor(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure queued and called OfficeHoursTickets can be retrieved by event for an instructor."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_instructor, 1)
    status: OfficeHoursEventStatus = oh_event_svc.get_queued_helped_stats_by_oh_event(
        user__comp110_instructor, oh_event
    )
    assert isinstance(status, OfficeHoursEventStatus)
    assert status.open_tickets_count == 1
    assert status.queued_tickets_count == 1


def test_get_queued_and_called_oh_tickets_by_event_exception_for_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when non-member tries to retrieve queued/called OfficeHoursTickets by event."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_non_member, 1)
    with pytest.raises(PermissionError):
        oh_event_svc.get_queued_helped_stats_by_oh_event(
            user__comp110_non_member, oh_event
        )
        pytest.fail()  # Fail test if no error was thrown above


def test_get_queued_and_called_tickets_by_event(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure correct ordering and length of queued and called tickets for an event."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, 1)
    event_tickets = oh_event_svc.get_queued_and_called_tickets_by_event(
        user__comp110_uta_0, oh_event
    )

    assert isinstance(event_tickets[0], OfficeHoursTicketDetails)
    assert len(event_tickets) == 2
    assert event_tickets[0].created_at < event_tickets[1].created_at


def test_get_queued_and_called_tickets_by_event_exception_if_student(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure a PermissionError is raised when a student attempts to access queued/called tickets."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, 1)

    with pytest.raises(PermissionError):
        oh_event_svc.get_queued_and_called_tickets_by_event(
            user__comp110_student_0, oh_event
        )
        pytest.fail()


def test_get_queued_and_called_tickets_by_event_exception_if_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure a PermissionError is raised when a non-member attempts to access queued/called tickets."""
    oh_event = oh_event_svc.get_event_by_id(user__comp110_non_member, 1)

    with pytest.raises(PermissionError):
        oh_event_svc.get_queued_and_called_tickets_by_event(
            user__comp110_non_member, oh_event
        )
        pytest.fail()


def test_get_event_tickets_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure fetching event tickets by UTAs, verifying type and count."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_event_1.id
    )
    event_tickets = oh_event_svc.get_event_tickets(user__comp110_uta_0, oh_event)

    assert isinstance(event_tickets[0], OfficeHoursTicketDetails)
    assert len(event_tickets) == 4


def test_get_event_tickets_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure fetching event tickets by instructors, verifying type and count."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, office_hours_data.comp_110_oh_event_1.id
    )
    event_tickets = oh_event_svc.get_event_tickets(user__comp110_instructor, oh_event)

    assert isinstance(event_tickets[0], OfficeHoursTicketDetails)
    assert len(event_tickets) == 4


def test_get_event_tickets_exception_if_student(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure a PermissionError is raised when a student attempts to access event tickets."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.get_event_tickets(user__comp110_student_0, oh_event)


def test_get_event_tickets_exception_if_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure a PermissionError is raised when a non-member attempts to access event tickets."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.get_event_tickets(user__comp110_non_member, oh_event)


def test_get_queued_helped_stats_by_oh_event_for_student(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure fetching queued and helped stats for an event by a student."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )
    student_ticket_status = (
        oh_event_svc.get_queued_helped_stats_by_oh_event_for_student(
            user__comp110_student_0,
            oh_event,
            office_hours_data.comp110_queued_ticket.id,
        )
    )

    assert isinstance(student_ticket_status, StudentOfficeHoursEventStatus)
    assert student_ticket_status.queued_tickets_count == 1
    assert student_ticket_status.ticket_position == 1


def test_get_queued_helped_stats_by_oh_event_for_student_exception_invalid_ticket_id(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure a ResourceNotFoundException is raised for an invalid ticket ID."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )

    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.get_queued_helped_stats_by_oh_event_for_student(
            user__comp110_student_0, oh_event, 99
        )


def test_get_queued_helped_stats_by_oh_event_for_student_exception_ticket_not_in_event(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when the ticket does not belong to the specified event."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )

    with pytest.raises(Exception):
        oh_event_svc.get_queued_helped_stats_by_oh_event_for_student(
            user__comp110_student_0, oh_event, office_hours_data.comp_523_pending_ticket
        )


def test_get_queued_helped_stats_by_oh_event_for_student_exception_ticket_not_queued(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised when attempting to get stats for a ticket not in the queued state."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_event_1.id
    )

    with pytest.raises(Exception):
        oh_event_svc.get_queued_helped_stats_by_oh_event_for_student(
            user__comp110_student_0,
            oh_event,
            office_hours_data.comp110_called_ticket.id,
        )
