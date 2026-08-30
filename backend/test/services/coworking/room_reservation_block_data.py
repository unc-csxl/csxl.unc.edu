"""Representative standing room reservations for development resets."""

from datetime import date, time

from sqlalchemy.orm import Session

from ....entities.coworking import RoomReservationBlockEntity
from ....models.coworking import (
    NewRoomReservationBlock,
    RoomReservationBlockWeekday,
)


blocks = [
    NewRoomReservationBlock(
        room_id="SN141",
        label="Office Hours",
        weekday=RoomReservationBlockWeekday.MONDAY,
        start_time=time(10),
        end_time=time(12),
        starts_on=date(2026, 8, 30),
    ),
    NewRoomReservationBlock(
        room_id="SN141",
        label="COMP211 Check-off",
        weekday=RoomReservationBlockWeekday.WEDNESDAY,
        start_time=time(13, 30),
        end_time=time(15, 30),
        starts_on=date(2026, 9, 2),
        ends_on=date(2026, 9, 2),
    ),
]


def insert_fake_data(session: Session) -> None:
    """Insert representative rules after room data has been loaded."""
    session.add_all(
        [RoomReservationBlockEntity.from_new_model(block) for block in blocks]
    )
