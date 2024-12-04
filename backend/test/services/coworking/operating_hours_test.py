"""Tests for Coworking Operating Hours Service."""

from unittest.mock import create_autospec, call

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

__authors__ = ["Kris Jordan", "Tobenna Okoli"]
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
    time_range = TimeRange(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
    )
    result: OperatingHours = operating_hours_svc.create(user_data.root, time_range)
    assert result.id is not None


def test_create_overlap(operating_hours_svc: OperatingHoursService):
    """Creating an Operating Hours entity that overlaps with another raises OperatingHoursCannotOverlapException"""
    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.create(
            user_data.root,
            TimeRange(
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
    time_range = TimeRange(
        start=time[TOMORROW] + timedelta(days=5),
        end=time[TOMORROW] + timedelta(days=5, hours=2),
    )
    operating_hours_svc.create(user_data.user, time_range)
    permission_svc.enforce.assert_called_with(
        user_data.user,
        "coworking.operating_hours.create",
        "coworking/operating_hours",
    )


def test_update(operating_hours_svc: OperatingHoursService):
    """Update an Operating Hours entity expected case."""
    future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    future.end = future.end + timedelta(minutes=30)
    operating_hours_svc.update(user_data.root, future)
    updated_future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    assert updated_future.end == future.end


def test_update_overlap(operating_hours_svc: OperatingHoursService):
    """Updating an Operating Hours entity that overlaps with another raises OperatingHoursCannotOverlapException"""
    tomorrow = operating_hours_svc.get_by_id(operating_hours_data.tomorrow.id)
    future = operating_hours_svc.get_by_id(operating_hours_data.future.id)
    future.start = tomorrow.start
    future.end = tomorrow.end

    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.update(user_data.root, future)


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
