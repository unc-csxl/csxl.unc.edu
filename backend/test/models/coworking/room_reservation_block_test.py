"""Unit tests for room reservation block models."""

from datetime import date, time

import pytest
from pydantic import ValidationError

from ....models.coworking import (
    NewRoomReservationBlock,
    RoomReservationBlockWeekday,
)


def make_block(**changes) -> NewRoomReservationBlock:
    values = {
        "room_id": "SN147",
        "label": "COMP211 Check-off",
        "weekday": RoomReservationBlockWeekday.TUESDAY,
        "start_time": time(11, 30),
        "end_time": time(17),
        "starts_on": date(2026, 9, 1),
        "ends_on": date(2026, 9, 1),
    }
    values.update(changes)
    return NewRoomReservationBlock(**values)


def test_valid_block_strips_label():
    block = make_block(label="  COMP211 Check-off  ")

    assert block.label == "COMP211 Check-off"
    assert block.enabled is True
    assert block.weekday == RoomReservationBlockWeekday.TUESDAY


@pytest.mark.parametrize("label", ["", "   "])
def test_label_is_required(label: str):
    with pytest.raises(ValidationError, match="label must not be empty"):
        make_block(label=label)


@pytest.mark.parametrize("field", ["start_time", "end_time"])
def test_times_must_align_to_half_hour(field: str):
    with pytest.raises(ValidationError, match="half-hour boundary"):
        make_block(**{field: time(11, 15)})


def test_end_time_must_follow_start_time():
    with pytest.raises(ValidationError, match="end_time must be greater"):
        make_block(start_time=time(17), end_time=time(11, 30))


def test_end_date_must_not_precede_start_date():
    with pytest.raises(ValidationError, match="ends_on must not precede"):
        make_block(
            starts_on=date(2026, 9, 2),
            ends_on=date(2026, 9, 1),
        )


def test_indefinite_block_is_valid():
    block = make_block(ends_on=None)

    assert block.ends_on is None
