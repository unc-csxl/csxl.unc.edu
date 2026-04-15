"""ReservationService#list_all_active_and_upcoming tests."""

from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from backend.services.exceptions import UserPermissionException

from .....services import PermissionService
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import time_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_list_all_active_and_upcoming_for_xl(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    all_reservations = reservation_svc.list_all_active_and_upcoming_for_xl(
        scenario.ambassador
    )

    # Assert
    assert len(all_reservations) == len(scenario.active_reservations) + len(
        scenario.confirmed_reservations
    )


def test_list_all_active_and_upcoming_permission(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc = make_reservation_service(session, permission_svc)

    # Act
    reservation_svc.list_all_active_and_upcoming_for_xl(scenario.ambassador)

    # Assert
    permission_svc.enforce.assert_called_once_with(
        scenario.ambassador,
        "coworking.reservation.read",
        "user/*",
    )


def test_list_all_active_and_upcoming_for_rooms_user(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "coworking.reservation.read", "user/*"
    )
    reservation_svc = make_reservation_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        reservation_svc.list_all_active_and_upcoming_for_rooms(scenario.user)


def test_list_all_active_and_upcoming_for_rooms_ambassador(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    all_reservations = reservation_svc.list_all_active_and_upcoming_for_rooms(
        scenario.ambassador
    )

    # Assert
    assert len(all_reservations) == len(scenario.room_reservations)
