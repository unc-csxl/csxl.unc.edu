"""Tests for ReservationService#get_map_reservations_for_date and helper functions."""

from datetime import date, datetime, time as Time
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from backend.models.coworking.availability import RoomState
from .....services.coworking import PolicyService, ReservationService
from .....services import PermissionService
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import *

__authors__ = [
    "Nick Wherthey",
    "Yuvraj Jain",
]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def make_policy_mock() -> PolicyService:
    policy_svc = MagicMock(spec=PolicyService)
    policy_svc.walkin_window.return_value = PolicyService().walkin_window(None)
    policy_svc.walkin_initial_duration.return_value = PolicyService().walkin_initial_duration(
        None
    )
    policy_svc.reservation_window.return_value = PolicyService().reservation_window(None)
    policy_svc.minimum_reservation_duration.return_value = (
        PolicyService().minimum_reservation_duration()
    )
    policy_svc.reservation_draft_timeout.return_value = (
        PolicyService().reservation_draft_timeout()
    )
    policy_svc.reservation_checkin_timeout.return_value = (
        PolicyService().reservation_checkin_timeout()
    )
    policy_svc.office_hours.return_value = {}
    return policy_svc


def test_transform_date_map_for_unavailable_simple(session: Session):
    """
    Validates the transformation of the date map to indicate unavailable time slots.

    This test ensures that time slots are appropriately grayed out for all other rooms
    once a user has made a reservation. For example, if Sally Student reserves room SN135
    from 1 pm to 3 pm on February 29, she should be prevented from booking any other room
    during these hours. The function verifies that the data map returned by the endpoint
    accurately reflects these unavailable slots, enhancing the user experience by
    preventing double bookings.
    """

    reservation_svc = make_reservation_service(session)

    # Arrange
    sample_date_map_1 = {
        "SN135": [0, 0, 0, 0],
        "SN137": [0, 0, 4, 4],
        "SN139": [0, 0, 0, 0],
    }

    expected_transformed_date_map_1 = {
        "SN135": [0, 0, 3, 3],
        "SN137": [0, 0, 4, 4],
        "SN139": [0, 0, 3, 3],
    }

    # Act
    reservation_svc._transform_date_map_for_unavailable(sample_date_map_1)

    # Assert
    assert sample_date_map_1 == expected_transformed_date_map_1


def test_transform_date_map_for_unavailable_complex(
    session: Session,
):
    reservation_svc = make_reservation_service(session)

    # Arrange
    sample_date_map_2 = {
        "SN135": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        "SN137": [0, 0, 1, 1, 4, 4, 4, 4, 0, 0],
        "SN139": [0, 4, 4, 1, 1, 0, 0, 0, 0, 0],
    }

    expected_transformed_date_map_2 = {
        "SN135": [0, 3, 3, 0, 3, 3, 1, 1, 1, 1],
        "SN137": [0, 3, 1, 1, 4, 4, 4, 4, 0, 0],
        "SN139": [0, 4, 4, 1, 1, 3, 3, 3, 0, 0],
    }

    # Act
    reservation_svc._transform_date_map_for_unavailable(sample_date_map_2)

    # Assert
    assert expected_transformed_date_map_2 == sample_date_map_2


def test_transform_date_map_for_office_hours(
    session: Session,
):
    """Tests to make sure that office hours events in rooms
    are marked unavailable (3)"""
    policy_svc = make_policy_mock()
    reservation_svc = make_reservation_service(session, policy_svc=policy_svc)

    # Arrange
    policy_svc.office_hours = MagicMock(
        return_value={
            "SN135": [],
            "SN137": [(Time(hour=15), Time(hour=16))],
            "SN139": [],
            "SN141": [(Time(hour=10), Time(hour=16))],
            "SN144": [],
            "SN146": [],
            "SN147": [],
        }
    )
    date = datetime(year=2024, month=5, day=1)
    start = datetime(year=2024, month=5, day=1, hour=10, minute=0)
    reserved_date_map = {
        "SN135": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "SN137": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "SN141": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }

    expected_transformed_date_map = {
        "SN135": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "SN137": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
        "SN141": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0],
    }

    # Act
    reservation_svc._transform_date_map_for_officehours(
        date, reserved_date_map, start, 16
    )

    # Assert
    assert reserved_date_map == expected_transformed_date_map


def test_idx_calculation(session: Session):
    reservation_svc = make_reservation_service(session)

    # Arrange
    time_1 = datetime.now().replace(hour=10, minute=12)
    oh_start = datetime.now().replace(hour=10, minute=0)

    # Act / Assert
    assert reservation_svc._idx_calculation(time_1, oh_start) == 0

    time_2 = datetime.now().replace(hour=12, minute=30)
    assert reservation_svc._idx_calculation(time_2, oh_start) == 5

    time_3 = datetime.now().replace(hour=13, minute=40)
    assert reservation_svc._idx_calculation(time_3, oh_start) == 7


def test_round_idx_calculation(session: Session):
    reservation_svc = make_reservation_service(session)

    # Arrange
    time = datetime.now().replace(hour=10, minute=0)
    time2 = datetime.now().replace(hour=18, minute=0)
    time3 = datetime.now().replace(hour=10, minute=1)
    time4 = datetime.now().replace(hour=18, minute=14)

    # Act
    rounded_time = reservation_svc._round_to_closest_half_hour(time, True)
    rounded_time2 = reservation_svc._round_to_closest_half_hour(time2, False)
    rounded_time3 = reservation_svc._round_to_closest_half_hour(time3, True)
    rounded_time4 = reservation_svc._round_to_closest_half_hour(time4, False)

    # Assert
    assert rounded_time.hour == 10 and rounded_time.minute == 0
    assert rounded_time2.hour == 18 and rounded_time2.minute == 0
    assert rounded_time3.hour == 10 and rounded_time3.minute == 30
    assert rounded_time4.hour == 18 and rounded_time4.minute == 0


def test_round_idx_calculation_2(session: Session):
    reservation_svc = make_reservation_service(session)

    # Arrange
    time = datetime.now().replace(hour=10, minute=44)

    # Act
    rounded_up = reservation_svc._round_to_closest_half_hour(time, True)
    rounded_down = reservation_svc._round_to_closest_half_hour(time, False)

    # Assert
    assert rounded_up.hour == 11 and rounded_up.minute == 0
    assert rounded_down.hour == 10 and rounded_down.minute == 30


def test_query_confirmed_reservations_by_date_and_room(
    session: Session, time: dict[str, datetime]
):
    """Test getting all reservations for a particular date."""
    arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    # Arrange
    target_date = time[NOW] + timedelta(days=2)

    # Act
    reservations = reservation_svc._query_confirmed_reservations_by_date_and_room(
        target_date, "SN135"
    )

    # Assert
    assert len(reservations) == 1
    assert reservations[0].id == 6
    assert reservations[0].room.id == "SN135"


def test_get_reservable_rooms(session: Session):
    arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    rooms = reservation_svc._get_reservable_rooms()

    # Assert
    assert rooms[0].id == "SN135" and rooms[0].reservable is True
    assert rooms[1].id == "SN137" and rooms[1].reservable is True
    assert rooms[2].id == "SN139" and rooms[2].reservable is True
    assert rooms[3].id == "SN141" and rooms[3].reservable is True


def test_query_xl_reservations_by_date_for_user(
    session: Session, time: dict[str, datetime]
):
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    # Act
    reservations = reservation_svc._query_xl_reservations_by_date_for_user(
        time[NOW], scenario.user
    )

    # Assert
    assert reservations[0].room is None
    assert reservations[0].users[0].first_name == "Sally"


def test_get_map_reserved_times_by_date(
    session: Session,
    time: dict[str, datetime],
):
    """Test for getting a dictionary where keys are room ids and time slots array are values.

    If this test fails, consider running the reset_demo script before running this test again.
    This is hard function to test, and this test does not ensure 100% coverage due to the
    multiple edge cases that arise out of it. I recommend setting a breakpoint and looking at
    the reserved_date_map in the debugger.
    """
    scenario = arrange_standard_reservation_scenario(session, time)
    policy_svc = make_policy_mock()
    reservation_svc = make_reservation_service(session, policy_svc=policy_svc)

    # Arrange
    policy_svc.office_hours = MagicMock(
        return_value={
            "SN135": [],
            "SN137": [],
            "SN139": [],
            "SN141": [],
            "SN144": [],
            "SN146": [],
            "SN147": [],
        }
    )
    test_time = datetime(2026, 4, 17, 0, 0)
    reservation_svc._get_reservable_rooms = MagicMock(
        return_value=[
            scenario.group_a,
            scenario.group_b,
            scenario.pair_a,
            scenario.group_c,
            scenario.xl_room,
        ]
    )
    reservation_svc._operating_hours_svc.schedule = MagicMock(
        return_value=[
            scenario.future.model_copy(
                update={
                    "start": datetime(2026, 4, 17, 10, 0),
                    "end": datetime(2026, 4, 17, 12, 30),
                }
            )
        ]
    )
    subject_room_reservation = scenario.reservation_6.model_copy(
        update={
            "start": datetime(2026, 4, 17, 10, 30),
            "end": datetime(2026, 4, 17, 12, 0),
            "room": scenario.group_a,
            "users": [scenario.user],
        }
    )
    reservation_svc._query_confirmed_reservations_by_date_and_room = MagicMock(
        side_effect=lambda date, room_id: [subject_room_reservation]
        if room_id == "SN135"
        else []
    )
    reservation_svc._query_xl_reservations_by_date_for_user = MagicMock(return_value=[])

    # Act
    reservation_details = reservation_svc.get_map_reserved_times_by_date(
        test_time, scenario.user
    )

    # Assert
    assert reservation_details.reserved_date_map["SN135"] == [0, 4, 4, 4, 0]
    assert reservation_details.reserved_date_map["SN139"] == [0, 3, 3, 3, 0]

    root_details = reservation_svc.get_map_reserved_times_by_date(
        test_time, scenario.root
    )
    assert root_details.reserved_date_map["SN135"] == [0, 1, 1, 1, 0]
    assert root_details.reserved_date_map["SN139"] == [0, 0, 0, 0, 0]


def test_get_map_reserved_times_by_date_outside_operating_hours(
    session: Session, time: dict[str, datetime]
):
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    # Arrange
    test_time = time[NOW] + timedelta(days=69)
    reservation_svc._get_reservable_rooms = MagicMock(
        return_value=[
            scenario.group_a,
            scenario.group_b,
            scenario.pair_a,
            scenario.group_c,
            scenario.xl_room,
        ]
    )
    reservation_svc._operating_hours_svc.schedule = MagicMock(return_value=[])

    # Act
    reservation_details = reservation_svc.get_map_reserved_times_by_date(
        test_time, scenario.user
    )

    # Assert
    assert reservation_details.number_of_time_slots == 16

    assert reservation_details.operating_hours_start.hour == 10
    assert reservation_details.operating_hours_start.minute == 0

    assert reservation_details.operating_hours_end.hour == 18
    assert reservation_details.operating_hours_end.minute == 0

    expected_date_map = {
        "SN135": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        "SN137": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        "SN139": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        "SN141": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        "SN156": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    }

    assert reservation_details.reserved_date_map == expected_date_map


def test_get_map_reserved_times_by_date_today_dynamic(
    session: Session, time: dict[str, datetime]
):
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)

    # Arrange
    fixed_now = datetime(2026, 4, 15, 12, 15)
    test_time = fixed_now
    reservation_svc._get_reservable_rooms = MagicMock(return_value=[scenario.group_a])
    reservation_svc._operating_hours_svc.schedule = MagicMock(
        return_value=[
            scenario.today.model_copy(
                update={
                    "start": fixed_now - ONE_HOUR,
                    "end": fixed_now + 3 * ONE_HOUR,
                }
            )
        ]
    )
    reservation_svc._query_confirmed_reservations_by_date_and_room = MagicMock(
        return_value=[]
    )
    reservation_svc._query_xl_reservations_by_date_for_user = MagicMock(return_value=[])

    # Act
    with patch("backend.services.coworking.reservation.datetime") as datetime_mock:
        datetime_mock.now.return_value = fixed_now
        reservation_details = reservation_svc.get_map_reserved_times_by_date(
            test_time, scenario.user
        )

    # Assert
    # We only see 6 time slots rather than 8 because operating hours started an hour ago
    assert reservation_details.number_of_time_slots == 6
