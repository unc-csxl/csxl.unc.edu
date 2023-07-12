"""Tests for Coworking Operating Hours Service."""

from ....services.coworking import OperatingHoursService
from ....models.coworking import OperatingHours, TimeRange

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import operating_hours_svc
from .times import *

# Insert fake data entities in database
from .operating_hours_data import fake_data_fixture

# Import the fake model data in a namespace for test assertions
from . import operating_hours_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_schedule_closed(operating_hours_svc: OperatingHoursService):
    """When there are no operating hours open in a given time range, returns an empty list."""
    time_range = TimeRange(start=A_WEEK_AGO, end=A_WEEK_AGO + ONE_HOUR)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 0


def test_schedule_one_match(operating_hours_svc: OperatingHoursService):
    """When one OperatingHours matches the time range, returns a list with just it."""
    time_range = TimeRange(start=NOW, end=IN_ONE_HOUR)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 1
    assert result[0].id == operating_hours_data.today.id


def test_schedule_multiple_match(operating_hours_svc: OperatingHoursService):
    """When one OperatingHours matches the time range, returns a list with just it."""
    time_range = TimeRange(start=TOMORROW, end=TOMORROW + ONE_DAY)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 2
    assert result[0].id == operating_hours_data.tomorrow.id
    assert result[1].id == operating_hours_data.future.id
