"""Unit tests for AvailabilityList model."""

import pytest
from pydantic import ValidationError
from ....models.coworking import AvailabilityList, TimeRange
from ...services.coworking.times import *

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_intialize():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    assert len(availability_list.availability) == 2


def test_validation_error_unsorted():
    with pytest.raises(ValidationError):
        availability_list = AvailabilityList(
            availability=[
                TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
                TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            ]
        )


def test_validation_error_overlaps():
    with pytest.raises(ValidationError):
        availability_list = AvailabilityList(
            availability=[
                TimeRange(start=NOW, end=IN_ONE_HOUR),
                TimeRange(start=IN_THIRTY_MINUTES, end=IN_TWO_HOURS),
            ]
        )


def test_constrain_front_single():
    availability_list = AvailabilityList(
        availability=[TimeRange(start=NOW, end=IN_THIRTY_MINUTES)]
    )
    availability_list.constrain(
        TimeRange(start=NOW + ONE_MINUTE, end=IN_THIRTY_MINUTES)
    )
    assert availability_list.availability[0].start == NOW + ONE_MINUTE
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES
    assert len(availability_list.availability) == 1


def test_constrain_front_do_not_truncate():
    availability_list = AvailabilityList(
        availability=[TimeRange(start=NOW, end=IN_THIRTY_MINUTES)]
    )
    availability_list.constrain(
        TimeRange(start=NOW - ONE_MINUTE, end=IN_THIRTY_MINUTES)
    )
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES
    assert len(availability_list.availability) == 1


def test_constrain_front_multiple():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.constrain(TimeRange(start=IN_THIRTY_MINUTES, end=IN_TWO_HOURS))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == IN_ONE_HOUR
    assert availability_list.availability[0].end == IN_TWO_HOURS


def test_constrain_front_empty():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.constrain(TimeRange(start=IN_TWO_HOURS, end=TOMORROW))
    assert len(availability_list.availability) == 0


def test_constrain_back_single():
    availability_list = AvailabilityList(
        availability=[TimeRange(start=NOW, end=IN_THIRTY_MINUTES)]
    )
    availability_list.constrain(
        TimeRange(start=NOW, end=IN_THIRTY_MINUTES - ONE_MINUTE)
    )
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES - ONE_MINUTE
    assert len(availability_list.availability) == 1


def test_constrain_back_do_not_truncate():
    availability_list = AvailabilityList(
        availability=[TimeRange(start=NOW, end=IN_THIRTY_MINUTES)]
    )
    availability_list.constrain(
        TimeRange(start=NOW, end=IN_THIRTY_MINUTES + ONE_MINUTE)
    )
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES
    assert len(availability_list.availability) == 1


def test_constrain_back_multiple():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.constrain(TimeRange(start=NOW, end=IN_ONE_HOUR))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES


def test_constrain_back_empty():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.constrain(TimeRange(start=THIRTY_MINUTES_AGO, end=NOW))
    assert len(availability_list.availability) == 0


def test_subtract_availability_empty():
    availability_list = AvailabilityList(availability=[])
    availability_list.subtract(TimeRange(start=NOW, end=IN_TWO_HOURS))
    assert len(availability_list.availability) == 0


def test_subtract_availability_before_first():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.subtract(TimeRange(start=NOW, end=IN_THIRTY_MINUTES))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == IN_ONE_HOUR
    assert availability_list.availability[0].end == IN_TWO_HOURS


def test_subtract_availability_after_last():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
        ]
    )
    availability_list.subtract(TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES


def test_subtract_all_availability_across_multiple():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.subtract(TimeRange(start=NOW, end=IN_TWO_HOURS))
    assert len(availability_list.availability) == 0


def test_subtract_availability_in_one():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.subtract(TimeRange(start=NOW, end=NOW + FIVE_MINUTES))
    assert len(availability_list.availability) == 2
    assert availability_list.availability[0].start == NOW + FIVE_MINUTES


def test_subtract_availability_inside():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.subtract(
        TimeRange(start=NOW + FIVE_MINUTES, end=NOW + 2 * FIVE_MINUTES)
    )
    assert len(availability_list.availability) == 3
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == NOW + FIVE_MINUTES
    assert availability_list.availability[1].start == NOW + 2 * FIVE_MINUTES
    assert availability_list.availability[1].end == IN_THIRTY_MINUTES


def test_subtract_availability_across_boundaries():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=IN_THIRTY_MINUTES),
            TimeRange(start=IN_ONE_HOUR, end=IN_TWO_HOURS),
        ]
    )
    availability_list.subtract(
        TimeRange(
            start=IN_THIRTY_MINUTES - FIVE_MINUTES, end=IN_ONE_HOUR + FIVE_MINUTES
        )
    )
    assert len(availability_list.availability) == 2
    assert availability_list.availability[0].start == NOW
    assert availability_list.availability[0].end == IN_THIRTY_MINUTES - FIVE_MINUTES
    assert availability_list.availability[1].start == IN_ONE_HOUR + FIVE_MINUTES
    assert availability_list.availability[1].end == IN_TWO_HOURS


def test_filter_time_ranges_below():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=NOW + FIVE_MINUTES),
            TimeRange(start=NOW + FIVE_MINUTES, end=NOW + THIRTY_MINUTES),
        ]
    )
    assert len(availability_list.availability) == 2
    availability_list.filter_time_ranges_below(FIVE_MINUTES)
    assert len(availability_list.availability) == 2
    availability_list.filter_time_ranges_below(FIVE_MINUTES + timedelta(seconds=1))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == NOW + FIVE_MINUTES


def test_total_duration_empty():
    none = AvailabilityList(availability=[])
    assert none.total_duration() == timedelta(0)


def test_total_duration_multiple():
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=NOW, end=NOW + FIVE_MINUTES),
            TimeRange(start=NOW + FIVE_MINUTES, end=NOW + THIRTY_MINUTES),
        ]
    )
    assert availability_list.total_duration() == timedelta(minutes=30)
