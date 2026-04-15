"""Tests for Coworking Operating Hours Service."""

from datetime import datetime, timedelta
from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from ....entities.coworking import OperatingHoursEntity
from ....services.coworking import OperatingHoursService
from ....models.coworking import OperatingHours, TimeRange
from ....services.coworking.exceptions import OperatingHoursCannotOverlapException
from ....services import PermissionService
from ....services.exceptions import ResourceNotFoundException
from .time import *
from ....models import User

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def make_subject(user_id: int = 1) -> User:
    return User(id=user_id, pid=user_id, onyen=f"user{user_id}")


def make_service(
    session: Session, permission_svc: PermissionService | None = None
) -> OperatingHoursService:
    return OperatingHoursService(
        session,
        (
            permission_svc
            if permission_svc is not None
            else create_autospec(PermissionService)
        ),
    )


def arrange_operating_hours(
    session: Session, time: dict[str, datetime]
) -> dict[str, OperatingHours]:
    arranged = {
        "today": OperatingHours(
            id=1,
            start=time[AN_HOUR_AGO],
            end=time[IN_THREE_HOURS],
        ),
        "future": OperatingHours(
            id=2,
            start=time[AN_HOUR_AGO] + 2 * ONE_DAY,
            end=time[IN_TWO_HOURS] + 2 * ONE_DAY,
        ),
        "tomorrow": OperatingHours(
            id=3,
            start=time[AN_HOUR_AGO] + ONE_DAY,
            end=time[IN_TWO_HOURS] + ONE_DAY,
        ),
        "three_days_from_today": OperatingHours(
            id=4,
            start=time[AN_HOUR_AGO] + 3 * ONE_DAY,
            end=time[IN_EIGHT_HOURS] + 3 * ONE_DAY,
        ),
    }

    session.add_all(
        OperatingHoursEntity.from_model(operating_hours)
        for operating_hours in arranged.values()
    )
    session.commit()

    return arranged


def test_schedule_closed(session: Session, time: dict[str, datetime]):
    """When there are no operating hours open in a given time range, returns an empty list."""
    operating_hours_svc = make_service(session)

    time_range = TimeRange(start=time[A_WEEK_AGO], end=time[A_WEEK_AGO] + ONE_HOUR)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 0


def test_schedule_one_match(session: Session, time: dict[str, datetime]):
    """When one OperatingHours matches the time range, returns a list with just it."""
    arranged = arrange_operating_hours(session, time)
    operating_hours_svc = make_service(session)

    time_range = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 1
    assert result[0].id == arranged["today"].id


def test_schedule_multiple_match(session: Session, time: dict[str, datetime]):
    """When one OperatingHours matches the time range, returns a list with just it."""
    arranged = arrange_operating_hours(session, time)
    operating_hours_svc = make_service(session)

    time_range = TimeRange(start=time[TOMORROW], end=time[TOMORROW] + ONE_DAY)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 2
    assert result[0].id == arranged["tomorrow"].id
    assert result[1].id == arranged["future"].id


def test_create(session: Session, time: dict[str, datetime]):
    """Creating an Operating Hours entity expected case."""
    operating_hours_svc = make_service(session)

    time_range = TimeRange(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
    )
    result: OperatingHours = operating_hours_svc.create(make_subject(), time_range)
    assert result.id is not None


def test_create_overlap(session: Session, time: dict[str, datetime]):
    """Creating an Operating Hours entity that overlaps with another raises OperatingHoursCannotOverlapException"""
    arranged = arrange_operating_hours(session, time)
    operating_hours_svc = make_service(session)

    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.create(
            make_subject(),
            TimeRange(
                start=arranged["future"].start + timedelta(minutes=30),
                end=arranged["future"].end + timedelta(minutes=30),
            ),
        )


def test_create_enforces_permission(session: Session, time: dict[str, datetime]):
    """Ensure we are enforcing coworking.operating_hours.create on coworking/operating_hours"""
    permission_svc = create_autospec(PermissionService)
    operating_hours_svc = make_service(session, permission_svc)

    time_range = TimeRange(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
    )
    subject = make_subject(7)

    operating_hours_svc.create(subject, time_range)

    permission_svc.enforce.assert_called_with(
        subject,
        "coworking.operating_hours.create",
        "coworking/operating_hours",
    )


def test_delete(session: Session, time: dict[str, datetime]):
    """Delete an Operating Hours entity expected case."""
    arranged = arrange_operating_hours(session, time)
    operating_hours_svc = make_service(session)

    future = operating_hours_svc.get_by_id(arranged["future"].id)  # type: ignore[arg-type]
    assert future.id is not None
    operating_hours_svc.delete(make_subject(), future)

    with pytest.raises(ResourceNotFoundException):
        operating_hours_svc.get_by_id(arranged["future"].id)  # type: ignore[arg-type]


def test_delete_permissions(session: Session, time: dict[str, datetime]):
    """Delete an Operating Hours entity expected case."""
    arranged = arrange_operating_hours(session, time)
    permission_svc = create_autospec(PermissionService)
    operating_hours_svc = make_service(session, permission_svc)
    subject = make_subject()

    assert arranged["future"].id is not None
    operating_hours_svc.delete(subject, arranged["future"])

    permission_svc.enforce.assert_called_with(
        subject,
        "coworking.operating_hours.delete",
        f"coworking/operating_hours/{arranged['future'].id}",
    )
