"""ReservationService#seat_availability tests"""

from datetime import datetime, timedelta

from .....services.coworking import PolicyService
from .....models.coworking import (
    TimeRange,
)
import pytest
from sqlalchemy.orm import Session

from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import (
    FIVE_MINUTES,
    IN_TEN_MINUTES,
    NOW,
    ONE_HOUR,
    ONE_MINUTE,
    THIRTY_MINUTES,
    THIRTY_MINUTES_AGO,
    time_data,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_seat_availability_in_past(session: Session, time: dict[str, datetime]):
    """There is no seat availability in the past."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    past = TimeRange(start=time[THIRTY_MINUTES_AGO], end=time[NOW])

    # Act
    available_seats = reservation_svc.seat_availability(scenario.seats, past)

    # Assert
    assert len(available_seats) == 0


def test_seat_availability_beyond_scheduled_operating_hours(
    session: Session, time: dict[str, datetime]
):
    """When there are no operating hours in a given bounds, there is no availability."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    out_of_bounds = TimeRange(
        start=time[NOW] + timedelta(days=423), end=time[NOW] + timedelta(days=424)
    )

    # Act
    available_seats = reservation_svc.seat_availability(scenario.seats, out_of_bounds)

    # Assert
    assert len(available_seats) == 0


def test_seat_availability_while_closed(session: Session):
    """There is no seat availability while the XL is closed."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)
    closed = TimeRange(
        start=scenario.today.end,
        end=scenario.today.end + ONE_HOUR,
    )

    # Act
    available_seats = reservation_svc.seat_availability(scenario.seats, closed)

    # Assert
    assert len(available_seats) == 0


def test_seat_availability_truncate_start(
    session: Session,
    time: dict[str, datetime],
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    policy_svc = PolicyService()
    reservation_svc = make_reservation_service(session, policy_svc=policy_svc)
    recent_past_to_five_minutes = TimeRange(
        start=time[NOW] - policy_svc.minimum_reservation_duration(),
        end=time[NOW] + FIVE_MINUTES,
    )

    # Act
    available_seats = reservation_svc.seat_availability(
        scenario.seats, recent_past_to_five_minutes
    )

    # Assert
    assert len(available_seats) == 0


def test_seat_availability_while_completely_open(
    session: Session,
):
    """All reservable seats should be available."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)
    tomorrow = TimeRange(
        start=scenario.future.start,
        end=scenario.future.start + ONE_HOUR,
    )

    # Act
    available_seats = reservation_svc.seat_availability(
        scenario.reservable_seats, tomorrow
    )

    # Assert
    assert len(available_seats) == len(scenario.reservable_seats)


def test_seat_availability_with_reservation(
    session: Session, time: dict[str, datetime]
):
    """Test data has one of the reservable seats reserved."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    today = TimeRange(start=time[NOW], end=time[IN_TEN_MINUTES])

    # Act
    available_seats = reservation_svc.seat_availability(
        scenario.reservable_seats, today
    )

    # Assert
    assert len(available_seats) == len(scenario.reservable_seats) - 1
    assert available_seats[0].id == scenario.monitor_seat_10.id


def test_seat_availability_near_requested_start(session: Session):
    """When the XL is open and some seats are about to become available."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)
    future = TimeRange(
        start=scenario.today.end - THIRTY_MINUTES - FIVE_MINUTES,
        end=scenario.today.end + FIVE_MINUTES,
    )

    # Act
    available_seats = reservation_svc.seat_availability(
        scenario.reservable_seats, future
    )

    # Assert
    assert len(available_seats) == len(scenario.reservable_seats)
    for seat in available_seats:
        assert seat.availability[0].start == scenario.reservation_4.end
        assert seat.availability[0].end == scenario.today.end


def test_seat_availability_all_reserved(session: Session):
    """Test when all reservable seats are reserved."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)
    future = TimeRange(
        start=scenario.reservation_4.start,
        end=scenario.reservation_4.end,
    )

    # Act
    available_seats = reservation_svc.seat_availability(
        scenario.reservable_seats, future
    )

    # Assert
    assert len(available_seats) == 0


def test_seat_availability_xl_closing_soon(
    session: Session,
):
    """When the XL is open and upcoming walkins are available, but the closing hour is under default walkin duration."""
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    policy_svc = PolicyService()
    reservation_svc = make_reservation_service(session, policy_svc=policy_svc)
    near_closing = TimeRange(
        start=scenario.tomorrow.end
        - (policy_svc.minimum_reservation_duration() - 2 * ONE_MINUTE),
        end=scenario.tomorrow.end,
    )

    # Act
    available_seats = reservation_svc.seat_availability(scenario.seats, near_closing)

    # Assert
    assert len(available_seats) == 0
