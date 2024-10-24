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

__authors__ = ["Will Zahrt"]


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


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session, time: dict[str, datetime]):
    """Inserts additional data needed to fully test signage."""
    insert_fake_data(session, time)
    session.commit()


def insert_fake_data(session: Session, time: dict[str, datetime]):
    entity = ReservationEntity.from_model(current_reservation)
    session.add(entity)
