"""Seat models a physical working space in the coworking space."""

from pydantic import BaseModel

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SeatIdentity(BaseModel):
    id: int


class Seat(SeatIdentity, BaseModel):
    title: str
    shorthand: str
    reservable: bool
    has_monitor: bool
    sit_stand: bool
    x: int
    y: int


class NewSeat(Seat, BaseModel):
    id: int | None = None
