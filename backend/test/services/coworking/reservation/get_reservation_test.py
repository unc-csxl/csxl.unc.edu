"""ReservationService#get_reservation tests."""

from datetime import datetime
from unittest.mock import create_autospec, call

import pytest
from sqlalchemy.orm import Session

from .....models.coworking import Reservation
from .....services import PermissionService
from .....services.coworking import ReservationService
from .....services.exceptions import ResourceNotFoundException, UserPermissionException
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import time_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_get_reservation(
    session: Session,
):
    """Get an existing reservation as a user party to the reservation."""
    time = time_data()
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    reservation: Reservation = reservation_svc.get_reservation(
        scenario.user, scenario.reservation_1.id
    )
    assert reservation.id == scenario.reservation_1.id
    assert reservation.start == scenario.reservation_1.start
    assert scenario.user.id in [user.id for user in reservation.users]


def test_get_non_existent_reservation(
    session: Session,
):
    """Get an existing reservation as a user party to the reservation."""
    time = time_data()
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 423
        reservation_svc.get_reservation(scenario.user, NONEXISTENT_ID)


def test_get_reservation_enforces_permissions(
    session: Session,
):
    time = time_data()
    scenario = arrange_standard_reservation_scenario(session, time)
    permission_svc = create_autospec(PermissionService)
    permission_svc.check.return_value = False
    reservation_svc = make_reservation_service(session, permission_svc)

    with pytest.raises(UserPermissionException):
        reservation_svc.get_reservation(scenario.user, scenario.reservation_4.id)

    permission_svc.check.assert_has_calls(
        [
            call(
                scenario.user,
                "coworking.reservation.read",
                f"user/{scenario.reservation_4.users[0].id}",
            ),
            call(
                scenario.user,
                "coworking.reservation.read",
                f"user/{scenario.reservation_4.users[1].id}",
            ),
        ]
    )
