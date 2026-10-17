"""Time range model for coworking module."""

from datetime import datetime, timedelta
from typing import Self
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ValidationInfo, field_validator

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TimeRange(BaseModel):
    """A time range with a start and end."""

    start: datetime
    end: datetime

    @field_validator("start", "end")
    @classmethod
    def remove_timezone(cls, value: datetime):
        """Store Eastern wall time; naive inputs already represent facility time."""
        if value.tzinfo is not None:
            return value.astimezone(ZoneInfo("America/New_York")).replace(tzinfo=None)
        return value

    @field_validator("end")
    @classmethod
    def check_end_greater_than_start(cls, v: datetime, info: ValidationInfo):
        if "start" in info.data and v <= info.data["start"]:
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
