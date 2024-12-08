"""Models open hours of the XL."""

from pydantic import BaseModel
from .time_range import TimeRange
from datetime import datetime, date


__authors__ = ["Kris Jordan", "Yuvraj Jain", "David Foss"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OperatingHoursRecurrence(BaseModel):
    id: int | None = None

    end_date: datetime

    # Bitmask saved as an int
    # Monday is 0, Sunday is 6 (following python datetime standard)
    recurs_on: int


class OperatingHours(TimeRange, BaseModel):
    """The operating hours of the XL."""

    id: int

    recurrence_id: int | None = None
    recurrence: OperatingHoursRecurrence | None = None


class OperatingHoursDraft(TimeRange, BaseModel):
    """Data for an operating hours draft (for creation and editing)."""

    id: int | None = None

    recurrence: OperatingHoursRecurrence | None = None
