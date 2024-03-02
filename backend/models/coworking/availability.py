"""Models for the availability of rooms and seats over a time range."""

from enum import Enum
from pydantic import BaseModel, validator

from ..room import Room
from .seat import Seat
from .time_range import TimeRange
from .availability_list import AvailabilityList

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class RoomState(int, Enum):
    AVAILABLE = 0
    RESERVED = 1
    SELECTED = 2
    UNAVAILABLE = 3
    SUBJECT_RESERVED = 4


class RoomAvailability(Room, AvailabilityList):
    """A room that is available for a given time range."""

    ...


class SeatAvailability(Seat, AvailabilityList, BaseModel):
    """A seat that is available for a given time range."""

    ...
