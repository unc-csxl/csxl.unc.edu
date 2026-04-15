"""Tests for Coworking Rooms Service."""

import pytest
from sqlalchemy.orm import Session

from ....entities import RoomEntity
from ....entities.coworking import SeatEntity
from ....models import RoomDetails
from ....models.coworking import SeatDetails
from ....services.coworking import SeatService
from .fixtures import seat_svc

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def arrange_seats(session: Session) -> list[SeatDetails]:
    room = RoomDetails(
        id="SN156",
        building="Sitterson",
        room="156",
        nickname="The XL",
        capacity=40,
        reservable=False,
        seats=[],
    )
    seats = [
        SeatDetails(
            id=1,
            title="Standing Monitor 00",
            shorthand="M00",
            reservable=True,
            has_monitor=True,
            sit_stand=True,
            x=0,
            y=0,
            room=room.to_room(),
        ),
        SeatDetails(
            id=2,
            title="Standing Monitor 01",
            shorthand="M01",
            reservable=False,
            has_monitor=True,
            sit_stand=True,
            x=0,
            y=1,
            room=room.to_room(),
        ),
        SeatDetails(
            id=3,
            title="Monitor 10",
            shorthand="M10",
            reservable=True,
            has_monitor=True,
            sit_stand=False,
            x=1,
            y=0,
            room=room.to_room(),
        ),
        SeatDetails(
            id=4,
            title="Monitor 11",
            shorthand="M11",
            reservable=False,
            has_monitor=True,
            sit_stand=False,
            x=1,
            y=1,
            room=room.to_room(),
        ),
    ]

    session.add(RoomEntity.from_model(room))
    session.add_all(SeatEntity.from_model(seat) for seat in seats)
    session.commit()

    return seats


def test_list(session: Session, seat_svc: SeatService):
    expected_seats = arrange_seats(session)

    seats = seat_svc.list()
    assert len(seats) == len(expected_seats)
    assert [seat.id for seat in seats] == [seat.id for seat in expected_seats]
    assert all(isinstance(seat, SeatDetails) for seat in seats)
