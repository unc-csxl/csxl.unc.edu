"""Unit tests for the TimeRange utility class."""

import pytest, json
from pydantic import ValidationError
from ....models.coworking import TimeRange
from ...services.coworking.time import *

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_initialization(time: dict[str, datetime]):
    time_range = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    assert time_range.start == time[NOW]
    assert time_range.end == time[IN_THIRTY_MINUTES]


def test_initialization_from_json_utc():
    input = '{"start":"2023-07-27T22:00:11.685Z", "end": "2023-07-27T22:01:11.685Z"}'
    data = json.loads(input)
    time_range = TimeRange(**data)
    assert time_range.start.tzinfo is None
    assert time_range.start.hour == 18


def test_validation_failure(time: dict[str, datetime]):
    with pytest.raises(ValidationError):
        time_range = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[NOW])


def test_overlaps_no_overlap(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    time_range_2 = TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS])
    assert not time_range_1.overlaps(time_range_2)
    assert not time_range_2.overlaps(time_range_1)


def test_partial_overlap_start(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    time_range_2 = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_TWO_HOURS])
    assert time_range_1.overlaps(time_range_2)
    assert time_range_2.overlaps(time_range_1)


def test_partial_overlap_end(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_TWO_HOURS])
    time_range_2 = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    assert time_range_1.overlaps(time_range_2)
    assert time_range_2.overlaps(time_range_1)


def test_total_overlap(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[NOW], end=time[IN_TWO_HOURS])
    time_range_2 = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_ONE_HOUR])
    assert time_range_1.overlaps(time_range_2)
    assert time_range_2.overlaps(time_range_1)


def test_subtract_no_overlap(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    time_range_2 = TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS])
    assert time_range_1.subtract(time_range_2) == [time_range_1]
    assert time_range_2.subtract(time_range_1) == [time_range_2]


def test_subtract_partial_overlap_start(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    time_range_2 = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_TWO_HOURS])
    assert time_range_1.subtract(time_range_2) == [
        TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    ]
    assert time_range_2.subtract(time_range_1) == [
        TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS])
    ]


def test_subtract_partial_overlap_end(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_TWO_HOURS])
    time_range_2 = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    assert time_range_1.subtract(time_range_2) == [
        TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS])
    ]
    assert time_range_2.subtract(time_range_1) == [
        TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    ]


def test_subtract_inside(time: dict[str, datetime]):
    time_range_1 = TimeRange(start=time[NOW], end=time[IN_TWO_HOURS])
    time_range_2 = TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_ONE_HOUR])
    assert time_range_1.subtract(time_range_2) == [
        TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
        TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
    ]
    assert time_range_2.subtract(time_range_1) == []


def test_duration(time: dict[str, datetime]):
    time_range = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    assert time_range.duration() == THIRTY_MINUTES

    time_range = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    assert time_range.duration() == ONE_HOUR
