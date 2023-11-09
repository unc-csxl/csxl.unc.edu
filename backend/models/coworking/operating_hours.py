"""Models open hours of the XL."""


from pydantic import BaseModel
from .time_range import TimeRange


class OperatingHours(TimeRange, BaseModel):
    """The operating hours of the XL."""

    id: int | None = None
