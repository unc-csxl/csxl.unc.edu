from enum import Enum
from datetime import datetime
from ...models import User
from .room import Room
from .seat import Seat
from .time_range import TimeRange


class ReservationState(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"


class ReservationRequest(TimeRange):
    id: int | None = None
    users: list[User] = []
    seats: list[Seat] = []


class Reservation(ReservationRequest):
    state: ReservationState
    room: Room | None = None
    created_at: datetime
    updated_at: datetime
    walkin: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ReservationDetails(Reservation):
    errors: list[str] = []
    extendable: bool = False
    extendable_at: datetime | None
    extendable_until: datetime | None
