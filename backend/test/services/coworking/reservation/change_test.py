"""ReservationService#change_reservation method tests"""

import pytest
from unittest.mock import create_autospec

from .....services import PermissionService, UserPermissionException
from .....services.coworking import ReservationService
from .....services.coworking.reservation import ReservationException
from .....models.coworking import ReservationState
from .....services.exceptions import ResourceNotFoundException

from .....models.user import UserIdentity
from .....models.coworking.seat import SeatIdentity
from .....models.coworking.reservation import ReservationPartial

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


def test_change_reservation_not_found(reservation_svc: ReservationService):
    request_reservation = ReservationPartial(id=999)
    with pytest.raises(ResourceNotFoundException):
        reservation_svc.change_reservation(user_data.user, request_reservation)


def test_change_reservation_without_permission(reservation_svc: ReservationService):
    with pytest.raises(UserPermissionException):
        reservation = reservation_svc.change_reservation(
            user_data.user, ReservationPartial(id=4, state=ReservationState.CONFIRMED)
        )


def test_change_reservation_enforces_permissions(reservation_svc: ReservationService):
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation = reservation_svc.change_reservation(
        user_data.root, ReservationPartial(id=5, state=ReservationState.CONFIRMED)
    )
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        user_data.root,
        "coworking.reservation.manage",
        f"user/{reservation_data.reservation_5.users[0].id}",
    )


def test_change_reservation_state_confirmed(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=5, state=ReservationState.CONFIRMED)
    )
    assert reservation_data.reservation_5.id == reservation.id
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_state_confirmed_idempotent(
    reservation_svc: ReservationService,
):
    reservation = reservation_svc.change_reservation(
        user_data.ambassador, ReservationPartial(id=4, state=ReservationState.CONFIRMED)
    )
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_state_noop(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=1, state=ReservationState.CONFIRMED)
    )
    assert reservation_data.reservation_1.state == reservation.state
    assert ReservationState.CONFIRMED != reservation.state


def test_change_reservation_cancel_draft(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=5, state=ReservationState.CANCELLED)
    )
    assert ReservationState.CANCELLED == reservation.state


def test_change_reservation_cancel_confirmed(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.ambassador, ReservationPartial(id=4, state=ReservationState.CANCELLED)
    )
    assert ReservationState.CANCELLED == reservation.state


def test_change_reservation_cancel_checkedin_noop(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=1, state=ReservationState.CANCELLED)
    )
    assert ReservationState.CHECKED_IN == reservation.state


def test_change_reservation_checkout(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=1, state=ReservationState.CHECKED_OUT)
    )
    assert ReservationState.CHECKED_OUT == reservation.state


def test_change_reservation_checkout_draft_noop(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=5, state=ReservationState.CHECKED_OUT)
    )
    assert ReservationState.DRAFT == reservation.state


def test_change_reservation_checkout_confirmed_noop(
    reservation_svc: ReservationService,
):
    reservation = reservation_svc.change_reservation(
        user_data.ambassador,
        ReservationPartial(id=4, state=ReservationState.CHECKED_OUT),
    )
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_change_seats_not_implemented(
    reservation_svc: ReservationService,
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation and changing its seat has logic implemented."""
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            user_data.ambassador,
            ReservationPartial(id=4, seats=[seat_data.monitor_seat_00]),
        )


def test_change_reservation_change_party_not_implemented(
    reservation_svc: ReservationService,
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation and changing its party has logic implemented."""
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            user_data.ambassador,
            ReservationPartial(id=4, users=[user_data.cads_leader]),
        )


def test_change_reservation_change_start_not_implemented(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation start time has logic implemented."""
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            user_data.ambassador,
            ReservationPartial(
                id=4,
                start=reservation_data.reservation_4.start + timedelta(seconds=423),
                end=reservation_data.reservation_4.end,
            ),
        )


def test_change_reservation_change_end_not_implemented(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation end time has logic implemented."""
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            user_data.ambassador,
            ReservationPartial(
                id=4,
                start=reservation_data.reservation_4.start,
                end=reservation_data.reservation_4.end + timedelta(minutes=423),
            ),
        )
