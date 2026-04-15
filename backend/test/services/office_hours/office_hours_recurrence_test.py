"""Tests for the OfficeHoursRecurrenceService."""

from datetime import datetime, timedelta
from unittest.mock import create_autospec

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from ....entities.academics.term_entity import TermEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....entities.office_hours.office_hours_recurrence_pattern_entity import (
    OfficeHoursRecurrencePatternEntity,
)
from ....entities.room_entity import RoomEntity
from ....models import RoomDetails, User
from ....models.academics.term import Term
from ....models.office_hours.course_site import CourseSite
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.office_hours import NewOfficeHours, OfficeHours
from ....models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
)
from ....services.exceptions import (
    CoursePermissionException,
    RecurringOfficeHourEventException,
    ResourceNotFoundException,
)
from ....services.office_hours import OfficeHoursRecurrenceService, OfficeHoursService

__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def make_subject(user_id: int, onyen: str) -> User:
    return User(id=user_id, pid=user_id, onyen=onyen)


def arrange_course_site(session: Session) -> tuple[CourseSite, RoomDetails]:
    term = Term(
        id="F26",
        name="Fall 2026",
        start=datetime(2026, 8, 17, 0, 0),
        end=datetime(2026, 12, 15, 23, 59),
    )
    room = RoomDetails(
        id="SN135",
        building="Sitterson",
        room="135",
        nickname="Group A",
        capacity=4,
        reservable=True,
        seats=[],
    )
    site = CourseSite(id=1, title="COMP 110", term_id=term.id)

    session.add(TermEntity.from_model(term))
    session.add(RoomEntity.from_model(room))
    session.add(CourseSiteEntity.from_model(site))
    session.commit()

    return site, room


def make_new_event(
    site_id: int,
    room_id: str,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> NewOfficeHours:
    start = start_time or datetime(2026, 4, 20, 13, 0)
    end = end_time or start + timedelta(hours=1)
    return NewOfficeHours(
        type=OfficeHoursEventType.OFFICE_HOURS,
        mode=OfficeHoursEventModeType.IN_PERSON,
        description="Sample",
        location_description="Sample",
        start_time=start,
        end_time=end,
        course_site_id=site_id,
        room_id=room_id,
        recurrence_pattern_id=None,
    )


def make_recurrence_pattern(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    *,
    recur_monday: bool = True,
    recur_tuesday: bool = True,
    recur_wednesday: bool = True,
    recur_thursday: bool = True,
    recur_friday: bool = True,
    recur_saturday: bool = True,
    recur_sunday: bool = True,
) -> NewOfficeHoursRecurrencePattern:
    start = start_date or datetime(2026, 4, 20, 0, 0)
    end = end_date or start + timedelta(days=14)
    return NewOfficeHoursRecurrencePattern(
        start_date=start,
        end_date=end,
        recur_monday=recur_monday,
        recur_tuesday=recur_tuesday,
        recur_wednesday=recur_wednesday,
        recur_thursday=recur_thursday,
        recur_friday=recur_friday,
        recur_saturday=recur_saturday,
        recur_sunday=recur_sunday,
    )


def test_create_recurring_requires_matching_days(session: Session):
    site, room = arrange_course_site(session)
    office_hours_svc = create_autospec(OfficeHoursService)
    service = OfficeHoursRecurrenceService(session, office_hours_svc)

    with pytest.raises(RecurringOfficeHourEventException):
        service.create_events(
            make_new_event(site.id, room.id),
            make_recurrence_pattern(
                start_date=datetime(2026, 4, 21, 0, 0),
                end_date=datetime(2026, 4, 21, 23, 59),
                recur_monday=True,
                recur_tuesday=False,
                recur_wednesday=False,
                recur_thursday=False,
                recur_friday=False,
                recur_saturday=False,
                recur_sunday=False,
            ),
        )
        pytest.fail()


def expected_event_count(pattern: NewOfficeHoursRecurrencePattern) -> int:
    count = 0
    current_date = pattern.start_date
    recurrence_by_weekday = [
        pattern.recur_monday,
        pattern.recur_tuesday,
        pattern.recur_wednesday,
        pattern.recur_thursday,
        pattern.recur_friday,
        pattern.recur_saturday,
        pattern.recur_sunday,
    ]

    while current_date <= pattern.end_date:
        if recurrence_by_weekday[current_date.weekday()]:
            count += 1
        current_date += timedelta(days=1)

    return count


def make_service(
    session: Session,
    permission_error: Exception | None = None,
) -> tuple[OfficeHoursRecurrenceService, OfficeHoursService]:
    office_hours_svc = create_autospec(OfficeHoursService)
    if permission_error is not None:
        office_hours_svc._check_site_admin_permissions.side_effect = permission_error

    return OfficeHoursRecurrenceService(session, office_hours_svc), office_hours_svc


def arrange_existing_recurring_events(
    session: Session,
    site_id: int,
    room_id: str,
) -> list[OfficeHours]:
    pattern = make_recurrence_pattern(end_date=datetime(2026, 4, 26, 0, 0))
    pattern_entity = OfficeHoursRecurrencePatternEntity.from_new_model(pattern)
    session.add(pattern_entity)
    session.flush()

    base_start = datetime(2026, 4, 20, 13, 0)
    events = [
        OfficeHours(
            id=1,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Recurring OH",
            location_description="Sitterson",
            start_time=base_start,
            end_time=base_start + timedelta(hours=1),
            course_site_id=site_id,
            room_id=room_id,
            recurrence_pattern_id=pattern_entity.id,
        ),
        OfficeHours(
            id=2,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Recurring OH",
            location_description="Sitterson",
            start_time=base_start + timedelta(days=1),
            end_time=base_start + timedelta(days=1, hours=1),
            course_site_id=site_id,
            room_id=room_id,
            recurrence_pattern_id=pattern_entity.id,
        ),
        OfficeHours(
            id=3,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Recurring OH",
            location_description="Sitterson",
            start_time=base_start + timedelta(days=2),
            end_time=base_start + timedelta(days=2, hours=1),
            course_site_id=site_id,
            room_id=room_id,
            recurrence_pattern_id=pattern_entity.id,
        ),
    ]

    session.add_all(OfficeHoursEntity.from_model(event) for event in events)
    session.commit()

    return events


def test_create_recurring_oh_event_instructor(
    session: Session,
):
    """Ensures that instructors can create recurring office hour events."""
    # Arrange
    site, room = arrange_course_site(session)
    instructor = make_subject(1, "instructor")
    event = make_new_event(site.id, room.id)
    recurrence_pattern = make_recurrence_pattern()
    oh_recurrence_svc, office_hours_svc = make_service(session)

    # Act
    new_events = oh_recurrence_svc.create_recurring(
        instructor,
        site.id,
        event,
        recurrence_pattern,
    )

    # Assert
    assert len(new_events) == expected_event_count(recurrence_pattern)
    assert new_events[0].recurrence_pattern_id is not None
    office_hours_svc._check_site_admin_permissions.assert_called_once_with(
        instructor, site.id
    )


def test_create_recurring_oh_event_not_authenticated(
    session: Session,
):
    """Ensures that users without the appropriate site permissions cannot create recurring office hour events."""
    # Arrange
    site, room = arrange_course_site(session)
    unauthorized_user = make_subject(2, "root")
    event = make_new_event(site.id, room.id)
    recurrence_pattern = make_recurrence_pattern()
    oh_recurrence_svc, _ = make_service(
        session, CoursePermissionException("Not authorized")
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_recurrence_svc.create_recurring(
            unauthorized_user,
            site.id,
            event,
            recurrence_pattern,
        )


def test_create_recurring_oh_event_invalid_days_recur(
    session: Session,
):
    """Ensures that an exception is thrown when recurrence pattern has no days selected."""
    # Arrange
    site, room = arrange_course_site(session)
    instructor = make_subject(1, "instructor")
    event = make_new_event(site.id, room.id)
    oh_recurrence_svc, _ = make_service(session)

    # Act / Assert
    with pytest.raises(RecurringOfficeHourEventException):
        oh_recurrence_svc.create_recurring(
            instructor,
            site.id,
            event,
            make_recurrence_pattern(
                recur_monday=False,
                recur_tuesday=False,
                recur_wednesday=False,
                recur_thursday=False,
                recur_friday=False,
                recur_saturday=False,
                recur_sunday=False,
            ),
        )


def test_create_recurring_oh_event_invalid_recurrence_end(
    session: Session,
):
    """Ensures that an exception is thrown when recurrence pattern end date is earlier than first event."""
    # Arrange
    site, room = arrange_course_site(session)
    instructor = make_subject(1, "instructor")
    event = make_new_event(site.id, room.id)
    oh_recurrence_svc, _ = make_service(session)

    # Act / Assert
    with pytest.raises(RecurringOfficeHourEventException):
        oh_recurrence_svc.create_recurring(
            instructor,
            site.id,
            event,
            make_recurrence_pattern(
                start_date=event.start_time - timedelta(days=14),
                end_date=event.start_time - timedelta(days=13),
                recur_monday=True,
                recur_tuesday=False,
                recur_wednesday=False,
                recur_thursday=False,
                recur_friday=False,
                recur_saturday=False,
                recur_sunday=False,
            ),
        )


def test_update_recurring_oh_event_instructor(
    session: Session,
):
    """Ensures that instructors can modify recurring office hours events."""
    # Arrange
    site, room = arrange_course_site(session)
    instructor = make_subject(1, "instructor")
    existing_events = arrange_existing_recurring_events(session, site.id, room.id)
    updated_recurrence_pattern = make_recurrence_pattern(
        recur_tuesday=False,
        recur_thursday=False,
    )
    oh_recurrence_svc, office_hours_svc = make_service(session)

    # Act
    modified_events = oh_recurrence_svc.update_recurring(
        instructor,
        site.id,
        existing_events[0],
        updated_recurrence_pattern,
    )

    # Assert
    assert len(modified_events) == expected_event_count(updated_recurrence_pattern)
    assert modified_events[0].recurrence_pattern_id is not None
    office_hours_svc._check_site_admin_permissions.assert_called_once_with(
        instructor, site.id
    )


def test_delete_recurring_oh_event_instructor(
    session: Session,
):
    """Ensures that instructors can delete recurring office hour events."""
    # Arrange
    site, room = arrange_course_site(session)
    instructor = make_subject(1, "instructor")
    existing_events = arrange_existing_recurring_events(session, site.id, room.id)
    oh_recurrence_svc, office_hours_svc = make_service(session)

    # Act
    oh_recurrence_svc.delete_recurring(
        instructor,
        site.id,
        existing_events[1].id,
    )

    # Assert
    remaining_events = session.scalars(select(OfficeHoursEntity)).all()
    assert [event.id for event in remaining_events] == [existing_events[0].id]
    office_hours_svc._check_site_admin_permissions.assert_called_once_with(
        instructor, site.id
    )


def test_delete_recurring_oh_event_not_found(
    session: Session,
):
    """Ensures that an exception is thrown when an unknown OH event ID is provided."""
    # Arrange
    site, _ = arrange_course_site(session)
    instructor = make_subject(1, "instructor")
    oh_recurrence_svc, _ = make_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_recurrence_svc.delete_recurring(
            instructor,
            site.id,
            999,
        )


def test_delete_recurring_oh_event_not_authorized(
    session: Session,
):
    """Ensures that an unauthorized user cannot delete recurring events."""
    # Arrange
    site, room = arrange_course_site(session)
    unauthorized_user = make_subject(2, "root")
    existing_events = arrange_existing_recurring_events(session, site.id, room.id)
    oh_recurrence_svc, _ = make_service(
        session, CoursePermissionException("Not authorized")
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_recurrence_svc.delete_recurring(
            unauthorized_user,
            site.id,
            existing_events[1].id,
        )
