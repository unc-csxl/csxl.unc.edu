"""ReservationService#get_current_reservations_for_user tests."""

from unittest.mock import create_autospec

from backend.models.coworking.reservation import ReservationState

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

# Import core data to ensure all data loads for the tests.
from ...core_data import setup_insert_data_fixture

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import seat_data
from . import reservation_data

__authors__ = [
    "Kris Jordan",
    "Nick Wherthey",
    "Yuvraj Jain",
    "Aarjav Jain",
    "John Schachte",
]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


def test_get_current_reservations_for_user_as_user(
    reservation_svc: ReservationService,
):
    """Get reservations for each user _as the user themself_."""
    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.user, user_data.user
    )
    assert len(reservations) == 3
    assert reservations[0].id == reservation_data.reservation_1.id

    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.ambassador, user_data.ambassador
    )
    assert len(reservations) == 1

    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.root, user_data.root
    )
    assert len(reservations) == 1


def test_get_current_reservations_for_user_permissions(
    reservation_svc: ReservationService,
):
    reservation_svc._permission_svc = create_autospec(reservation_svc._permission_svc)
    reservation_svc.get_current_reservations_for_user(user_data.root, user_data.user)
    reservation_svc._permission_svc.enforce.assert_called_with(
        user_data.root,
        "coworking.reservation.read",
        f"user/{user_data.user.id}",
    )


def test_get_current_reservation_for_user_by_state(reservation_svc: ReservationService):
    """Get reservation for user by state."""
    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.user, user_data.user, ReservationState.CHECKED_IN
    )
    assert len(reservations) == 1
    assert reservations[0].id == reservation_data.reservation_1.id
    assert reservations[0].state == reservation_data.reservation_1.state
