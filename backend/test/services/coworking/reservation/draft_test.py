"""ReservationService#draft_reservation method tests."""

from datetime import datetime, timedelta
from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from .....models.coworking import ReservationRequest, ReservationState
from .....models.coworking.seat import SeatIdentity
from .....models.user import UserIdentity
from .....services import PermissionService
from .....services.coworking.reservation import ReservationException
from .scenario import (
    arrange_standard_reservation_scenario,
    make_reservation_service,
    make_test_request,
)
from ..time import (
    FIVE_MINUTES,
    IN_THIRTY_MINUTES,
    NOW,
    ONE_HOUR,
    TEN_MINUTES,
    THIRTY_MINUTES,
    THIRTY_MINUTES_AGO,
    assert_equal_times,
)

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_draft_reservation_open_seats(session: Session, time: dict[str, datetime]):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(scenario)

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert reservation is not None
    assert reservation.id is not None
    assert reservation.state == ReservationState.DRAFT
    assert_equal_times(time[NOW], reservation.start)
    assert_equal_times(time[IN_THIRTY_MINUTES], reservation.end)
    assert_equal_times(time[NOW], reservation.created_at)
    assert_equal_times(time[NOW], reservation.updated_at)
    assert len(reservation.seats) == 1
    assert len(reservation.users) == 1
    assert reservation.users[0].id == scenario.ambassador.id


def test_draft_reservation_in_past(session: Session, time: dict[str, datetime]):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(scenario, {"start": time[THIRTY_MINUTES_AGO]})

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert_equal_times(time[NOW], reservation.start)


def test_draft_reservation_beyond_walkin_limit(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "users": [UserIdentity(**scenario.user.model_dump())],
            "start": scenario.reservation_1.end,
            "end": scenario.reservation_1.end
            + reservation_svc._policy_svc.walkin_initial_duration(scenario.user)
            + timedelta(minutes=10),
        },
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.user, request)

    # Assert
    assert_equal_times(scenario.reservation_1.end, reservation.start)
    assert_equal_times(
        scenario.reservation_1.end
        + reservation_svc._policy_svc.walkin_initial_duration(scenario.user),
        reservation.end,
    )


def test_draft_reservation_some_taken_seats(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "seats": [
                SeatIdentity(id=scenario.reservation_1.seats[0].id),
                SeatIdentity(id=scenario.monitor_seat_01.id),
            ]
        },
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert len(reservation.seats) == 1
    assert reservation.seats[0].id == scenario.monitor_seat_01.id


def test_draft_reservation_seat_availability_truncated(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "users": [UserIdentity(**scenario.user.model_dump())],
            "start": scenario.reservation_1.end,
            "end": scenario.today.end,
            "seats": [
                SeatIdentity(id=seat.id) for seat in scenario.reservation_4.seats
            ],
        },
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.user, request)

    # Assert
    assert_equal_times(scenario.reservation_4.start, reservation.end)
    assert len(reservation.seats) == 1


def test_draft_reservation_future(session: Session, time: dict[str, datetime]):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    future_reservation_limit = (
        reservation_svc._policy_svc.maximum_initial_reservation_duration(scenario.user)
    )
    start = scenario.future.start
    end = scenario.future.start + future_reservation_limit
    request = make_test_request(
        scenario,
        {
            "seats": [SeatIdentity(id=seat.id) for seat in scenario.reservable_seats],
            "start": start,
            "end": end,
        },
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert_equal_times(start, reservation.start)
    assert_equal_times(end, reservation.end)


def test_draft_reservation_future_unreservable(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    start = scenario.tomorrow.start
    end = scenario.tomorrow.start + ONE_HOUR
    request = make_test_request(
        scenario,
        {
            "seats": [SeatIdentity(id=seat.id) for seat in scenario.unreservable_seats],
            "start": start,
            "end": end,
        },
    )

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, request)


def test_draft_reservation_all_closed_seats(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "seats": [SeatIdentity(id=scenario.reservation_1.seats[0].id)],
            "end": scenario.reservation_1.end + timedelta(minutes=8),
        },
    )

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, request)


def test_draft_reservation_has_reservation_conflict(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "users": [UserIdentity(**scenario.user.model_dump())],
            "end": time[NOW] + TEN_MINUTES,
        },
    )

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.user, request)


def test_draft_walkin_reservation_has_walkin_reservation_conflict(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(scenario, {"start": time[THIRTY_MINUTES_AGO]})

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert reservation.walkin
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, request)


def test_draft_reservation_in_middle_of_another(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "start": scenario.today.end - ONE_HOUR + FIVE_MINUTES,
            "end": scenario.today.end - ONE_HOUR + FIVE_MINUTES * 4,
        },
    )

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, request)


def test_draft_reservation_has_conflict_but_ok(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    conflict = scenario.reservation_4
    request = make_test_request(
        scenario,
        {
            "start": time[NOW],
            "end": conflict.start + THIRTY_MINUTES,
            "users": [UserIdentity(**scenario.root.model_dump())],
        },
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.root, request)

    # Assert
    assert reservation.id is not None
    assert_equal_times(conflict.start, reservation.end)


def test_draft_reservation_has_no_users(session: Session, time: dict[str, datetime]):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(scenario, {"users": []})

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.user, request)


def test_draft_reservation_permissions(session: Session, time: dict[str, datetime]):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc = make_reservation_service(session, permission_svc)
    request = make_test_request(scenario)

    # Act
    reservation = reservation_svc.draft_reservation(scenario.root, request)

    # Assert
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        scenario.root,
        "coworking.reservation.manage",
        f"user/{scenario.ambassador.id}",
    )


def test_draft_reservation_multiple_users_not_implemented(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {
            "users": [
                UserIdentity(**scenario.root.model_dump()),
                UserIdentity(**scenario.ambassador.model_dump()),
            ]
        },
    )

    # Act / Assert
    with pytest.raises(NotImplementedError):
        reservation_svc.draft_reservation(scenario.ambassador, request)


def test_draft_reservation_user_did_not_accepted_agreement(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    scenario.user.accepted_community_agreement = False
    reservation_svc = make_reservation_service(session)
    request = make_test_request(
        scenario,
        {"users": [UserIdentity(**scenario.user.model_dump())]},
    )

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.user, request)


def test_draft_reservation_room_time_conflict(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    start = scenario.reservation_6.start - timedelta(minutes=30)
    end = scenario.reservation_6.start + timedelta(minutes=30)
    conflict_draft = ReservationRequest(
        seats=[],
        room=scenario.group_a,
        start=start,
        end=end,
        users=[scenario.ambassador],
    )

    # Act / Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, conflict_draft)

    conflict_draft.start = scenario.reservation_6.start
    conflict_draft.end = scenario.reservation_6.end
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, conflict_draft)

    conflict_draft.start = scenario.reservation_6.start + timedelta(minutes=30)
    conflict_draft.end = scenario.reservation_6.end - timedelta(minutes=30)
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, conflict_draft)

    conflict_draft.start = scenario.reservation_6.end - timedelta(minutes=30)
    conflict_draft.end = scenario.reservation_6.end + timedelta(minutes=30)
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.ambassador, conflict_draft)


def test_draft_reservation_room_no_time_conflict_before(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = ReservationRequest(
        seats=[],
        room=scenario.group_b,
        start=scenario.reservation_6.start - timedelta(minutes=30),
        end=scenario.reservation_6.start,
        users=[scenario.ambassador],
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert reservation.id is not None


def test_draft_reservation_room_no_time_conflict_after(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = ReservationRequest(
        seats=[],
        room=scenario.group_b,
        start=scenario.reservation_6.end,
        end=scenario.reservation_6.end + timedelta(minutes=30),
        users=[scenario.ambassador],
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert reservation.id is not None


def test_draft_reservation_different_room_time_conflict(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    request = ReservationRequest(
        seats=[],
        room=scenario.group_b,
        start=scenario.reservation_6.start,
        end=scenario.reservation_6.end,
        users=[scenario.ambassador],
    )

    # Act
    reservation = reservation_svc.draft_reservation(scenario.ambassador, request)

    # Assert
    assert reservation.id is not None


def test_draft_reservation_crosses_weekly_limit(
    session: Session, time: dict[str, datetime]
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time)
    scenario.user.accepted_community_agreement = True
    reservation_svc = make_reservation_service(session)
    temp_draft_1 = ReservationRequest(
        seats=[],
        room=scenario.group_a,
        start=scenario.three_days_from_today.start,
        end=scenario.three_days_from_today.start + timedelta(hours=2),
        users=[scenario.user],
    )
    temp_draft_2 = ReservationRequest(
        seats=[],
        room=scenario.group_a,
        start=scenario.three_days_from_today.start + timedelta(hours=2),
        end=scenario.three_days_from_today.start + timedelta(hours=4),
        users=[scenario.user],
    )
    exceed_limit_draft = ReservationRequest(
        seats=[],
        room=scenario.group_a,
        start=scenario.three_days_from_today.start + timedelta(hours=4),
        end=scenario.three_days_from_today.start + timedelta(hours=6),
        users=[scenario.user],
    )

    # Act
    reservation_svc.draft_reservation(scenario.user, temp_draft_1)
    reservation_svc.draft_reservation(scenario.user, temp_draft_2)

    # Assert
    with pytest.raises(ReservationException):
        reservation_svc.draft_reservation(scenario.user, exceed_limit_draft)
