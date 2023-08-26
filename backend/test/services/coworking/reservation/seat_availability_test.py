"""ReservationService#seat_availability tests"""

import pytest
from unittest.mock import create_autospec

from .....services.coworking import ReservationService, PolicyService
from .....models.coworking import (
    TimeRange,
)

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
from ..room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import operating_hours_data
from .. import seat_data
from . import reservation_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_seat_availability_in_past(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """There is no seat availability in the past."""
    past = TimeRange(start=time[THIRTY_MINUTES_AGO], end=time[NOW])
    available_seats = reservation_svc.seat_availability(seat_data.seats, past)
    assert len(available_seats) == 0


def test_seat_availability_while_closed(reservation_svc: ReservationService):
    """There is no seat availability while the XL is closed."""
    closed = TimeRange(
        start=operating_hours_data.today.end,
        end=operating_hours_data.today.end + ONE_HOUR,
    )
    available_seats = reservation_svc.seat_availability(seat_data.seats, closed)
    assert len(available_seats) == 0


def test_seat_availability_truncate_start(
    reservation_svc: ReservationService,
    policy_svc: PolicyService,
    time: dict[str, datetime],
):
    recent_past_to_five_minutes = TimeRange(
        start=time[NOW] - policy_svc.minimum_reservation_duration(),
        end=time[NOW] + FIVE_MINUTES,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.seats, recent_past_to_five_minutes
    )
    assert len(available_seats) == 0


def test_seat_availability_while_completely_open(
    reservation_svc: ReservationService,
):
    """All reservable seats should be available."""
    tomorrow = TimeRange(
        start=operating_hours_data.future.start,
        end=operating_hours_data.future.start + ONE_HOUR,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, tomorrow
    )
    assert len(available_seats) == len(seat_data.reservable_seats)


def test_seat_availability_with_reservation(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Test data has one of the reservable seats reserved."""
    today = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, today
    )
    assert len(available_seats) == len(seat_data.reservable_seats) - 1
    assert available_seats[0].id == seat_data.monitor_seat_10.id


def test_seat_availability_near_requested_start(reservation_svc: ReservationService):
    """When the XL is open and some seats are about to become available."""
    future = TimeRange(
        start=operating_hours_data.today.end - THIRTY_MINUTES - FIVE_MINUTES,
        end=operating_hours_data.today.end + FIVE_MINUTES,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, future
    )
    assert len(available_seats) == len(seat_data.reservable_seats)
    for seat in available_seats:
        assert seat.availability[0].start == reservation_data.reservation_4.end
        assert seat.availability[0].end == operating_hours_data.today.end


def test_seat_availability_all_reserved(reservation_svc: ReservationService):
    """Test when all reservable seats are reserved."""
    future = TimeRange(
        start=reservation_data.reservation_4.start,
        end=reservation_data.reservation_4.end,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, future
    )
    assert len(available_seats) == 0


def test_seat_availability_xl_closing_soon(reservation_svc: ReservationService):
    """When the XL is open and upcoming walkins are available, but the closing hour is under default walkin duration."""
    near_closing = TimeRange(
        start=operating_hours_data.tomorrow.end - THIRTY_MINUTES + FIVE_MINUTES,
        end=operating_hours_data.tomorrow.end,
    )
    available_seats = reservation_svc.seat_availability(seat_data.seats, near_closing)
    assert len(available_seats) == 0
