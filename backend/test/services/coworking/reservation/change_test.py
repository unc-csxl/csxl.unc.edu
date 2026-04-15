"""ReservationService#change_reservation method tests"""

from datetime import datetime, timedelta

import pytest
from unittest.mock import create_autospec

from sqlalchemy.orm import Session

from .....services import PermissionService, UserPermissionException
from .....models.coworking import ReservationState
from .....services.exceptions import ResourceNotFoundException

from .....models.coworking.reservation import Reservation, ReservationPartial
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import IN_ONE_HOUR, NOW, time_data

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_change_reservation_not_found(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    request_reservation = ReservationPartial(id=999)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        reservation_svc.change_reservation(scenario.user, request_reservation)


def test_change_reservation_without_permission(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "coworking.reservation.manage", f"user/{scenario.root.id}"
    )
    reservation_svc = make_reservation_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        reservation_svc.change_reservation(
            scenario.user,
            ReservationPartial(id=4, state=ReservationState.CONFIRMED),
        )


def test_change_reservation_enforces_permissions(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc = make_reservation_service(session, permission_svc)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.root,
        ReservationPartial(id=5, state=ReservationState.CONFIRMED),
    )

    # Assert
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        scenario.root,
        "coworking.reservation.manage",
        f"user/{scenario.reservation_5.users[0].id}",
    )


def test_change_reservation_state_confirmed(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.user,
        ReservationPartial(id=5, state=ReservationState.CONFIRMED),
    )

    # Assert
    assert scenario.reservation_5.id == reservation.id
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_state_confirmed_idempotent(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.ambassador,
        ReservationPartial(id=4, state=ReservationState.CONFIRMED),
    )

    # Assert
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_state_noop(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.user,
        ReservationPartial(id=1, state=ReservationState.CONFIRMED),
    )

    # Assert
    assert scenario.reservation_1.state == reservation.state
    assert ReservationState.CONFIRMED != reservation.state


def test_change_reservation_cancel_draft(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.user,
        ReservationPartial(id=5, state=ReservationState.CANCELLED),
    )

    # Assert
    assert ReservationState.CANCELLED == reservation.state


def test_change_reservation_cancel_confirmed(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.ambassador,
        ReservationPartial(id=4, state=ReservationState.CANCELLED),
    )

    # Assert
    assert ReservationState.CANCELLED == reservation.state


def test_change_reservation_cancel_checkedin_noop(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.user,
        ReservationPartial(id=1, state=ReservationState.CANCELLED),
    )

    # Assert
    assert ReservationState.CHECKED_IN == reservation.state


def test_change_reservation_checkout(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.user,
        ReservationPartial(id=1, state=ReservationState.CHECKED_OUT),
    )

    # Assert
    assert ReservationState.CHECKED_OUT == reservation.state


def test_change_reservation_checkout_draft_noop(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.user,
        ReservationPartial(id=5, state=ReservationState.CHECKED_OUT),
    )

    # Assert
    assert ReservationState.DRAFT == reservation.state


def test_change_reservation_checkout_confirmed_noop(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    reservation = reservation_svc.change_reservation(
        scenario.ambassador,
        ReservationPartial(id=4, state=ReservationState.CHECKED_OUT),
    )

    # Assert
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_confirmed_checkin_room(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    reservation = Reservation(
        id=8,
        start=time[NOW],
        end=time[IN_ONE_HOUR],
        created_at=time[NOW],
        updated_at=time[NOW],
        walkin=False,
        room=scenario.group_a,
        state=ReservationState.CONFIRMED,
        users=[scenario.user],
        seats=[],
    )

    # Act / Assert
    assert reservation_svc._change_state(reservation, delta=ReservationState.CHECKED_IN)


def test_change_reservation_change_seats_not_implemented(
    session: Session,
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation and changing its seat has logic implemented."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            scenario.ambassador,
            ReservationPartial(id=4, seats=[scenario.monitor_seat_00]),
        )


def test_change_reservation_change_party_not_implemented(
    session: Session,
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation and changing its party has logic implemented."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            scenario.ambassador,
            ReservationPartial(id=4, users=[scenario.root]),
        )


def test_change_reservation_change_start_not_implemented(
    session: Session, time: dict[str, datetime]
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation start time has logic implemented."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            scenario.ambassador,
            ReservationPartial(
                id=4,
                start=scenario.reservation_4.start + timedelta(seconds=423),
                end=scenario.reservation_4.end,
            ),
        )


def test_change_reservation_change_end_not_implemented(
    session: Session, time: dict[str, datetime]
):
    """This test is for 100% coverage but should be replaced with actual tests for when
    changing a reservation end time has logic implemented."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    # Act / Assert
    with pytest.raises(NotImplementedError):
        reservation_svc.change_reservation(
            scenario.ambassador,
            ReservationPartial(
                id=4,
                start=scenario.reservation_4.start,
                end=scenario.reservation_4.end + timedelta(minutes=423),
            ),
        )
