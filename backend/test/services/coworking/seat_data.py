"""Seat data for tests."""

import pytest
from sqlalchemy import delete
from sqlalchemy.orm import Session
from ....entities.coworking import SeatEntity
from ....models.coworking.seat_details import SeatDetails

from ..reset_table_id_seq import reset_table_id_seq
from .room_data import the_xl

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

monitor_seat_00 = SeatDetails(
    id=1,
    title="Standing Monitor 00",
    shorthand="M00",
    reservable=True,
    has_monitor=True,
    sit_stand=True,
    x=0,
    y=0,
    room=the_xl.to_room(),
)

monitor_seat_01 = SeatDetails(
    id=2,
    title="Standing Monitor 01",
    shorthand="M01",
    reservable=False,
    has_monitor=True,
    sit_stand=True,
    x=0,
    y=1,
    room=the_xl.to_room(),
)
monitor_seat_10 = SeatDetails(
    id=3,
    title="Monitor 10",
    shorthand="M10",
    reservable=True,
    has_monitor=True,
    sit_stand=False,
    x=1,
    y=0,
    room=the_xl.to_room(),
)
monitor_seat_11 = SeatDetails(
    id=4,
    title="Monitor 11",
    shorthand="M11",
    reservable=False,
    has_monitor=True,
    sit_stand=False,
    x=1,
    y=1,
    room=the_xl.to_room(),
)
monitor_seats = [monitor_seat_00, monitor_seat_01, monitor_seat_10, monitor_seat_11]

# common_area_00 = SeatDetails(
#     id=20,
#     title="Common Area 00",
#     shorthand="C00",
#     reservable=False,
#     has_monitor=False,
#     sit_stand=False,
#     x=5,
#     y=0,
#     room=the_xl.to_room()
# )
# common_area_01 = SeatDetails(
#     id=21,
#     title="Common Area 01",
#     shorthand="C01",
#     reservable=False,
#     has_monitor=False,
#     sit_stand=False,
#     x=5,
#     y=1,
#     room=the_xl.to_room()
# )
# common_area_seats = [common_area_00, common_area_01]

# conference_table_00 = SeatDetails(
#     id=40,
#     title="Conference Table 01",
#     shorthand="G01",
#     reservable=True,
#     has_monitor=False,
#     sit_stand=False,
#     x=20,
#     y=20,
#     room=the_xl.to_room()
# )
# conference_table_01 = SeatDetails(
#     id=41,
#     title="Conference Table 02",
#     shorthand="G02",
#     reservable=False,
#     has_monitor=False,
#     sit_stand=False,
#     x=20,
#     y=21,
#     room=the_xl.to_room(),
# )
# conference_table_seats = [conference_table_00, conference_table_01]

seats = monitor_seats  # + common_area_seats + conference_table_seats

reservable_seats = [seat for seat in seats if seat.reservable]

unreservable_seats = [seat for seat in seats if not seat.reservable]


def insert_fake_data(session: Session):
    for seat in seats:
        entity = SeatEntity.from_model(seat)
        session.add(entity)
    reset_table_id_seq(session, SeatEntity, SeatEntity.id, len(seats) + 1)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()


def delete_all(session: Session):
    session.execute(delete(SeatEntity))