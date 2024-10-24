"""Tests for the RoleService class."""

# Tested Dependencies
from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session

from backend.entities.coworking.reservation_entity import ReservationEntity
from backend.models.coworking.reservation import Reservation, ReservationState
from ...models import SignageOverviewFast, SignageOverviewSlow
from ...services import SignageService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import signage_svc

# Data Setup and Injected Service Fixtures
from .coworking.seat_data import fake_data_fixture as insert_fake_seat_data
from .room_data import fake_data_fixture as insert_fake_room_data
from .user_data import fake_data_fixture as insert_fake_user_data
from .coworking.reservation.reservation_data import (
    fake_data_fixture as insert_fake_reservation_data,
)
from .office_hours.office_hours_data import (
    fake_data_fixture as insert_fake_office_hours_data,
)
from .signage_data import fake_data_fixture as insert_fake_sigange_data


#  Import the fake model data in a namespace for test assertions
from .coworking import seat_data
from . import room_data, user_data
from .coworking.reservation import reservation_data
from .office_hours import office_hours_data

__authors__ = ["Will Zahrt", "Andrew Lockard"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

now = datetime.now()

# current_reservation = Reservation(
#     id=8,
#     start=now - timedelta(hours=1),
#     end=now + timedelta(hours=2),
#     created_at=now - timedelta(hours=2),
#     updated_at=now - timedelta(hours=1, minutes=30),
#     walkin=False,
#     room=room_data.pair_a,
#     state=ReservationState.CHECKED_IN,
#     users=[user_data.root],
#     seats=[],
# )


# @pytest.fixture(autouse=True)
# def insert_additional_fake_data(session: Session):
#     """Inserts additional data needed to fully test signage."""
#     entity = ReservationEntity.from_model(current_reservation)
#     session.add(entity)
#     session.commit()


def test_get_fast_data(signage_svc: SignageService):
    fast_data = signage_svc.get_fast_data()
    assert len(fast_data.active_office_hours) == 1
    assert (
        fast_data.active_office_hours[0].id
        == office_hours_data.comp_110_current_office_hours.id
    )
    available_rooms = [room.id for room in room_data.rooms]
    assert room_data.pair_a.id not in available_rooms

    available_seats = [seat for seat in fast_data.seat_availability if seat.reservable]
    assert seat_data.monitor_seat_01 not in available_seats
    assert seat_data.monitor_seat_11 not in available_seats
