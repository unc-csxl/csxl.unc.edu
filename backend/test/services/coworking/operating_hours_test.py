"""Tests for Coworking Operating Hours Service."""

from unittest.mock import create_autospec, call

from backend.entities.coworking.operating_hours_entity import OperatingHoursEntity
from backend.models.coworking.operating_hours import (
    OperatingHoursDraft,
    OperatingHoursRecurrence,
)

from ....services.coworking import OperatingHoursService
from ....models.coworking import OperatingHours, TimeRange
from ....services.coworking.exceptions import OperatingHoursCannotOverlapException
from ....services import PermissionService
from ....services.exceptions import ResourceNotFoundException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, operating_hours_svc
from .time import *

# Insert fake data entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from .operating_hours_data import fake_data_fixture as insert_order_1

# Import the fake model data in a namespace for test assertions
from . import operating_hours_data
from ..core_data import user_data

__authors__ = ["Kris Jordan", "Tobenna Okoli", "David Foss"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_schedule_closed(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """When there are no operating hours open in a given time range, returns an empty list."""
    time_range = TimeRange(start=time[A_WEEK_AGO], end=time[A_WEEK_AGO] + ONE_HOUR)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 0


def test_schedule_one_match(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """When one OperatingHours matches the time range, returns a list with just it."""
    time_range = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 1
    assert result[0].id == operating_hours_data.today.id


def test_schedule_multiple_match(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """When multiple OperatingHours match the time range, returns a list with just it."""
    time_range = TimeRange(start=time[TOMORROW], end=time[TOMORROW] + ONE_DAY)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 2
    assert result[0].id == operating_hours_data.tomorrow.id
    assert result[1].id == operating_hours_data.future.id


def test_create(operating_hours_svc: OperatingHoursService, time: dict[str, datetime]):
    """Creating an Operating Hours entity expected case."""
    operating_hours_draft = OperatingHoursDraft(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
    )
    result: OperatingHours = operating_hours_svc.create(
        user_data.root, operating_hours_draft
    )
    assert result.id is not None


def test_create_overlap(operating_hours_svc: OperatingHoursService):
    """Creating an Operating Hours entity that overlaps with another raises OperatingHoursCannotOverlapException"""
    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.create(
            user_data.root,
            OperatingHoursDraft(
                start=operating_hours_data.future.start + timedelta(minutes=30),
                end=operating_hours_data.future.end + timedelta(minutes=30),
            ),
        )


def test_create_enforces_permission(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """Ensure we are enforcing coworking.operating_hours.create on coworking/operating_hours"""
    permission_svc = create_autospec(PermissionService)
    operating_hours_svc._permission_svc = permission_svc
    operating_hours_draft = OperatingHoursDraft(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
    )
    operating_hours_svc.create(user_data.user, operating_hours_draft)
    permission_svc.enforce.assert_called_with(
        user_data.user,
        "coworking.operating_hours.create",
        "coworking/operating_hours",
    )


def test_recurring_create(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """Creating a recurring Operating Hours entity expected case."""
    operating_hours_draft = OperatingHoursDraft(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
        recurrence=OperatingHoursRecurrence(
            end_date=datetime.now() + timedelta(days=50), recurs_on=0b10100
        ),
    )
    result: OperatingHours = operating_hours_svc.create(
        user_data.root, operating_hours_draft
    )

    hours_in_future_week = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > time[TOMORROW] + timedelta(days=30, hours=10),
            OperatingHoursEntity.end < time[TOMORROW] + timedelta(days=37, hours=10),
            OperatingHoursEntity.recurrence_id == result.recurrence_id,
        )
        .all()
    )

    print(len(hours_in_future_week))
    assert len(hours_in_future_week) == 2

    for operating_hours in hours_in_future_week:
        assert (
            operating_hours.start.hour == result.start.hour
            and operating_hours.start.minute == result.start.minute
            and operating_hours.start.second == result.start.second
            and operating_hours.start.microsecond == result.start.microsecond
            and operating_hours.end.hour == result.end.hour
            and operating_hours.end.minute == result.end.minute
            and operating_hours.end.second == result.end.second
            and operating_hours.end.microsecond == result.end.microsecond
        )


def test_recurring_create_overlap(operating_hours_svc: OperatingHoursService):
    """Creating a recurring Operating Hours entity that overlaps in the future raises OperatingHoursCannotOverlapException"""
    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.create(
            user_data.root,
            OperatingHoursDraft(
                start=datetime.now().replace(hour=11),
                end=datetime.now().replace(hour=15),
                recurrence=OperatingHoursRecurrence(
                    end_date=datetime.now() + timedelta(days=30), recurs_on=0b11111
                ),
            ),
        )


def test_update(operating_hours_svc: OperatingHoursService):
    """Update an Operating Hours entity expected case."""
    future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    future.start = future.start + timedelta(minutes=30)
    future.end = future.end + timedelta(minutes=30)
    operating_hours_svc.update(user_data.root, future)
    updated_future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    assert updated_future.start == future.start and updated_future.end == future.end


def test_update_overlap(operating_hours_svc: OperatingHoursService):
    """Updating an Operating Hours entity to where it overlaps with another raises OperatingHoursCannotOverlapException"""
    tomorrow = operating_hours_svc.get_by_id(operating_hours_data.tomorrow.id)
    future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    future.start = tomorrow.start
    future.end = tomorrow.end

    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.update(user_data.root, future)


def test_recurring_update_hours(operating_hours_svc: OperatingHoursService):
    """Update an Operating Hours entity expected case when just updating the hours."""

    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )
    future_tuesday_recurring = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > tuesday_recurring.start + timedelta(days=15),
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .first()
    )
    future_tuesday_recurring.start = future_tuesday_recurring.start + timedelta(
        minutes=30
    )
    future_tuesday_recurring.end = future_tuesday_recurring.end + timedelta(minutes=30)
    operating_hours_svc.update(user_data.root, future_tuesday_recurring, cascade=True)
    for entity in (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    ):
        assert (
            entity.start.hour == future_tuesday_recurring.start.hour
            and entity.start.minute == future_tuesday_recurring.start.minute
            and entity.start.second == future_tuesday_recurring.start.second
            and entity.start.microsecond == future_tuesday_recurring.start.microsecond
            and entity.end.hour == future_tuesday_recurring.end.hour
            and entity.end.minute == future_tuesday_recurring.end.minute
            and entity.end.second == future_tuesday_recurring.end.second
            and entity.end.microsecond == future_tuesday_recurring.end.microsecond
        )
    for entity in (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start < future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    ):
        assert (
            entity.start.hour == tuesday_recurring.start.hour
            and entity.start.minute == tuesday_recurring.start.minute
            and entity.start.second == tuesday_recurring.start.second
            and entity.start.microsecond == tuesday_recurring.start.microsecond
            and entity.end.hour == tuesday_recurring.end.hour
            and entity.end.minute == tuesday_recurring.end.minute
            and entity.end.second == tuesday_recurring.end.second
            and entity.end.microsecond == tuesday_recurring.end.microsecond
        )


def test_recurring_update_days(operating_hours_svc: OperatingHoursService):
    """Update an Operating Hours entity expected case when changing recur_on."""
    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )
    future_tuesday_recurring = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > tuesday_recurring.start + timedelta(days=15),
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .first()
    ).to_model()

    future_tuesday_recurring_draft = OperatingHoursDraft(
        id=future_tuesday_recurring.id,
        start=future_tuesday_recurring.start,
        end=future_tuesday_recurring.end,
        recurrence=future_tuesday_recurring.recurrence,
    )
    future_tuesday_recurring_draft.recurrence.recurs_on = 0b10000
    operating_hours_svc.update(
        user_data.root, future_tuesday_recurring_draft, cascade=True
    )
    for entity in (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    ):
        assert entity.start.weekday() == 4
    for entity in (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start < future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    ):
        assert entity.start.weekday() == 1


def test_recurring_update_extend(operating_hours_svc: OperatingHoursService):
    """Update an Operating Hours entity expected case when making end_date later."""
    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )
    future_tuesday_recurring = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > tuesday_recurring.start + timedelta(days=15),
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .first()
    ).to_model()

    future_tuesday_recurring_draft = OperatingHoursDraft(
        id=future_tuesday_recurring.id,
        start=future_tuesday_recurring.start,
        end=future_tuesday_recurring.end,
        recurrence=future_tuesday_recurring.recurrence,
    )

    original_days_following = len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )

    future_tuesday_recurring_draft.recurrence.end_date = (
        future_tuesday_recurring_draft.recurrence.end_date + timedelta(days=7)
    )
    operating_hours_svc.update(
        user_data.root, future_tuesday_recurring_draft, cascade=True
    )
    assert original_days_following + 1 == len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )


def test_recurring_update_contract(operating_hours_svc: OperatingHoursService):
    """Update an Operating Hours entity expected case when making end_date sooner."""
    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )
    future_tuesday_recurring = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > tuesday_recurring.start + timedelta(days=15),
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .first()
    ).to_model()

    future_tuesday_recurring_draft = OperatingHoursDraft(
        id=future_tuesday_recurring.id,
        start=future_tuesday_recurring.start,
        end=future_tuesday_recurring.end,
        recurrence=future_tuesday_recurring.recurrence,
    )

    original_days_following = len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )

    future_tuesday_recurring_draft.recurrence.end_date = (
        future_tuesday_recurring_draft.recurrence.end_date - timedelta(days=7)
    )
    operating_hours_svc.update(
        user_data.root, future_tuesday_recurring_draft, cascade=True
    )
    assert original_days_following - 1 == len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )


def test_recurring_update_overlap(operating_hours_svc: OperatingHoursService):
    """Updating an Operating Hours entity to where recurrence overlaps with another raises OperatingHoursCannotOverlapException"""
    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )

    tuesday_recurring_draft = OperatingHoursDraft(
        id=tuesday_recurring.id,
        start=tuesday_recurring.start,
        end=tuesday_recurring.end,
        recurrence=tuesday_recurring.recurrence,
    )
    tuesday_recurring_draft.recurrence.recurs_on = 0b00001
    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.update(
            user_data.root, tuesday_recurring_draft, cascade=True
        )


def test_update_enforces_permission(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """Ensure we are enforcing coworking.operating_hours.create on coworking/operating_hours"""
    permission_svc = create_autospec(PermissionService)
    operating_hours_svc._permission_svc = permission_svc

    future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    future.end = future.end + timedelta(minutes=30)
    operating_hours_svc.update(user_data.root, future)
    permission_svc.enforce.assert_called_with(
        user_data.root,
        "coworking.operating_hours.update",
        "coworking/operating_hours",
    )


def test_delete(operating_hours_svc: OperatingHoursService):
    """Delete an Operating Hours entity expected case."""
    future = operating_hours_svc.get_by_id(operating_hours_data.future.id)  # type: ignore
    assert future.id is not None
    operating_hours_svc.delete(user_data.root, future)
    with pytest.raises(ResourceNotFoundException):
        future = operating_hours_svc.get_by_id(operating_hours_data.future.id)  # type: ignore


def test_delete_permissions(operating_hours_svc: OperatingHoursService):
    """Delete an Operating Hours entity expected case."""
    permission_svc = create_autospec(PermissionService)
    operating_hours_svc._permission_svc = permission_svc

    assert operating_hours_data.future.id is not None
    operating_hours_svc.delete(user_data.root, operating_hours_data.future)
    permission_svc.enforce.assert_called_with(
        user_data.root,
        "coworking.operating_hours.delete",
        f"coworking/operating_hours/{operating_hours_data.future.id}",
    )


def test_delete_recurring(operating_hours_svc: OperatingHoursService):
    """Delete an Operating Hours entity expected case when deleting an hour that recurs."""
    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )
    future_tuesday_recurring = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > tuesday_recurring.start + timedelta(days=15),
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .first()
    ).to_model()
    original_days_following = len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )
    assert future_tuesday_recurring.id is not None
    assert original_days_following > 0
    operating_hours_svc.delete(user_data.root, future_tuesday_recurring, True)
    with pytest.raises(ResourceNotFoundException):
        future_tuesday_recurring = operating_hours_svc.get_by_id(future_tuesday_recurring.id)  # type: ignore

    assert 0 == len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )

    assert future_tuesday_recurring.start >= operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    ).recurrence.end_date.replace(tzinfo=future_tuesday_recurring.start.tzinfo)


def test_delete_mid_recurrence(operating_hours_svc: OperatingHoursService):
    """Delete an Operating Hours entity expected case when deleting an hour that recurs without cascading."""
    tuesday_recurring = operating_hours_svc.get_by_id(
        operating_hours_data.tuesday_recurring.id
    )
    future_tuesday_recurring = (
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > tuesday_recurring.start + timedelta(days=15),
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .first()
    ).to_model()
    original_days_following = len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )
    assert future_tuesday_recurring.id is not None
    assert original_days_following > 0
    operating_hours_svc.delete(user_data.root, future_tuesday_recurring)
    with pytest.raises(ResourceNotFoundException):
        future_tuesday_recurring = operating_hours_svc.get_by_id(future_tuesday_recurring.id)  # type: ignore

    assert original_days_following == len(
        operating_hours_svc._session.query(OperatingHoursEntity)
        .filter(
            OperatingHoursEntity.start > future_tuesday_recurring.start,
            OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
        )
        .all()
    )

    assert (
        tuesday_recurring.recurrence.end_date
        == (
            operating_hours_svc._session.query(OperatingHoursEntity)
            .filter(
                OperatingHoursEntity.start > future_tuesday_recurring.start,
                OperatingHoursEntity.recurrence_id == tuesday_recurring.recurrence_id,
            )
            .first()
        )
        .to_model()
        .recurrence.end_date
    )
