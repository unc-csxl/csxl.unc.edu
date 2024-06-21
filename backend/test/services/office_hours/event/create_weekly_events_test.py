"""Tests for `create_weekly_events()` in Office Hours Event Service."""

import pytest
from datetime import datetime, date

from .....models.office_hours.office_hours import (
    OfficeHoursEvent,
    OfficeHoursEventRecurringDraft,
    Weekday,
)

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


def test_create_weekly_events(oh_event_svc: OfficeHoursEventService):
    """Test creation of weekly events."""
    start_date = date(2024, 4, 29)
    end_date = date(2024, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=start_date,
        recurring_end_date=end_date,
        selected_week_days=[Weekday.Monday],
    )

    events = oh_event_svc.create_weekly_events(user__comp110_instructor, draft)

    assert len(events) == 2
    assert isinstance(events[0], OfficeHoursEvent)

    assert events[0].start_time.hour == events[1].start_time.hour
    assert events[0].start_time.minute == events[1].start_time.minute

    assert events[0].end_time.hour == events[1].end_time.hour
    assert events[0].end_time.minute == events[1].end_time.minute

    assert events[0].event_date != events[1].event_date

    for event in events:
        assert event.event_date.strftime("%A").lower() == Weekday.Monday.name.lower()


def test_create_weekly_events_multiple_days(oh_event_svc: OfficeHoursEventService):
    """Test creation of weekly events on multiple days."""
    start_date = date(2024, 4, 29)
    end_date = date(2024, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=start_date,
        recurring_end_date=end_date,
        selected_week_days=[Weekday.Monday, Weekday.Tuesday, Weekday.Friday],
    )

    events = oh_event_svc.create_weekly_events(user__comp110_instructor, draft)

    assert len(events) == 6
    assert isinstance(events[0], OfficeHoursEvent)

    assert events[0].start_time.hour == events[1].start_time.hour
    assert events[0].start_time.minute == events[1].start_time.minute

    assert events[0].end_time.hour == events[1].end_time.hour
    assert events[0].end_time.minute == events[1].end_time.minute

    assert events[0].event_date != events[1].event_date

    for event in events:
        assert event.event_date.strftime("%A").lower() in (
            [
                Weekday.Monday.name.lower(),
                Weekday.Tuesday.name.lower(),
                Weekday.Friday.name.lower(),
            ]
        )


def test_create_weekly_events_exception_if_student(
    oh_event_svc: OfficeHoursEventService,
):
    """Test exception if a student tries to create weekly events."""
    start_date = date(2024, 4, 29)
    end_date = date(2024, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=start_date,
        recurring_end_date=end_date,
        selected_week_days=[Weekday.Monday, Weekday.Tuesday, Weekday.Friday],
    )

    with pytest.raises(PermissionError):
        oh_event_svc.create_weekly_events(user__comp110_student_0, draft)
        pytest.fail()


def test_create_weekly_events_exception_if_end_date_before_start_date(
    oh_event_svc: OfficeHoursEventService,
):
    """Test exception if end date is before start date."""
    start_date = date(2024, 4, 29)
    end_date = date(2024, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=end_date,
        recurring_end_date=start_date,
        selected_week_days=[Weekday.Monday, Weekday.Tuesday, Weekday.Friday],
    )

    with pytest.raises(Exception):
        oh_event_svc.create_weekly_events(user__comp110_instructor, draft)
        pytest.fail()


def test_create_weekly_events_exception_if_date_range_more_sixteen_weeks(
    oh_event_svc: OfficeHoursEventService,
):
    """Test exception if date range is more than sixteen weeks."""
    start_date = date(2024, 4, 29)
    end_date = date(2025, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=start_date,
        recurring_end_date=end_date,
        selected_week_days=[Weekday.Monday, Weekday.Tuesday, Weekday.Friday],
    )

    with pytest.raises(Exception):
        oh_event_svc.create_weekly_events(user__comp110_instructor, draft)
        pytest.fail()


def test_create_weekly_events_exception_if_no_selected_days(
    oh_event_svc: OfficeHoursEventService,
):
    """Test exception if no selected days."""
    start_date = date(2024, 4, 29)
    end_date = date(2025, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=start_date,
        recurring_end_date=end_date,
        selected_week_days=[],
    )

    with pytest.raises(Exception):
        oh_event_svc.create_weekly_events(user__comp110_instructor, draft)
        pytest.fail()


def test_create_weekly_events_exception_if_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test exception if non-member tries to create weekly events."""
    start_date = date(2024, 4, 29)
    end_date = date(2025, 5, 12)

    draft = OfficeHoursEventRecurringDraft(
        draft=office_hours_data.comp110_event_draft,
        recurring_start_date=start_date,
        recurring_end_date=end_date,
        selected_week_days=[],
    )

    with pytest.raises(PermissionError):
        oh_event_svc.create_weekly_events(user__comp110_non_member, draft)
        pytest.fail()
