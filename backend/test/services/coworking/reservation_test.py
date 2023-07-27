"""Tests for Coworking Reservation Service."""

import pytest
from unittest.mock import create_autospec

from ....services.coworking import ReservationService, PolicyService
from ....services.coworking.reservation import ReservationError
from ....models.coworking import Reservation, TimeRange, ReservationState

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (seat_svc) are required to be imported in the testing module.
from .fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)
from .time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ..core_data import setup_insert_data_fixture as insert_order_0
from .operating_hours_data import fake_data_fixture as insert_order_1
from .room_data import fake_data_fixture as insert_order_2
from .seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ..core_data import user_data
from . import operating_hours_data
from . import seat_data
from . import reservation_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_get_current_reservations_for_user_as_user(
    reservation_svc: ReservationService,
):
    """Get reservations for each user _as the user themself_."""
    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.user, user_data.user
    )
    assert len(reservations) == 1
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
        f"coworking.reservation.users/{user_data.user.id}",
    )


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
        start=operating_hours_data.tomorrow.start,
        end=operating_hours_data.tomorrow.start + ONE_HOUR,
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


def test_xl_closing_soon(reservation_svc: ReservationService):
    """When the XL is open and upcoming walkins are available, but the closing hour is under default walkin duration."""
    near_closing = TimeRange(
        start=operating_hours_data.tomorrow.end - THIRTY_MINUTES + FIVE_MINUTES,
        end=operating_hours_data.tomorrow.end,
    )
    available_seats = reservation_svc.seat_availability(seat_data.seats, near_closing)
    assert len(available_seats) == 0


def test_draft_reservation_open_seats(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Request with an open seat."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador, reservation_data.test_request()
    )
    assert reservation is not None
    assert reservation.id is not None
    assert reservation.state == ReservationState.DRAFT
    assert_equal_times(time[NOW], reservation.start)
    assert_equal_times(time[IN_THIRTY_MINUTES], reservation.end)
    assert_equal_times(time[NOW], reservation.created_at)
    assert_equal_times(time[NOW], reservation.updated_at)
    assert len(reservation.seats) == 1
    assert len(reservation.users) == 1
    assert reservation.users[0].id == user_data.ambassador.id


def test_draft_reservation_in_past(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Request a reservation that starts in the past. Its start should be now, instead."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        reservation_data.test_request({"start": time[THIRTY_MINUTES_AGO]}),
    )
    assert_equal_times(time[NOW], reservation.start)


def test_draft_reservation_beyond_walkin_limit(reservation_svc: ReservationService):
    """Walkin time limit should be bounded by PolicyService#walkin_initial_duration"""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        reservation_data.test_request(
            {
                "users": [user_data.user],
                "start": reservation_data.reservation_1.end,
                "end": reservation_data.reservation_1.end
                + reservation_svc._policy_svc.walkin_initial_duration(user_data.user)
                + timedelta(minutes=10),
            }
        ),
    )
    assert_equal_times(reservation_data.reservation_1.end, reservation.start)
    assert_equal_times(
        reservation_data.reservation_1.end
        + reservation_svc._policy_svc.walkin_initial_duration(user_data.user),
        reservation.end,
    )


def test_draft_reservation_some_taken_seats(reservation_svc: ReservationService):
    """Request with list of some taken, some open seats."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        reservation_data.test_request(
            {
                "seats": [
                    reservation_data.reservation_1.seats[0],
                    seat_data.monitor_seat_01,
                ]
            }
        ),
    )
    assert len(reservation.seats) == 1
    assert reservation.seats[0].id == seat_data.monitor_seat_01.id


def test_draft_reservation_seat_availability_truncated(
    reservation_svc: ReservationService,
):
    """When walkin requested and seat is reserved later on."""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [user_data.user],
                "start": reservation_data.reservation_1.end,
                "end": operating_hours_data.today.end,
                "seats": reservation_data.reservation_4.seats,
            }
        ),
    )
    assert_equal_times(reservation_data.reservation_4.start, reservation.end)
    assert len(reservation.seats) == 1


def test_draft_reservation_future(reservation_svc: ReservationService):
    """When a reservation is in the future, it has longer limits."""
    future_reservation_limit = (
        reservation_svc._policy_svc.maximum_initial_reservation_duration(user_data.user)
    )
    start = operating_hours_data.tomorrow.start
    end = operating_hours_data.tomorrow.start + future_reservation_limit
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [user_data.user],
                "seats": seat_data.reservable_seats,
                "start": start,
                "end": end,
            }
        ),
    )
    assert_equal_times(start, reservation.start)
    assert_equal_times(end, reservation.end)


def test_future_reservation_unreservable(reservation_svc: ReservationService):
    """When a reservation is not a walk-in, only unreservable seats are available."""
    with pytest.raises(ReservationError):
        start = operating_hours_data.tomorrow.start
        end = operating_hours_data.tomorrow.start + ONE_HOUR
        reservation = reservation_svc.draft_reservation(
            user_data.user,
            reservation_data.test_request(
                {
                    "seats": seat_data.unreservable_seats,
                    "start": start,
                    "end": end,
                }
            ),
        )


def test_draft_reservation_all_closed_seats(reservation_svc: ReservationService):
    """Request with all closed seats errors."""
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.ambassador,
            reservation_data.test_request(
                {
                    "seats": [
                        reservation_data.reservation_1.seats[0],
                    ]
                }
            ),
        )


def test_draft_reservation_has_reservation_conflict(
    reservation_svc: ReservationService,
):
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.user,
            reservation_data.test_request({"users": [user_data.user]}),
        )


def test_draft_reservation_has_no_users(reservation_svc: ReservationService):
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.user, reservation_data.test_request({"users": []})
        )


# TODO:
# Enforce permissions
# Check for equality between users and available seats
# Limit users and seats counts to policy
# Clean-up / Refactor Implementation
# Documentation Standards for #draft_reservation
# Think about errors/validations of drafts that can be edited rather
#  than raising exceptions.
