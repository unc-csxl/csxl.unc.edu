"""Tests for the room reservation block migration backfill."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.entities.coworking import RoomReservationBlockEntity
from backend.migrations.versions.d4a7b2c91f10_add_room_reservation_blocks import (
    INITIAL_ROOM_RESERVATION_BLOCKS,
    _backfill_room_reservation_blocks,
)
from ..room_data import fake_data_fixture as insert_order_0  # noqa: F401


def test_initial_policy_inventory_is_bounded() -> None:
    assert len(INITIAL_ROOM_RESERVATION_BLOCKS) == 15

    temporary = [
        block
        for block in INITIAL_ROOM_RESERVATION_BLOCKS
        if block["label"] == "COMP211 Check-off"
    ]
    long_lived = [
        block
        for block in INITIAL_ROOM_RESERVATION_BLOCKS
        if block["label"] == "Office Hours"
    ]

    assert len(temporary) == 6
    assert len(long_lived) == 9
    assert {block["starts_on"] for block in temporary} == {
        date(2026, 9, 1),
        date(2026, 9, 2),
        date(2026, 9, 3),
        date(2026, 9, 4),
    }
    assert all(block["ends_on"] == block["starts_on"] for block in temporary)
    assert all(block["ends_on"] is None for block in long_lived)


def test_backfill_skips_rooms_missing_from_the_database(session: Session) -> None:
    _backfill_room_reservation_blocks(session.connection())
    session.expire_all()

    blocks = session.scalars(
        select(RoomReservationBlockEntity).order_by(RoomReservationBlockEntity.id)
    ).all()

    assert len(blocks) == 8
    assert {block.room_id for block in blocks} == {"SN135", "SN141"}
    assert sum(block.label == "COMP211 Check-off" for block in blocks) == 1
