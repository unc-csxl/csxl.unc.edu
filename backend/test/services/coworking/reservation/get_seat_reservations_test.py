"""ReservationService#get_seat_reservations tests."""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from .....models.coworking import (
    Reservation,
    TimeRange,
)
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import (
    FIVE_MINUTES,
    IN_THIRTY_MINUTES,
    NOW,
    ONE_MINUTE,
    THIRTY_MINUTES_AGO,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_get_seat_reservations_none(
    session: Session, time: dict[str, datetime]
):
    """Get all reservations for a time range with no reservations."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    in_the_past = TimeRange(
        start=time[THIRTY_MINUTES_AGO] - FIVE_MINUTES,
        end=time[THIRTY_MINUTES_AGO] - ONE_MINUTE,
    )

    # Act
    reservations = reservation_svc.get_seat_reservations(scenario.seats, in_the_past)

    # Assert
    assert len(reservations) == 0


def test_get_seat_reservations_active(
    session: Session, time: dict[str, datetime]
):
    """Get all reservations that are active (not cancelled or checked out)."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])

    # Act
    reservations = reservation_svc.get_seat_reservations(scenario.seats, current)

    # Assert
    assert len(reservations) == len(scenario.active_reservations)
    assert isinstance(reservations[0], Reservation)
    assert reservations[0].id == scenario.reservation_1.id


def test_get_seat_reservations_unreserved_seats(
    session: Session, time: dict[str, datetime]
):
    """Get reservations for unreserved seats (expecting no matches)."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])

    # Act
    reservations = reservation_svc.get_seat_reservations(
        scenario.unreservable_seats, current
    )

    # Assert
    assert len(reservations) == 0
