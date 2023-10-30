"""Fixtures used for testing the Coworking Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ....services import PermissionService
from ....services.coworking import (
    OperatingHoursService,
    RoomService,
    SeatService,
    ReservationService,
    PolicyService,
    StatusService,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def operating_hours_svc(session: Session, permission_svc: PermissionService):
    """OperatingHoursService fixture."""
    return OperatingHoursService(session, permission_svc)


@pytest.fixture()
def room_svc(session: Session):
    """RoomService fixture."""
    return RoomService(session)


@pytest.fixture()
def seat_svc(session: Session):
    """SeatService fixture."""
    return SeatService(session)


@pytest.fixture()
def policy_svc():
    """CoworkingPolicyService fixture."""
    return PolicyService()


@pytest.fixture()
def reservation_svc(
    session: Session,
    policy_svc: PolicyService,
    permission_svc: PermissionService,
    operating_hours_svc: OperatingHoursService,
    seat_svc: SeatService,
):
    """ReservationService fixture."""
    return ReservationService(
        session, permission_svc, policy_svc, operating_hours_svc, seat_svc
    )


@pytest.fixture()
def status_svc():
    policies_mock = create_autospec(PolicyService)
    operating_hours_mock = create_autospec(OperatingHoursService)
    seat_mock = create_autospec(SeatService)
    reservation_mock = create_autospec(ReservationService)
    return StatusService(
        policies_mock, operating_hours_mock, seat_mock, reservation_mock
    )
