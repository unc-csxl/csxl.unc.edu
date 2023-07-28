"""Models for the availability of rooms and seats over a time range."""

from pydantic import BaseModel, validator

from .room import Room
from .seat import SeatIdentity
from .time_range import TimeRange
from .availability_list import AvailabilityList


class RoomAvailability(Room, AvailabilityList):
    """A room that is available for a given time range."""

    ...


class SeatAvailability(SeatIdentity, AvailabilityList):
    """A seat that is available for a given time range."""

    ...
