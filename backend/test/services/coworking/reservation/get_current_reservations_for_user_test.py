"""ReservationService#get_current_reservations_for_user tests."""

from unittest.mock import create_autospec

from backend.models.coworking.reservation import ReservationState
import pytest
from sqlalchemy.orm import Session

from .....services import PermissionService
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import time_data

__authors__ = [
    "Kris Jordan",
    "Nick Wherthey",
    "Yuvraj Jain",
    "Aarjav Jain",
    "John Schachte",
]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_get_current_reservations_for_user_as_user(
    session: Session,
):
    """Get reservations for each user _as the user themself_."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservations = reservation_svc.get_current_reservations_for_user(
        scenario.user, scenario.user
    )

    # Assert
    assert len(reservations) == 3
    assert reservations[0].id == scenario.reservation_1.id

    # Act
    reservations = reservation_svc.get_current_reservations_for_user(
        scenario.ambassador, scenario.ambassador
    )

    # Assert
    assert len(reservations) == 1

    # Act
    reservations = reservation_svc.get_current_reservations_for_user(
        scenario.root, scenario.root
    )

    # Assert
    assert len(reservations) == 1


def test_get_current_reservations_for_user_permissions(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)
    reservation_svc._permission_svc = create_autospec(PermissionService)

    # Act
    reservation_svc.get_current_reservations_for_user(scenario.root, scenario.user)

    # Assert
    reservation_svc._permission_svc.enforce.assert_called_with(
        scenario.root,
        "coworking.reservation.read",
        f"user/{scenario.user.id}",
    )


def test_get_current_reservation_for_user_by_state(session: Session):
    """Get reservation for user by state."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservations = reservation_svc.get_current_reservations_for_user(
        scenario.user,
        scenario.user,
        ReservationState.CHECKED_IN,
    )

    # Assert
    assert len(reservations) == 1
    assert reservations[0].id == scenario.reservation_1.id
    assert reservations[0].state == scenario.reservation_1.state
