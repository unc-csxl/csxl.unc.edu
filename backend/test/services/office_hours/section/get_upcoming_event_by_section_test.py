"""Tests for `get_upcoming_event_by_section()` in Office Hours Section Service."""

from datetime import datetime, timedelta
import pytest

from .....models.coworking.time_range import TimeRange
from .....models.office_hours.office_hours import OfficeHoursEvent

from .....services.office_hours.section import OfficeHoursSectionService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_section_svc

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
    user__comp110_uta_0,
    user__comp301_instructor,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_upcoming_events_by_section_by_uta(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving upcoming events by section for a UTA within a specified time range."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_upcoming_events_by_section(
        user__comp110_uta_0,
        oh_section,
        TimeRange(start=datetime.now(), end=datetime.now() + timedelta(days=7)),
    )

    assert isinstance(events[0], OfficeHoursEvent)
    assert len(events) == len(office_hours_data.comp110_oh_upcoming_events)
    assert events[0].id == office_hours_data.comp_110_upcoming_oh_event.id


def test_get_upcoming_events_by_section_by_instructor(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving upcoming events by section for an instructor within a specified time range."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_upcoming_events_by_section(
        user__comp110_uta_0,
        oh_section,
        TimeRange(start=datetime.now(), end=datetime.now() + timedelta(days=7)),
    )

    assert isinstance(events[0], OfficeHoursEvent)
    assert len(events) == len(office_hours_data.comp110_oh_upcoming_events)
    assert events[0].id == office_hours_data.comp_110_upcoming_oh_event.id


def test_get_upcoming_events_by_section_by_student(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving upcoming events by section for a student within a specified time range."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_upcoming_events_by_section(
        user__comp110_uta_0,
        oh_section,
        TimeRange(start=datetime.now(), end=datetime.now() + timedelta(days=7)),
    )

    assert isinstance(events[0], OfficeHoursEvent)
    assert len(events) == len(office_hours_data.comp110_oh_upcoming_events)
    assert events[0].id == office_hours_data.comp_110_upcoming_oh_event.id


def test_get_upcoming_events_by_section_small_time_range(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving upcoming events by section within a very short time range (no events expected)."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_upcoming_events_by_section(
        user__comp110_uta_0,
        oh_section,
        TimeRange(start=datetime.now(), end=datetime.now() + timedelta(hours=5)),
    )

    assert len(events) == 0


def test_get_upcoming_events_by_section_exception_if_non_member(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for raising an exception when a non-member tries to retrieve upcoming events."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_non_member, office_hours_data.comp_110_oh_section.id
    )
    with pytest.raises(PermissionError):
        oh_section_svc.get_upcoming_events_by_section(
            user__comp110_non_member,
            oh_section,
            TimeRange(start=datetime.now(), end=datetime.now() + timedelta(days=7)),
        )
        pytest.fail()
