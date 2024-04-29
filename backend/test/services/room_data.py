"""Room data for tests."""

import pytest
from sqlalchemy.orm import Session
from ...entities import RoomEntity
from ...models import RoomDetails
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


the_xl = RoomDetails(
    id="SN156",
    building="Sitterson",
    room="156",
    nickname="The XL",
    capacity=40,
    reservable=False,
    seats=[],
)

group_a = RoomDetails(
    id="SN135",
    building="Sitterson",
    room="135",
    nickname="Group A",
    capacity=4,
    reservable=True,
    seats=[],
)

group_b = RoomDetails(
    id="SN137",
    building="Sitterson",
    room="137",
    nickname="Group B",
    capacity=4,
    reservable=True,
    seats=[],
)

group_c = RoomDetails(
    id="SN141",
    building="Sitterson",
    room="141",
    nickname="Group C",
    capacity=6,
    reservable=True,
    seats=[],
)

pair_a = RoomDetails(
    id="SN139",
    building="Sitterson",
    room="139",
    nickname="Pair A",
    capacity=2,
    reservable=True,
    seats=[],
)

new_room = RoomDetails(
    id="FB009",
    building="Fred Brooks",
    room="009",
    nickname="Large Room",
    capacity=100,
    reservable=False,
    seats=[],
)

edited_xl = RoomDetails(
    id="SN156",
    building="Sitterson",
    room="156",
    nickname="The CSXL",
    capacity=100,
    reservable=False,
    seats=[],
)

rooms = [the_xl, group_a, group_b, group_c, pair_a]


def insert_fake_data(session: Session):
    for room in rooms:
        entity = RoomEntity.from_model(room)
        session.add(entity)

    # Don't need to reset room sequence because its ID is a string


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
