"""ReservationService#get_seat_reservations tests."""

from datetime import datetime
from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from .....services import PermissionService
from .....models.coworking import Reservation
from .....services.exceptions import ResourceNotFoundException
from .....services.coworking.reservation import ReservationException
from .....models.coworking import ReservationState
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import IN_ONE_HOUR, NOW, time_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_staff_checkin_success(
    session: Session,
):
    """Expected case of this service method."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation: Reservation = reservation_svc.staff_checkin_reservation(
        scenario.ambassador, scenario.reservation_4
    )

    # Assert
    assert reservation.id == scenario.reservation_4.id
    assert reservation.state == ReservationState.CHECKED_IN


def test_staff_checkin_idempotence(
    session: Session,
):
    """Repeated checkin requests should not error out and be idempotent."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation_svc.staff_checkin_reservation(
        scenario.ambassador, scenario.reservation_4
    )
    reservation: Reservation = reservation_svc.staff_checkin_reservation(
        scenario.ambassador, scenario.reservation_4
    )

    # Assert
    assert reservation.id == scenario.reservation_4.id
    assert reservation.state == ReservationState.CHECKED_IN


def test_staff_checkin_not_found(session: Session, time: dict[str, datetime]):
    """ResourceNotFoundException expected when reservation does not exist."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    reservation = Reservation(
        id=423,
        start=time[NOW],
        end=time[IN_ONE_HOUR],
        state=ReservationState.CONFIRMED,
        users=[],
        seats=[],
        created_at=time[NOW],
        updated_at=time[NOW],
    )

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        reservation_svc.staff_checkin_reservation(scenario.ambassador, reservation)


def test_staff_checkin_wrong_state_draft(
    session: Session,
):
    """Checkins can only happen from a state of Confirmed."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.staff_checkin_reservation(
            scenario.ambassador, scenario.reservation_5
        )


def test_staff_checkin_wrong_state_checked_out(
    session: Session,
):
    """Checkins can only happen from a state of Confirmed."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.staff_checkin_reservation(
            scenario.ambassador, scenario.reservation_2
        )


def test_staff_checkin_wrong_state_cancelled(
    session: Session,
):
    """Checkins can only happen from a state of Confirmed."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.staff_checkin_reservation(
            scenario.ambassador, scenario.reservation_3
        )


def test_staff_checkin_enforces_permissions(session: Session):
    """Checkin requires a permission to take action coworking.reservation.manage on user/*"""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc = make_reservation_service(session, permission_svc)

    # Act
    reservation = reservation_svc.staff_checkin_reservation(
        scenario.ambassador, scenario.reservation_4
    )

    # Assert
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        scenario.ambassador,
        "coworking.reservation.manage",
        "user/*",
    )
