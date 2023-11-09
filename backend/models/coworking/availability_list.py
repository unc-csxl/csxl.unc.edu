"""Utility class for tracking availability over TimeRanges.

Handles logic for constraining availability within a bounds, removing availability, and so on.
"""

from datetime import timedelta
from pydantic import BaseModel, field_validator
from .time_range import TimeRange

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class AvailabilityList(BaseModel):
    """A list of availability for a given time range.

    The availability list must be sorted by start time.

    No two avialability ranges may overlap.
    """

    availability: list[TimeRange]

    @field_validator("availability")
    def check_sorted(cls, v):
        if any(v[i].start > v[i + 1].start for i in range(len(v) - 1)):
            raise ValueError("availability list must be sorted by start time")
        return v

    @field_validator("availability")
    def check_no_overlaps(cls, v):
        if any(v[i].end > v[i + 1].start for i in range(len(v) - 1)):
            raise ValueError("availability list must not contain overlapping ranges")
        return v

    def constrain(self, bounds: TimeRange) -> None:
        """Constrains availability within given bounds.

        Args:
            bounds (TimeRange): The bounds to constrain availability within.

        Returns:
            None"""
        front = 0
        while (
            front < len(self.availability)
            and self.availability[front].end <= bounds.start
        ):
            front += 1

        self.availability = self.availability[front:]
        if len(self.availability) > 0:
            if self.availability[0].start < bounds.start:
                self.availability[0].start = bounds.start
        else:
            return

        back = len(self.availability) - 1
        while back >= 0 and self.availability[back].start >= bounds.end:
            back -= 1

        self.availability = self.availability[: back + 1]
        if len(self.availability) > 0:
            if self.availability[-1].end > bounds.end:
                self.availability[-1].end = bounds.end

    def subtract(self, block: TimeRange) -> None:
        """Removes availability that overlaps a given block."""

        if len(self.availability) == 0:
            return

        if block.start >= self.availability[-1].end:
            return

        if block.end <= self.availability[0].start:
            return

        # Find the first availability range that overalps the block.
        front = 0
        while front < len(self.availability) and not block.overlaps(
            self.availability[front]
        ):
            front += 1

        end = front + 1
        while end < len(self.availability) and block.overlaps(self.availability[end]):
            end += 1

        availability: list[TimeRange] = self.availability[:front]
        for i in range(front, end):
            availability += self.availability[i].subtract(block)
        availability += self.availability[end:]

        self.availability = availability

    def filter_time_ranges_below(self, minimum: timedelta) -> None:
        """Remove all TimeRanges that are not at least the minimum timedelta.

        Args:
            minimum (timedelta): The threshold of which to remove beneath.

        Returns:
            None"""
        self.availability = [
            time_range
            for time_range in self.availability
            if time_range.duration() >= minimum
        ]

    def total_duration(self) -> timedelta:
        """Sum the durations of all availability.

        Returns:
            timedelta - Total amount of time available in this list."""
        if len(self.availability) == 0:
            return timedelta(0)

        durations = [time_range.duration() for time_range in self.availability]
        total = durations[0]
        for i in range(1, len(self.availability)):
            total += durations[i]

        return total
