"""Models for standing room reservation blocks."""

from datetime import date, datetime, time
from enum import IntEnum
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator


class RoomReservationBlockWeekday(IntEnum):
    """Weekdays using the same numbering as ``date.weekday``."""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class NewRoomReservationBlock(BaseModel):
    """A weekly room reservation block before it is persisted."""

    room_id: str
    label: str = Field(max_length=120)
    weekday: RoomReservationBlockWeekday
    start_time: time
    end_time: time
    starts_on: date
    ends_on: date | None = None
    enabled: bool = True

    @field_validator("label")
    @classmethod
    def validate_label(cls, value: str) -> str:
        label = value.strip()
        if not label:
            raise ValueError("label must not be empty")
        return label

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_half_hour(cls, value: time) -> time:
        if value.minute not in (0, 30) or value.second != 0 or value.microsecond != 0:
            raise ValueError("times must align to a half-hour boundary")
        return value

    @model_validator(mode="after")
    def validate_ranges(self) -> Self:
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        if self.ends_on is not None and self.ends_on < self.starts_on:
            raise ValueError("ends_on must not precede starts_on")
        return self


class RoomReservationBlock(NewRoomReservationBlock):
    """A persisted weekly room reservation block."""

    id: int
    created_at: datetime
    updated_at: datetime


class RoomReservationBlockOccurrence(BaseModel):
    """A room reservation block expanded onto a calendar date."""

    id: int
    room_id: str
    label: str
    start: datetime
    end: datetime
