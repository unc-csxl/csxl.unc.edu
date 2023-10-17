"""Represent the status of the XL coworking space."""

from pydantic import BaseModel

from .reservation import Reservation
from .availability import SeatAvailability
from .operating_hours import OperatingHours


class Status(BaseModel):
    """The status of the XL coworking space, including reservations, for a given user."""

    my_reservations: list[Reservation]
    seat_availability: list[SeatAvailability]
    operating_hours: list[OperatingHours]
