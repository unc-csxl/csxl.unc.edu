"""Persistence tests for room reservation block entities."""

from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from ....entities import RoomEntity
from ....entities.coworking import RoomReservationBlockEntity
from ....models import RoomDetails
from ....models.coworking import (
    NewRoomReservationBlock,
    RoomReservationBlockWeekday,
)


def add_room(session: Session) -> None:
    session.add(
        RoomEntity.from_model(
            RoomDetails(
                id="SN147",
                building="Sitterson",
                room="147",
                nickname="Group D",
                capacity=8,
                reservable=True,
                seats=[],
            )
        )
    )


def test_entity_round_trip(session: Session):
    add_room(session)
    block = NewRoomReservationBlock(
        room_id="SN147",
        label="COMP211 Check-off",
        weekday=RoomReservationBlockWeekday.TUESDAY,
        start_time=time(11, 30),
        end_time=time(17),
        starts_on=date(2026, 9, 1),
        ends_on=date(2026, 9, 1),
    )
    session.add(RoomReservationBlockEntity.from_new_model(block))
    session.commit()

    entity = session.scalar(select(RoomReservationBlockEntity))

    assert entity is not None
    assert entity.room.id == "SN147"
    assert entity.to_model().label == "COMP211 Check-off"
    assert entity.to_model().weekday == RoomReservationBlockWeekday.TUESDAY
    assert entity.created_at is not None
    assert entity.updated_at is not None


def test_entity_persists_disabled_indefinite_block(session: Session):
    add_room(session)
    entity = RoomReservationBlockEntity.from_new_model(
        NewRoomReservationBlock(
            room_id="SN147",
            label="Department Meeting",
            weekday=RoomReservationBlockWeekday.FRIDAY,
            start_time=time(15),
            end_time=time(16),
            starts_on=date(2026, 9, 4),
            enabled=False,
        )
    )
    session.add(entity)
    session.commit()
    session.expire_all()

    persisted = session.get(RoomReservationBlockEntity, entity.id)

    assert persisted is not None
    assert persisted.enabled is False
    assert persisted.ends_on is None
