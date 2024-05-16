"""Tests for ReservationService#get_map_reservations_for_date and helper functions."""

from backend.models.coworking.availability import RoomState
from backend.models.coworking.reservation import ReservationState
from datetime import date

from .....services.coworking import ReservationService

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (seat_svc) are required to be imported in the testing module.
from ..fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)

from ..time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ...core_data import user_data
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..operating_hours_data import fake_data_fixture as insert_order_1
from ...room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import seat_data
from . import reservation_data

__authors__ = [
    "Yuvraj Jain",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

def test_get_total_time_user_reservations_student(reservation_svc: ReservationService):
    hours = reservation_svc.get_total_time_user_reservations(user_data.user)
    assert hours == "4.5"


def test_get_total_time_user_reservations_ambassador(reservation_svc: ReservationService):
    hours = reservation_svc.get_total_time_user_reservations(user_data.ambassador)
    assert hours == "6"


def test_get_total_time_user_reservations_root(reservation_svc: ReservationService):
    hours = reservation_svc.get_total_time_user_reservations(user_data.root)
    assert hours == "6"