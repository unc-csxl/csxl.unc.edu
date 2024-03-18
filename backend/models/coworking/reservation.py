from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from ...models.user import User, UserIdentity
from ..room import Room, RoomPartial
from .seat import Seat, SeatIdentity
from .time_range import TimeRange

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ReservationState(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"


class ReservationIdentity(BaseModel):
    id: int


class ReservationRequest(TimeRange):
    users: list[UserIdentity] = []
    seats: list[SeatIdentity] = []
    room: RoomPartial | None = None


class Reservation(ReservationIdentity, TimeRange):
    state: ReservationState
    users: list[User] = []
    seats: list[Seat] = []
    room: Room | None = None
    walkin: bool = False
    created_at: datetime
    updated_at: datetime


class ReservationMapDetails(BaseModel):
    reserved_date_map: dict[str, list[int]] = {}
    operating_hours_start: datetime | None = None
    operating_hours_end: datetime | None = None
    number_of_time_slots: int | None = None


class ReservationPartial(Reservation, BaseModel):
    start: datetime | None = None
    end: datetime | None = None
    state: ReservationState | None = None
    users: list[User] | None = None
    seats: list[Seat] | None = None
    room: Room | None = None
    walkin: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ReservationDetails(Reservation):
    errors: list[str] = []
    extendable: bool = False
    extendable_at: datetime | None
    extendable_until: datetime | None
