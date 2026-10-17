"""Models open hours of the XL."""

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, field_serializer

from .time_range import TimeRange

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OperatingHours(TimeRange, BaseModel):
    """The operating hours of the XL."""

    id: int | None = None

    @field_serializer("start", "end", when_used="json")
    def serialize_time(self, value: datetime) -> str:
        """Include the facility's UTC offset so browsers interpret hours correctly."""
        return value.replace(tzinfo=ZoneInfo("America/New_York")).isoformat()
