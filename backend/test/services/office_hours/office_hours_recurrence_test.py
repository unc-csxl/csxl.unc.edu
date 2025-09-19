"""Tests for the OfficeHoursRecurrenceService."""

import pytest

from ....services.exceptions import (
    CoursePermissionException,
    RecurringOfficeHourEventException,
    ResourceNotFoundException,
)

from ....services.office_hours import OfficeHoursRecurrenceService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import oh_svc_mock, oh_recurrence_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..academics.course_data import fake_data_fixture as insert_order_1
from ..academics.section_data import fake_data_fixture as insert_order_2
from ..room_data import fake_data_fixture as insert_order_3
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_4

# Important fake model data in namespace for test assertions
from .. import user_data
from ..office_hours import office_hours_data

__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_create_recurring_oh_event_instructor(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that instructors can create recurring office hour events."""
    new_events = oh_recurrence_svc.create_recurring(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.new_event,
        office_hours_data.new_recurrence_pattern,
    )

    new_recurrence_pattern_array = [
        office_hours_data.new_recurrence_pattern.recur_monday,
        office_hours_data.new_recurrence_pattern.recur_tuesday,
        office_hours_data.new_recurrence_pattern.recur_wednesday,
        office_hours_data.new_recurrence_pattern.recur_thursday,
        office_hours_data.new_recurrence_pattern.recur_friday,
        office_hours_data.new_recurrence_pattern.recur_saturday,
        office_hours_data.new_recurrence_pattern.recur_sunday,
    ]
    new_recurrence_time_delta = (
        office_hours_data.new_recurrence_pattern.end_date
        - office_hours_data.new_recurrence_pattern.start_date
    )
    expected_new_events_length = 0
    for i in range(new_recurrence_time_delta.days + 1):
        if new_recurrence_pattern_array[i % len(new_recurrence_pattern_array)]:
            expected_new_events_length += 1

    assert len(new_events) == expected_new_events_length
    assert new_events[0].recurrence_pattern_id is not None


def test_create_recurring_oh_event_not_authenticated(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that users without the appropriate site permissions cannot create recurring office hour events."""
    with pytest.raises(CoursePermissionException):
        oh_recurrence_svc.create_recurring(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.new_event,
            office_hours_data.new_recurrence_pattern,
        )
        pytest.fail()


def test_create_recurring_oh_event_invalid_days_recur(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that an exception is thrown when recurrence pattern has no days selected."""
    with pytest.raises(RecurringOfficeHourEventException):
        oh_recurrence_svc.create_recurring(
            user_data.instructor,
            office_hours_data.comp_110_site.id,
            office_hours_data.new_event,
            office_hours_data.invalid_recurrence_pattern_days,
        )
        pytest.fail()


def test_create_recurring_oh_event_invalid_recurrence_end(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that an exception is thrown when recurrence pattern end date is earlier than first event."""
    with pytest.raises(RecurringOfficeHourEventException):
        oh_recurrence_svc.create_recurring(
            user_data.instructor,
            office_hours_data.comp_110_site.id,
            office_hours_data.new_event,
            office_hours_data.invalid_recurrence_pattern_end,
        )
        pytest.fail()


def test_update_recurring_oh_event_instructor(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that instructors can modify recurring office hours events."""
    modified_events = oh_recurrence_svc.update_recurring(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.first_recurring_event,
        office_hours_data.updated_recurrence_pattern,
    )

    updated_recurrence_pattern_array = [
        office_hours_data.updated_recurrence_pattern.recur_monday,
        office_hours_data.updated_recurrence_pattern.recur_tuesday,
        office_hours_data.updated_recurrence_pattern.recur_wednesday,
        office_hours_data.updated_recurrence_pattern.recur_thursday,
        office_hours_data.updated_recurrence_pattern.recur_friday,
        office_hours_data.updated_recurrence_pattern.recur_saturday,
        office_hours_data.updated_recurrence_pattern.recur_sunday,
    ]
    updated_recurrence_time_delta = (
        office_hours_data.updated_recurrence_pattern.end_date
        - office_hours_data.updated_recurrence_pattern.start_date
    )
    expected_modified_events_length = 0
    for i in range(updated_recurrence_time_delta.days + 1):
        if updated_recurrence_pattern_array[i % len(updated_recurrence_pattern_array)]:
            expected_modified_events_length += 1

    assert len(modified_events) == expected_modified_events_length
    assert modified_events[0].recurrence_pattern_id is not None


def test_delete_recurring_oh_event_instructor(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that instructors can delete recurring office hour events."""
    oh_recurrence_svc.delete_recurring(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.second_recurring_event.id,
    )


def test_delete_recurring_oh_event_not_found(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that an exception is thrown when an unknown OH event ID is provided."""
    with pytest.raises(ResourceNotFoundException):
        oh_recurrence_svc.delete_recurring(
            user_data.instructor,
            office_hours_data.comp_110_site.id,
            office_hours_data.seventh_recurring_event.id + 1,
        )
        pytest.fail()


def test_delete_recurring_oh_event_not_authorized(
    oh_recurrence_svc: OfficeHoursRecurrenceService,
):
    """Ensures that an unauthorized user cannot delete recurring events."""
    with pytest.raises(CoursePermissionException):
        oh_recurrence_svc.delete_recurring(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.second_recurring_event.id,
        )
        pytest.fail()
