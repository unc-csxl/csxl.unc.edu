"""ReservationService#get_seat_reservations tests."""

from unittest.mock import create_autospec

from .....models.coworking import (
    Reservation,
    TimeRange,
)
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
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..operating_hours_data import fake_data_fixture as insert_order_1
from ...room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import seat_data
from . import reservation_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_get_seat_reservations_none(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Get all reservations for a time range with no reservations."""
    in_the_past = TimeRange(
        start=time[THIRTY_MINUTES_AGO] - FIVE_MINUTES,
        end=time[THIRTY_MINUTES_AGO] - ONE_MINUTE,
    )
    reservations = reservation_svc.get_seat_reservations(seat_data.seats, in_the_past)
    assert len(reservations) == 0


def test_get_seat_reservations_active(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Get all reservations that are active (not cancelled or checked out)."""
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    reservations = reservation_svc.get_seat_reservations(seat_data.seats, current)
    assert len(reservations) == len(reservation_data.active_reservations)
    assert isinstance(reservations[0], Reservation)
    assert reservations[0].id == reservation_data.reservation_1.id


def test_get_seat_reservations_unreserved_seats(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Get reservations for unreserved seats (expecting no matches)."""
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    reservations = reservation_svc.get_seat_reservations(
        seat_data.unreservable_seats, current
    )
    assert len(reservations) == 0
