"""ReservationService#draft_reservation method tests"""

import pytest
from unittest.mock import create_autospec

from .....services import PermissionService
from .....services.coworking import ReservationService
from .....services.coworking.reservation import ReservationError
from .....models.coworking import ReservationState

from .....models.user import UserIdentity
from .....models.coworking.seat import SeatIdentity

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
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
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
                    SeatIdentity(
                        **reservation_data.reservation_1.seats[0].model_dump()
                    ),
                    SeatIdentity(**seat_data.monitor_seat_01.model_dump()),
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
                "users": [UserIdentity(**user_data.user.model_dump())],
                "start": reservation_data.reservation_1.end,
                "end": operating_hours_data.today.end,
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in reservation_data.reservation_4.seats
                ],
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
    start = operating_hours_data.future.start
    end = operating_hours_data.future.start + future_reservation_limit
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in seat_data.reservable_seats
                ],
                "start": start,
                "end": end,
            }
        ),
    )
    assert_equal_times(start, reservation.start)
    assert_equal_times(end, reservation.end)


def test_draft_reservation_future_unreservable(reservation_svc: ReservationService):
    """When a reservation is not a walk-in, only unreservable seats are available."""
    with pytest.raises(ReservationError):
        start = operating_hours_data.tomorrow.start
        end = operating_hours_data.tomorrow.start + ONE_HOUR
        reservation = reservation_svc.draft_reservation(
            user_data.ambassador,
            reservation_data.test_request(
                {
                    "seats": [
                        SeatIdentity(**seat.model_dump())
                        for seat in seat_data.unreservable_seats
                    ],
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
                        SeatIdentity(
                            **reservation_data.reservation_1.seats[0].model_dump()
                        ),
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
            reservation_data.test_request(
                {"users": [UserIdentity(**user_data.user.model_dump())]}
            ),
        )


def test_draft_reservation_has_no_users(reservation_svc: ReservationService):
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.user, reservation_data.test_request({"users": []})
        )


def test_draft_reservation_permissions(reservation_svc: ReservationService):
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation = reservation_svc.draft_reservation(
        user_data.root, reservation_data.test_request()
    )
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        user_data.root,
        "coworking.reservation.manage",
        f"user/{user_data.ambassador.id}",
    )


def test_draft_reservation_one_user_for_now(reservation_svc: ReservationService):
    with pytest.raises(ReservationError):
        reservation_svc.draft_reservation(
            user_data.ambassador,
            reservation_data.test_request(
                {
                    "users": [
                        UserIdentity(**user_data.root.model_dump()),
                        UserIdentity(**user_data.ambassador.model_dump()),
                    ]
                }
            ),
        )
