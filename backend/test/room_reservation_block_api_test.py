"""Unit tests for room reservation block API delegation."""

from datetime import date, time

from ..api.coworking.room_reservation_block import (
    create_room_reservation_block,
    delete_room_reservation_block,
    get_room_reservation_block,
    get_room_reservation_blocks,
    update_room_reservation_block,
)
from ..models.coworking import (
    NewRoomReservationBlock,
    RoomReservationBlockWeekday,
)


class StubRoomReservationBlockService:
    def __init__(self):
        self.result = object()
        self.calls = []

    def list_rules(self, *args):
        self.calls.append(("list", *args))
        return [self.result]

    def get(self, *args):
        self.calls.append(("get", *args))
        return self.result

    def create(self, *args):
        self.calls.append(("create", *args))
        return self.result

    def update(self, *args):
        self.calls.append(("update", *args))
        return self.result

    def delete(self, *args):
        self.calls.append(("delete", *args))


def make_block() -> NewRoomReservationBlock:
    return NewRoomReservationBlock(
        room_id="SN141",
        label="COMP211 Check-off",
        weekday=RoomReservationBlockWeekday.WEDNESDAY,
        start_time=time(13, 30),
        end_time=time(15, 30),
        starts_on=date(2026, 9, 2),
    )


def test_read_routes_delegate_to_service():
    service = StubRoomReservationBlockService()
    subject = object()

    assert get_room_reservation_blocks(
        "SN141", True, subject=subject, block_svc=service
    ) == [service.result]
    assert (
        get_room_reservation_block(7, subject=subject, block_svc=service)
        is service.result
    )
    assert service.calls == [
        ("list", subject, "SN141", True),
        ("get", subject, 7),
    ]


def test_write_routes_delegate_to_service():
    service = StubRoomReservationBlockService()
    subject = object()
    block = make_block()

    assert (
        create_room_reservation_block(block, subject=subject, block_svc=service)
        is service.result
    )
    assert (
        update_room_reservation_block(7, block, subject=subject, block_svc=service)
        is service.result
    )
    assert delete_room_reservation_block(7, subject=subject, block_svc=service) is None
    assert service.calls == [
        ("create", subject, block),
        ("update", subject, 7, block),
        ("delete", subject, 7),
    ]
