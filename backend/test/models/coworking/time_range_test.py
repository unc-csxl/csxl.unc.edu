"""Unit tests for the TimeRange utility class."""

import pytest
from pydantic import ValidationError
from ....models.coworking import TimeRange
from ...services.coworking.times import *

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_initialization():
    time_range = TimeRange(start=NOW, end=IN_THIRTY_MINUTES)
    assert time_range.start == NOW
    assert time_range.end == IN_THIRTY_MINUTES


def test_validation_failure():
    with pytest.raises(ValidationError):
        time_range = TimeRange(start=IN_THIRTY_MINUTES, end=NOW)


def test_overlaps_no_overlap():
    time_range_1 = TimeRange(start=NOW, end=IN_THIRTY_MINUTES)
    time_range_2 = TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS)
    assert not time_range_1.overlaps(time_range_2)
    assert not time_range_2.overlaps(time_range_1)


def test_partial_overlap_start():
    time_range_1 = TimeRange(start=NOW, end=IN_ONE_HOUR)
    time_range_2 = TimeRange(start=IN_THIRTY_MINUTES, end=IN_TWO_HOURS)
    assert time_range_1.overlaps(time_range_2)
    assert time_range_2.overlaps(time_range_1)


def test_partial_overlap_end():
    time_range_1 = TimeRange(start=IN_THIRTY_MINUTES, end=IN_TWO_HOURS)
    time_range_2 = TimeRange(start=NOW, end=IN_ONE_HOUR)
    assert time_range_1.overlaps(time_range_2)
    assert time_range_2.overlaps(time_range_1)


def test_total_overlap():
    time_range_1 = TimeRange(start=NOW, end=IN_TWO_HOURS)
    time_range_2 = TimeRange(start=IN_THIRTY_MINUTES, end=IN_ONE_HOUR)
    assert time_range_1.overlaps(time_range_2)
    assert time_range_2.overlaps(time_range_1)


def test_subtract_no_overlap():
    time_range_1 = TimeRange(start=NOW, end=IN_THIRTY_MINUTES)
    time_range_2 = TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS)
    assert time_range_1.subtract(time_range_2) == [time_range_1]
    assert time_range_2.subtract(time_range_1) == [time_range_2]


def test_subtract_partial_overlap_start():
    time_range_1 = TimeRange(start=NOW, end=IN_ONE_HOUR)
    time_range_2 = TimeRange(start=IN_THIRTY_MINUTES, end=IN_TWO_HOURS)
    assert time_range_1.subtract(time_range_2) == [
        TimeRange(start=NOW, end=IN_THIRTY_MINUTES)
    ]
    assert time_range_2.subtract(time_range_1) == [
        TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS)
    ]


def test_subtract_partial_overlap_end():
    time_range_1 = TimeRange(start=IN_THIRTY_MINUTES, end=IN_TWO_HOURS)
    time_range_2 = TimeRange(start=NOW, end=IN_ONE_HOUR)
    assert time_range_1.subtract(time_range_2) == [
        TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS)
    ]
    assert time_range_2.subtract(time_range_1) == [
        TimeRange(start=NOW, end=IN_THIRTY_MINUTES)
    ]


def test_subtract_inside():
    time_range_1 = TimeRange(start=NOW, end=IN_TWO_HOURS)
    time_range_2 = TimeRange(start=IN_THIRTY_MINUTES, end=IN_ONE_HOUR)
    assert time_range_1.subtract(time_range_2) == [
        TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
        TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
    ]
    assert time_range_2.subtract(time_range_1) == []


def test_duration():
    time_range = TimeRange(start=NOW, end=IN_THIRTY_MINUTES)
    assert time_range.duration() == THIRTY_MINUTES

    time_range = TimeRange(start=NOW, end=IN_ONE_HOUR)
    assert time_range.duration() == ONE_HOUR
