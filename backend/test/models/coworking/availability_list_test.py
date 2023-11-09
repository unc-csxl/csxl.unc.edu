"""Unit tests for AvailabilityList model."""

import pytest
from pydantic import ValidationError
from ....models.coworking import AvailabilityList, TimeRange
from ...services.coworking.time import *

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_intialize(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    assert len(availability_list.availability) == 2


def test_validation_error_unsorted(time: dict[str, datetime]):
    with pytest.raises(ValidationError):
        availability_list = AvailabilityList(
            availability=[
                TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
                TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            ]
        )


def test_validation_error_overlaps(time: dict[str, datetime]):
    with pytest.raises(ValidationError):
        availability_list = AvailabilityList(
            availability=[
                TimeRange(start=time[NOW], end=time[IN_ONE_HOUR]),
                TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_TWO_HOURS]),
            ]
        )


def test_constrain_front_single(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])]
    )
    availability_list.constrain(
        TimeRange(start=time[NOW] + ONE_MINUTE, end=time[IN_THIRTY_MINUTES])
    )
    assert availability_list.availability[0].start == time[NOW] + ONE_MINUTE
    assert availability_list.availability[0].end == time[IN_THIRTY_MINUTES]
    assert len(availability_list.availability) == 1


def test_constrain_front_do_not_truncate(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])]
    )
    availability_list.constrain(
        TimeRange(start=time[NOW] - ONE_MINUTE, end=time[IN_THIRTY_MINUTES])
    )
    assert availability_list.availability[0].start == time[NOW]
    assert availability_list.availability[0].end == time[IN_THIRTY_MINUTES]
    assert len(availability_list.availability) == 1


def test_constrain_front_multiple(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.constrain(
        TimeRange(start=time[IN_THIRTY_MINUTES], end=time[IN_TWO_HOURS])
    )
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == time[IN_ONE_HOUR]
    assert availability_list.availability[0].end == time[IN_TWO_HOURS]


def test_constrain_front_empty(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.constrain(TimeRange(start=time[IN_TWO_HOURS], end=time[TOMORROW]))
    assert len(availability_list.availability) == 0


def test_constrain_back_single(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])]
    )
    availability_list.constrain(
        TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES] - ONE_MINUTE)
    )
    assert availability_list.availability[0].start == time[NOW]
    assert availability_list.availability[0].end == time[IN_THIRTY_MINUTES] - ONE_MINUTE

    assert len(availability_list.availability) == 1


def test_constrain_back_do_not_truncate(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])]
    )
    availability_list.constrain(
        TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES] + ONE_MINUTE)
    )
    assert availability_list.availability[0].start == time[NOW]
    assert availability_list.availability[0].end == time[IN_THIRTY_MINUTES]
    assert len(availability_list.availability) == 1


def test_constrain_back_multiple(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.constrain(TimeRange(start=time[NOW], end=time[IN_ONE_HOUR]))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == time[NOW]
    assert availability_list.availability[0].end == time[IN_THIRTY_MINUTES]


def test_constrain_back_empty(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.constrain(
        TimeRange(start=time[THIRTY_MINUTES_AGO], end=time[NOW])
    )
    assert len(availability_list.availability) == 0


def test_subtract_availability_empty(time: dict[str, datetime]):
    availability_list = AvailabilityList(availability=[])
    availability_list.subtract(TimeRange(start=time[NOW], end=time[IN_TWO_HOURS]))
    assert len(availability_list.availability) == 0


def test_subtract_availability_before_first(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.subtract(TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == time[IN_ONE_HOUR]
    assert availability_list.availability[0].end == time[IN_TWO_HOURS]


def test_subtract_availability_after_last(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
        ]
    )
    availability_list.subtract(
        TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS])
    )
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == time[NOW]
    assert availability_list.availability[0].end == time[IN_THIRTY_MINUTES]


def test_subtract_all_availability_across_multiple(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.subtract(TimeRange(start=time[NOW], end=time[IN_TWO_HOURS]))
    assert len(availability_list.availability) == 0


def test_subtract_availability_in_one(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.subtract(TimeRange(start=time[NOW], end=time[NOW] + FIVE_MINUTES))
    assert len(availability_list.availability) == 2
    assert availability_list.availability[0].start == time[NOW] + FIVE_MINUTES


def test_subtract_availability_inside(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.subtract(
        TimeRange(start=time[NOW] + FIVE_MINUTES, end=time[NOW] + 2 * FIVE_MINUTES)
    )
    assert len(availability_list.availability) == 3
    assert availability_list.availability[0].start == time[NOW]
    assert availability_list.availability[0].end == time[NOW] + FIVE_MINUTES
    assert availability_list.availability[1].start == time[NOW] + 2 * FIVE_MINUTES
    assert availability_list.availability[1].end == time[IN_THIRTY_MINUTES]


def test_subtract_availability_across_boundaries(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES]),
            TimeRange(start=time[IN_ONE_HOUR], end=time[IN_TWO_HOURS]),
        ]
    )
    availability_list.subtract(
        TimeRange(
            start=time[IN_THIRTY_MINUTES] - FIVE_MINUTES,
            end=time[IN_ONE_HOUR] + FIVE_MINUTES,
        )
    )
    assert len(availability_list.availability) == 2
    assert availability_list.availability[0].start == time[NOW]
    assert (
        availability_list.availability[0].end == time[IN_THIRTY_MINUTES] - FIVE_MINUTES
    )
    assert availability_list.availability[1].start == time[IN_ONE_HOUR] + FIVE_MINUTES
    assert availability_list.availability[1].end == time[IN_TWO_HOURS]


def test_filter_time_ranges_below(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[NOW] + FIVE_MINUTES),
            TimeRange(start=time[NOW] + FIVE_MINUTES, end=time[NOW] + THIRTY_MINUTES),
        ]
    )
    assert len(availability_list.availability) == 2
    availability_list.filter_time_ranges_below(FIVE_MINUTES)
    assert len(availability_list.availability) == 2
    availability_list.filter_time_ranges_below(FIVE_MINUTES + timedelta(seconds=1))
    assert len(availability_list.availability) == 1
    assert availability_list.availability[0].start == time[NOW] + FIVE_MINUTES


def test_total_duration_empty(time: dict[str, datetime]):
    none = AvailabilityList(availability=[])
    assert none.total_duration() == timedelta(0)


def test_total_duration_multiple(time: dict[str, datetime]):
    availability_list = AvailabilityList(
        availability=[
            TimeRange(start=time[NOW], end=time[NOW] + FIVE_MINUTES),
            TimeRange(start=time[NOW] + FIVE_MINUTES, end=time[NOW] + THIRTY_MINUTES),
        ]
    )
    assert availability_list.total_duration() == timedelta(minutes=30)
