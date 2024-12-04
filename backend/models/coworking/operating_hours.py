"""Models open hours of the XL."""

from pydantic import BaseModel
from .time_range import TimeRange
from datetime import datetime, date


__authors__ = ["Kris Jordan, Yuvraj Jain, David Foss"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OperatingHoursRecurrence(BaseModel):
    start_date: date
    end_date: date

    # Bitmask saved as an int
    recurs_on: int


class OperatingHours(TimeRange, BaseModel):
    """The operating hours of the XL."""

    id: int | None = None

    recurrence_id: int | None = None


class OperatingHoursDraft(TimeRange, BaseModel):
    """Data for an operating hours draft (for creation and editing)."""

    recurrence: OperatingHoursRecurrence | None = None
