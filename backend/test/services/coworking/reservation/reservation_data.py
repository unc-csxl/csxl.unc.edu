"""Reservation data for tests."""

import pytest
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from .....entities.coworking import ReservationEntity
from .....models.coworking import Reservation, ReservationState, ReservationRequest
from .....models.user import UserIdentity
from .....models.coworking.seat import SeatIdentity
from ..time import *

from ...core_data import user_data
from ...reset_table_id_seq import reset_table_id_seq
from .. import seat_data
from .. import operating_hours_data


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Active reservation for 00 starts 30 minutes ago, ends in an hour
reservation_1: Reservation
# Reservation ended early (checked out)
reservation_2: Reservation
# Reservation cancelled
reservation_3: Reservation
# Future reservations for a half-hour toward end of day, with half hour til close
reservation_4: Reservation
# Draft reservation for user tomorrow
reservation_5: Reservation

# Lists used for access
active_reservations: list[Reservation]
draft_reservations: list[Reservation]
confirmed_reservations: list[Reservation]
reservations: list[Reservation]


def instantiate_global_models(time: dict[str, datetime]):
    global reservation_1, reservation_2, reservation_3, reservation_4, reservation_5
    global active_reservations, reservations, draft_reservations, confirmed_reservations
    reservation_1 = Reservation(
        id=1,
        start=time[THIRTY_MINUTES_AGO],
        end=time[IN_THIRTY_MINUTES],
        created_at=time[THIRTY_MINUTES_AGO],
        updated_at=time[THIRTY_MINUTES_AGO],
        walkin=False,
        room=None,
        state=ReservationState.CHECKED_IN,
        users=[user_data.user],
        seats=[seat_data.monitor_seat_00],
    )

    # Reservation ended early (checked out)
    reservation_2 = Reservation(
        id=2,
        start=time[THIRTY_MINUTES_AGO],
        end=time[IN_THIRTY_MINUTES],
        created_at=time[THIRTY_MINUTES_AGO],
        updated_at=time[THIRTY_MINUTES_AGO],
        walkin=False,
        room=None,
        state=ReservationState.CHECKED_OUT,
        users=[user_data.ambassador],
        seats=[seat_data.monitor_seat_01],
    )

    # Reservation cancelled
    reservation_3 = Reservation(
        id=3,
        start=time[THIRTY_MINUTES_AGO],
        end=time[IN_THIRTY_MINUTES],
        created_at=time[THIRTY_MINUTES_AGO],
        updated_at=time[THIRTY_MINUTES_AGO],
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
        created_at=time[NOW],
        updated_at=time[NOW],
        walkin=False,
        room=None,
        state=ReservationState.CONFIRMED,
        users=[user_data.root, user_data.ambassador],
        seats=[seat_data.reservable_seats[0], seat_data.reservable_seats[1]],
    )

    # Draft future reservation
    reservation_5 = Reservation(
        id=5,
        start=operating_hours_data.tomorrow.start,
        end=operating_hours_data.tomorrow.end + ONE_HOUR,
        created_at=time[NOW],
        updated_at=time[NOW],
        walkin=False,
        room=None,
        state=ReservationState.DRAFT,
        users=[user_data.user],
        seats=[seat_data.reservable_seats[0]],
    )

    active_reservations = [reservation_1]
    confirmed_reservations = [reservation_4]
    draft_reservations = [reservation_5]
    reservations = [
        reservation_1,
        reservation_2,
        reservation_3,
        reservation_4,
        reservation_5,
    ]


def test_request(overrides: dict | None = None) -> ReservationRequest:
    # Generate default values for the Reservation
    reservation_data = {
        "start": datetime.now(),
        "end": datetime.now() + THIRTY_MINUTES,
        "users": [UserIdentity(id=user_data.ambassador.id)],
        "seats": [SeatIdentity(id=seat_data.monitor_seat_01.id)],
    }

    # Override the defaults if provided in the overrides dictionary
    if overrides:
        reservation_data.update(overrides)

    # Create the Reservation model
    return ReservationRequest(**reservation_data)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session, time: dict[str, datetime]):
    insert_fake_data(session, time)
    session.commit()


def insert_fake_data(session: Session, time: dict[str, datetime]):
    instantiate_global_models(time)

    for reservation in reservations:
        entity = ReservationEntity.from_model(reservation, session)
        session.add(entity)

    reset_table_id_seq(
        session, ReservationEntity, ReservationEntity.id, len(reservations) + 1
    )

def delete_future_data(session: Session, time: dict[str, datetime]):
    reservations = session.scalars(select(ReservationEntity).where(ReservationEntity.end >= time[NOW])).all()
    for reservation in reservations:
        session.delete(reservation)