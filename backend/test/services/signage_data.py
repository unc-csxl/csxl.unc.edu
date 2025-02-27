"""One more additional reservation data for signage tests."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from ...entities.coworking import ReservationEntity
from ...models.coworking import Reservation, ReservationState, ReservationRequest
from time import *

from .core_data import user_data

from . import room_data

__authors__ = ["Will Zahrt", "Andrew Lockard"]


now = datetime.now()

current_reservation = Reservation(
    id=8,
    start=now - timedelta(hours=1),
    end=now + timedelta(hours=2),
    created_at=now - timedelta(hours=2),
    updated_at=now - timedelta(hours=1, minutes=30),
    walkin=False,
    room=room_data.pair_a,
    state=ReservationState.CHECKED_IN,
    users=[user_data.root],
    seats=[],
)

checked_out_reservation_1 = Reservation(
    id=9,
    start=now - timedelta(hours=2),
    end=now - timedelta(hours=1),
    created_at=now - timedelta(hours=2),
    updated_at=now - timedelta(hours=1),
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_OUT,
    users=[user_data.ambassador],
    seats=[],
)

checked_out_reservation_2 = Reservation(
    id=10,
    start=now - timedelta(hours=4),
    end=now - timedelta(hours=3),
    created_at=now - timedelta(hours=4),
    updated_at=now - timedelta(hours=3),
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_OUT,
    users=[user_data.ambassador],
    seats=[],
)

checked_out_reservation_3 = Reservation(
    id=11,
    start=now - timedelta(hours=2),
    end=now - timedelta(hours=1),
    created_at=now - timedelta(hours=2),
    updated_at=now - timedelta(hours=1),
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_OUT,
    users=[user_data.root],
    seats=[],
)

checked_out_reservation_4 = Reservation(
    id=12,
    start=now - timedelta(hours=4),
    end=now - timedelta(hours=3),
    created_at=now - timedelta(hours=4),
    updated_at=now - timedelta(hours=3),
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_OUT,
    users=[user_data.root],
    seats=[],
)

checked_out_reservation_5 = Reservation(
    id=13,
    start=now - timedelta(hours=4),
    end=now - timedelta(hours=3),
    created_at=now - timedelta(hours=4),
    updated_at=now - timedelta(hours=3),
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_OUT,
    users=[user_data.user],
    seats=[],
)

reservations = [
    current_reservation,
    checked_out_reservation_1,
    checked_out_reservation_2,
    checked_out_reservation_3,
    checked_out_reservation_4,
    checked_out_reservation_5,
]


def insert_fake_data(session: Session):
    for model in reservations:
        entity = ReservationEntity.from_model(model, session)
        session.add(entity)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Inserts additional data needed to fully test signage."""
    insert_fake_data(session)
    session.commit()
