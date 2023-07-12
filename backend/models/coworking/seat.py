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
