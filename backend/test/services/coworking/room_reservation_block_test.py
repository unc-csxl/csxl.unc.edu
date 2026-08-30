"""Tests for the room reservation block service."""

from datetime import date, datetime, time

import pytest
from sqlalchemy.orm import Session

from ....entities.coworking import ReservationEntity
from ....models.coworking import (
    NewRoomReservationBlock,
    ReservationState,
    RoomReservationBlockWeekday,
)
from ....services import PermissionService
from ....services.coworking import RoomReservationBlockService
from ....services.coworking.exceptions import RoomReservationBlockConflictException
from ....services.exceptions import UserPermissionException
from ..core_data import setup_insert_data_fixture as insert_order_0  # noqa: F401
from ..room_data import fake_data_fixture as insert_order_1  # noqa: F401
from .. import user_data


@pytest.fixture()
def room_reservation_block_svc(session: Session) -> RoomReservationBlockService:
    return RoomReservationBlockService(session, PermissionService(session))


def make_block(**changes) -> NewRoomReservationBlock:
    values = {
        "room_id": "SN141",
        "label": "COMP211 Check-off",
        "weekday": RoomReservationBlockWeekday.WEDNESDAY,
        "start_time": time(13, 30),
        "end_time": time(15, 30),
        "starts_on": date(2026, 9, 2),
        "ends_on": date(2026, 12, 2),
    }
    values.update(changes)
    return NewRoomReservationBlock(**values)


def test_create_get_list_and_schedule(
    room_reservation_block_svc: RoomReservationBlockService,
):
    created = room_reservation_block_svc.create(user_data.root, make_block())

    assert room_reservation_block_svc.get(user_data.root, created.id) == created
    assert room_reservation_block_svc.list_rules(user_data.root) == [created]

    occurrence = room_reservation_block_svc.schedule(date(2026, 9, 9))[0]
    assert occurrence.label == "COMP211 Check-off"
    assert occurrence.start == datetime(2026, 9, 9, 13, 30)
    assert occurrence.end == datetime(2026, 9, 9, 15, 30)
    assert room_reservation_block_svc.schedule(date(2026, 9, 10)) == []


def test_overlapping_rule_is_rejected(
    room_reservation_block_svc: RoomReservationBlockService,
):
    room_reservation_block_svc.create(user_data.root, make_block())

    with pytest.raises(RoomReservationBlockConflictException, match="COMP211"):
        room_reservation_block_svc.create(
            user_data.root,
            make_block(label="Another Event", start_time=time(15), end_time=time(16)),
        )


def test_adjacent_and_nonconcurrent_rules_are_allowed(
    room_reservation_block_svc: RoomReservationBlockService,
):
    room_reservation_block_svc.create(user_data.root, make_block())

    adjacent = room_reservation_block_svc.create(
        user_data.root,
        make_block(label="Adjacent", start_time=time(15, 30), end_time=time(16)),
    )
    later_term = room_reservation_block_svc.create(
        user_data.root,
        make_block(
            label="Next Term",
            starts_on=date(2026, 12, 3),
            ends_on=date(2027, 5, 1),
        ),
    )

    assert adjacent.id != later_term.id


def test_disabled_rule_does_not_block_or_appear_by_default(
    room_reservation_block_svc: RoomReservationBlockService,
):
    disabled = room_reservation_block_svc.create(
        user_data.root, make_block(enabled=False)
    )

    assert room_reservation_block_svc.schedule(date(2026, 9, 9)) == []
    assert room_reservation_block_svc.list_rules(user_data.root) == []
    assert room_reservation_block_svc.list_rules(
        user_data.root, include_disabled=True
    ) == [disabled]


def test_active_reservation_conflict_is_rejected(
    session: Session,
    room_reservation_block_svc: RoomReservationBlockService,
):
    session.add(
        ReservationEntity(
            start=datetime(2026, 9, 9, 14),
            end=datetime(2026, 9, 9, 15),
            state=ReservationState.CONFIRMED,
            walkin=False,
            room_id="SN141",
            users=[],
            seats=[],
        )
    )
    session.commit()

    with pytest.raises(RoomReservationBlockConflictException, match="reservation"):
        room_reservation_block_svc.create(user_data.root, make_block())


def test_update_and_delete(
    room_reservation_block_svc: RoomReservationBlockService,
):
    created = room_reservation_block_svc.create(user_data.root, make_block())
    updated = room_reservation_block_svc.update(
        user_data.root, created.id, make_block(label="Updated label")
    )

    assert updated.label == "Updated label"

    room_reservation_block_svc.delete(user_data.root, created.id)

    assert room_reservation_block_svc.list_rules(user_data.root) == []


def test_student_cannot_manage_rules(
    room_reservation_block_svc: RoomReservationBlockService,
):
    with pytest.raises(UserPermissionException):
        room_reservation_block_svc.create(user_data.user, make_block())
