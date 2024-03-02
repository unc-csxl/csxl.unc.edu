"""Time range model for coworking module."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator, ValidationInfo, validator
from typing import Self

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TimeRange(BaseModel):
    """A time range with a start and end."""

    start: datetime
    end: datetime

    @field_validator("start", "end", mode="before")
    @classmethod
    def remove_timezone(cls, value: datetime):
        if type(value) == str:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            dt = dt.astimezone(ZoneInfo("America/New_York"))
            dt = dt.replace(tzinfo=None)
            return dt
        return value

    @field_validator("end")
    @classmethod
    def check_end_greater_than_start(cls, v: datetime, info: ValidationInfo):
        if v <= info.data["start"]:
            raise ValueError("end must be greater than start")
        return v

    def overlaps(self, other: Self) -> bool:
        """Returns True if this time range overlaps another.

        Args:
            other (TimeRange): The other time range to check for overlap.

        Returns:
            bool: True if this time range overlaps another.
        """
        return self.start < other.end and other.start < self.end

    def subtract(self, other: Self) -> list[Self]:
        """Subtracts another time range from this one.

        Args:
            other (TimeRange): The time range to subtract.

        Returns:
            list[TimeRange]: The resulting time ranges after subtraction.
        """
        if not self.overlaps(other):
            return [self]

        results = []

        if self.start < other.start:
            results.append(TimeRange(start=self.start, end=other.start))

        if self.end > other.end:
            results.append(TimeRange(start=other.end, end=self.end))

        return results

    def duration(self) -> timedelta:
        """Compute the duration of a TimeRange.

        Returns:
            timedelta: The amount of time between end and start."""
        return self.end - self.start
