"""Models open hours of the XL."""


from pydantic import BaseModel
from .time_range import TimeRange


__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

class OperatingHours(TimeRange, BaseModel):
    """The operating hours of the XL."""

    id: int | None = None
