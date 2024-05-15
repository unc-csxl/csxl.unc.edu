"""Tests for `get_current_events_by_section()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.event import OfficeHoursEvent

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
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_uta_0,
    user__comp301_instructor,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_current_events_by_section_by_uta(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving current events by section for a UTA."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_current_events_by_section(
        user__comp110_uta_0, oh_section
    )

    assert isinstance(events[0], OfficeHoursEvent)
    assert len(events) == len(office_hours_data.comp110_oh_current_events)
    assert events[0].id == office_hours_data.comp_110_current_oh_event.id


def test_get_current_events_by_section_by_instructor(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving current events by section for an instructor."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_instructor, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_current_events_by_section(
        user__comp110_instructor, oh_section
    )

    assert isinstance(events[0], OfficeHoursEvent)
    assert len(events) == len(office_hours_data.comp110_oh_current_events)
    assert events[0].id == office_hours_data.comp_110_current_oh_event.id


def test_get_current_events_by_section_by_student(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving current events by section for an student."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_instructor, office_hours_data.comp_110_oh_section.id
    )
    events = oh_section_svc.get_current_events_by_section(
        user__comp110_instructor, oh_section
    )

    assert isinstance(events[0], OfficeHoursEvent)
    assert len(events) == len(office_hours_data.comp110_oh_current_events)
    assert events[0].id == office_hours_data.comp_110_current_oh_event.id


def test_get_current_events_by_section_exception_if_non_member(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for raising an exception when a non-member tries to retrieve current events."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_non_member, office_hours_data.comp_110_oh_section.id
    )
    with pytest.raises(PermissionError):
        oh_section_svc.get_current_events_by_section(
            user__comp110_non_member, oh_section
        )
        pytest.fail()
