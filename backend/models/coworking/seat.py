"""Seat models a physical working space in the coworking space."""

from pydantic import BaseModel

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Seat(BaseModel):
    id: int | None = None
    title: str
    shorthand: str
    reservable: bool
    has_monitor: bool
    sit_stand: bool
    x: int
    y: int


class SeatPartial(Seat, BaseModel):
    title: str | None = None
    shorthand: str | None = None
    reservable: bool | None = None
    has_monitor: bool | None = None
    sit_stand: bool | None = None
    x: int | None = None
    y: int | None = None


class SeatIdentity(SeatPartial, BaseModel):
    id: int
