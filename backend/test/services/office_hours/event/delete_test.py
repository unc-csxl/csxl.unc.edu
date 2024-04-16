"""Tests for `delete()` in Office Hours Event Service."""

import pytest

from .....services.exceptions import ResourceNotFoundException

from .....services.office_hours.event import OfficeHoursEventService

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


def test_delete_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be deleted by a UTA."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_past_oh_event_0.id
    )

    oh_event_svc.delete(user__comp110_uta_0, oh_event)

    # Check If Event Is Deleted
    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.get_event_by_id(
            user__comp110_uta_0, office_hours_data.comp_110_past_oh_event_0.id
        )


def test_delete_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an OfficeHoursEvent can be deleted by a instructor."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, office_hours_data.comp_110_past_oh_event_0.id
    )

    oh_event_svc.delete(user__comp110_instructor, oh_event)

    # Check If Event Is Deleted
    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.get_event_by_id(
            user__comp110_instructor, office_hours_data.comp_110_past_oh_event_0.id
        )


def test_delete_exception_if_student(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an exception is raised if a student attempts to delete OH event."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_student_0, office_hours_data.comp_110_past_oh_event_0.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.delete(user__comp110_student_0, oh_event)


def test_delete_exception_if_non_member(oh_event_svc: OfficeHoursEventService):
    """Test case to ensure an exception is raised if a non-member attempts to delete OH event."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_non_member, office_hours_data.comp_110_past_oh_event_0.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.delete(user__comp110_non_member, oh_event)
        pytest.fail()


def test_delete_exception_if_existing_ticket_data(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to ensure an exception is raised if OH event to be deleted has ticket data."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_non_member, office_hours_data.comp_110_current_oh_event.id
    )

    with pytest.raises(Exception):
        oh_event_svc.delete(user__comp110_uta_0, oh_event)
        pytest.fail()
