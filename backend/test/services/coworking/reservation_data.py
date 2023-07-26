"""Reservation data for tests."""

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from ....entities.coworking import ReservationEntity
from ....models.coworking import Reservation, ReservationState, ReservationRequest
from .times import *

from . import user_data
from . import seat_data
from . import operating_hours_data


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Active reservation for 00 starts 30 minutes ago, ends in an hour
reservation_1 = Reservation(
    id=1,
    start=THIRTY_MINUTES_AGO,
    end=IN_THIRTY_MINUTES,
    created_at=THIRTY_MINUTES_AGO,
    updated_at=THIRTY_MINUTES_AGO,
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_IN,
    users=[user_data.user],
    seats=[seat_data.monitor_seat_00],
)

# Reservation ended early (checked out)
reservation_2 = Reservation(
    id=2,
    start=THIRTY_MINUTES_AGO,
    end=IN_THIRTY_MINUTES,
    created_at=THIRTY_MINUTES_AGO,
    updated_at=THIRTY_MINUTES_AGO,
    walkin=False,
    room=None,
    state=ReservationState.CHECKED_OUT,
    users=[user_data.ambassador],
    seats=[seat_data.monitor_seat_01],
)

# Reservation cancelled
reservation_3 = Reservation(
    id=3,
    start=THIRTY_MINUTES_AGO,
    end=IN_THIRTY_MINUTES,
    created_at=THIRTY_MINUTES_AGO,
    updated_at=THIRTY_MINUTES_AGO,
    walkin=False,
    room=None,
    state=ReservationState.CANCELLED,
    users=[user_data.root],
    seats=[seat_data.monitor_seat_10],
)

# Future reservations for a half-hour toward end of day, with half hour til close
reservation_4 = Reservation(
    id=4,
    start=operating_hours_data.today.end - ONE_HOUR,
    end=operating_hours_data.today.end - THIRTY_MINUTES,
    created_at=NOW,
    updated_at=NOW,
    walkin=False,
    room=None,
    state=ReservationState.CONFIRMED,
    users=[user_data.root, user_data.ambassador],
    seats=[seat_data.reservable_seats[0], seat_data.reservable_seats[1]],
)

active_reservations = [reservation_1]
reservations = [reservation_1, reservation_2, reservation_3, reservation_4]


def test_request(overrides=None) -> ReservationRequest:
    # Generate default values for the Reservation
    reservation_data = {
        "start": datetime.now(),
        "end": datetime.now() + THIRTY_MINUTES,
        "users": [user_data.ambassador],
        "seats": [seat_data.monitor_seat_01],
    }

    # Override the defaults if provided in the overrides dictionary
    if overrides:
        reservation_data.update(overrides)

    # Create the Reservation model
    return ReservationRequest(**reservation_data)


def insert_fake_data(session: Session):
    for reservation in reservations:
        entity = ReservationEntity.from_model(reservation, session)
        session.add(entity)
    session.execute(
        text(
            f"ALTER SEQUENCE {ReservationEntity.__table__}_id_seq RESTART WITH {len(reservations) + 1}"
        )
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
