"""Tests for Coworking Reservation Service."""

import pytest
from unittest.mock import create_autospec

from ....services import PermissionService, UserPermissionError
from ....services.coworking import ReservationService, PolicyService
from ....services.coworking.reservation import ReservationError
from ....models.coworking import (
    Reservation,
    TimeRange,
    ReservationState,
    ReservationPartial,
)
from ....models.user import UserIdentity
from ....models.coworking.seat import SeatIdentity

# Some internal methods use SQLAlchemy layer and are tested here
from sqlalchemy.orm import Session
from ....entities.coworking import ReservationEntity

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (seat_svc) are required to be imported in the testing module.
from .fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)
from .time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ..core_data import setup_insert_data_fixture as insert_order_0
from .operating_hours_data import fake_data_fixture as insert_order_1
from .room_data import fake_data_fixture as insert_order_2
from .seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ..core_data import user_data
from . import operating_hours_data
from . import seat_data
from . import reservation_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_get_current_reservations_for_user_as_user(
    reservation_svc: ReservationService,
):
    """Get reservations for each user _as the user themself_."""
    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.user, user_data.user
    )
    assert len(reservations) == 2
    assert reservations[0].id == reservation_data.reservation_1.id
    assert reservations[1].id == reservation_data.reservation_5.id

    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.ambassador, user_data.ambassador
    )
    assert len(reservations) == 1

    reservations = reservation_svc.get_current_reservations_for_user(
        user_data.root, user_data.root
    )
    assert len(reservations) == 1


def test_get_current_reservations_for_user_permissions(
    reservation_svc: ReservationService,
):
    reservation_svc._permission_svc = create_autospec(reservation_svc._permission_svc)
    reservation_svc.get_current_reservations_for_user(user_data.root, user_data.user)
    reservation_svc._permission_svc.enforce.assert_called_with(
        user_data.root,
        "coworking.reservation.read",
        f"user/{user_data.user.id}",
    )


def test_get_seat_reservations_none(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Get all reservations for a time range with no reservations."""
    in_the_past = TimeRange(
        start=time[THIRTY_MINUTES_AGO] - FIVE_MINUTES,
        end=time[THIRTY_MINUTES_AGO] - ONE_MINUTE,
    )
    reservations = reservation_svc.get_seat_reservations(seat_data.seats, in_the_past)
    assert len(reservations) == 0


def test_get_seat_reservations_active(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Get all reservations that are active (not cancelled or checked out)."""
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    reservations = reservation_svc.get_seat_reservations(seat_data.seats, current)
    assert len(reservations) == len(reservation_data.active_reservations)
    assert isinstance(reservations[0], Reservation)
    assert reservations[0].id == reservation_data.reservation_1.id


def test_get_seat_reservations_unreserved_seats(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Get reservations for unreserved seats (expecting no matches)."""
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    reservations = reservation_svc.get_seat_reservations(
        seat_data.unreservable_seats, current
    )
    assert len(reservations) == 0


def test_state_transition_reservation_entities_by_time_noop(
    session: Session, reservation_svc: ReservationService, time: dict[str, datetime]
):
    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in reservation_data.active_reservations
    ]
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        time[NOW], entities
    )
    assert collected is not entities
    assert collected == entities


def test_state_transition_reservation_entities_by_time_expired_active(
    session: Session, reservation_svc: ReservationService
):
    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in reservation_data.active_reservations
    ]
    cutoff = entities[0].end
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )

    assert len(collected) == len(entities) - 1
    reservation = session.get(ReservationEntity, entities[0].id, populate_existing=True)
    assert reservation.state == ReservationState.CHECKED_OUT


def test_state_transition_reservation_entities_by_time_active_draft(
    session: Session, reservation_svc: ReservationService, policy_svc: PolicyService
):
    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in reservation_data.draft_reservations
    ]
    cutoff = entities[0].created_at + policy_svc.reservation_draft_timeout()
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )
    assert len(collected) == len(entities)
    assert collected[0].state == ReservationState.DRAFT


def test_state_transition_reservation_entities_by_time_expired_draft(
    session: Session, reservation_svc: ReservationService, policy_svc: PolicyService
):
    policy_mock = create_autospec(PolicyService)
    policy_mock.reservation_draft_timeout.return_value = (
        policy_svc.reservation_draft_timeout()
    )
    reservation_svc._policy_svc = policy_mock

    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in reservation_data.draft_reservations
    ]
    cutoff = (
        entities[0].created_at
        + policy_svc.reservation_draft_timeout()
        + timedelta(seconds=1)
    )
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )
    assert len(collected) == len(entities) - 1

    reservation = session.get(ReservationEntity, entities[0].id, populate_existing=True)
    assert reservation.state == ReservationState.CANCELLED

    policy_mock.reservation_draft_timeout.assert_called_once()


def test_state_transition_reservation_entities_by_time_checkin_timeout(
    session: Session, reservation_svc: ReservationService, policy_svc: PolicyService
):
    policy_mock = create_autospec(PolicyService)
    policy_mock.reservation_checkin_timeout.return_value = (
        policy_svc.reservation_checkin_timeout()
    )
    reservation_svc._policy_svc = policy_mock

    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in reservation_data.confirmed_reservations
    ]
    cutoff = (
        entities[0].start
        + policy_svc.reservation_checkin_timeout()
        + timedelta(seconds=1)
    )
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )
    assert len(collected) == len(entities) - 1

    reservation = session.get(ReservationEntity, entities[0].id, populate_existing=True)
    assert reservation.state == ReservationState.CANCELLED

    policy_mock.reservation_checkin_timeout.assert_called_once()


def test_seat_availability_in_past(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """There is no seat availability in the past."""
    past = TimeRange(start=time[THIRTY_MINUTES_AGO], end=time[NOW])
    available_seats = reservation_svc.seat_availability(seat_data.seats, past)
    assert len(available_seats) == 0


def test_seat_availability_while_closed(reservation_svc: ReservationService):
    """There is no seat availability while the XL is closed."""
    closed = TimeRange(
        start=operating_hours_data.today.end,
        end=operating_hours_data.today.end + ONE_HOUR,
    )
    available_seats = reservation_svc.seat_availability(seat_data.seats, closed)
    assert len(available_seats) == 0


def test_seat_availability_truncate_start(
    reservation_svc: ReservationService,
    policy_svc: PolicyService,
    time: dict[str, datetime],
):
    recent_past_to_five_minutes = TimeRange(
        start=time[NOW] - policy_svc.minimum_reservation_duration(),
        end=time[NOW] + FIVE_MINUTES,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.seats, recent_past_to_five_minutes
    )
    assert len(available_seats) == 0


def test_seat_availability_while_completely_open(
    reservation_svc: ReservationService,
):
    """All reservable seats should be available."""
    tomorrow = TimeRange(
        start=operating_hours_data.future.start,
        end=operating_hours_data.future.start + ONE_HOUR,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, tomorrow
    )
    assert len(available_seats) == len(seat_data.reservable_seats)


def test_seat_availability_with_reservation(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Test data has one of the reservable seats reserved."""
    today = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, today
    )
    assert len(available_seats) == len(seat_data.reservable_seats) - 1
    assert available_seats[0].id == seat_data.monitor_seat_10.id


def test_seat_availability_near_requested_start(reservation_svc: ReservationService):
    """When the XL is open and some seats are about to become available."""
    future = TimeRange(
        start=operating_hours_data.today.end - THIRTY_MINUTES - FIVE_MINUTES,
        end=operating_hours_data.today.end + FIVE_MINUTES,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, future
    )
    assert len(available_seats) == len(seat_data.reservable_seats)
    for seat in available_seats:
        assert seat.availability[0].start == reservation_data.reservation_4.end
        assert seat.availability[0].end == operating_hours_data.today.end


def test_seat_availability_all_reserved(reservation_svc: ReservationService):
    """Test when all reservable seats are reserved."""
    future = TimeRange(
        start=reservation_data.reservation_4.start,
        end=reservation_data.reservation_4.end,
    )
    available_seats = reservation_svc.seat_availability(
        seat_data.reservable_seats, future
    )
    assert len(available_seats) == 0


def test_xl_closing_soon(reservation_svc: ReservationService):
    """When the XL is open and upcoming walkins are available, but the closing hour is under default walkin duration."""
    near_closing = TimeRange(
        start=operating_hours_data.tomorrow.end - THIRTY_MINUTES + FIVE_MINUTES,
        end=operating_hours_data.tomorrow.end,
    )
    available_seats = reservation_svc.seat_availability(seat_data.seats, near_closing)
    assert len(available_seats) == 0


def test_draft_reservation_open_seats(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Request with an open seat."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador, reservation_data.test_request()
    )
    assert reservation is not None
    assert reservation.id is not None
    assert reservation.state == ReservationState.DRAFT
    assert_equal_times(time[NOW], reservation.start)
    assert_equal_times(time[IN_THIRTY_MINUTES], reservation.end)
    assert_equal_times(time[NOW], reservation.created_at)
    assert_equal_times(time[NOW], reservation.updated_at)
    assert len(reservation.seats) == 1
    assert len(reservation.users) == 1
    assert reservation.users[0].id == user_data.ambassador.id


def test_draft_reservation_in_past(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Request a reservation that starts in the past. Its start should be now, instead."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        reservation_data.test_request({"start": time[THIRTY_MINUTES_AGO]}),
    )
    assert_equal_times(time[NOW], reservation.start)


def test_draft_reservation_beyond_walkin_limit(reservation_svc: ReservationService):
    """Walkin time limit should be bounded by PolicyService#walkin_initial_duration"""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "start": reservation_data.reservation_1.end,
                "end": reservation_data.reservation_1.end
                + reservation_svc._policy_svc.walkin_initial_duration(user_data.user)
                + timedelta(minutes=10),
            }
        ),
    )
    assert_equal_times(reservation_data.reservation_1.end, reservation.start)
    assert_equal_times(
        reservation_data.reservation_1.end
        + reservation_svc._policy_svc.walkin_initial_duration(user_data.user),
        reservation.end,
    )


def test_draft_reservation_some_taken_seats(reservation_svc: ReservationService):
    """Request with list of some taken, some open seats."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        reservation_data.test_request(
            {
                "seats": [
                    SeatIdentity(
                        **reservation_data.reservation_1.seats[0].model_dump()
                    ),
                    SeatIdentity(**seat_data.monitor_seat_01.model_dump()),
                ]
            }
        ),
    )
    assert len(reservation.seats) == 1
    assert reservation.seats[0].id == seat_data.monitor_seat_01.id


def test_draft_reservation_seat_availability_truncated(
    reservation_svc: ReservationService,
):
    """When walkin requested and seat is reserved later on."""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "start": reservation_data.reservation_1.end,
                "end": operating_hours_data.today.end,
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in reservation_data.reservation_4.seats
                ],
            }
        ),
    )
    assert_equal_times(reservation_data.reservation_4.start, reservation.end)
    assert len(reservation.seats) == 1


def test_draft_reservation_future(reservation_svc: ReservationService):
    """When a reservation is in the future, it has longer limits."""
    future_reservation_limit = (
        reservation_svc._policy_svc.maximum_initial_reservation_duration(user_data.user)
    )
    start = operating_hours_data.future.start
    end = operating_hours_data.future.start + future_reservation_limit
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "seats": [
                    SeatIdentity(**seat.model_dump())
                    for seat in seat_data.reservable_seats
                ],
                "start": start,
                "end": end,
            }
        ),
    )
    assert_equal_times(start, reservation.start)
    assert_equal_times(end, reservation.end)


def test_future_reservation_unreservable(reservation_svc: ReservationService):
    """When a reservation is not a walk-in, only unreservable seats are available."""
    with pytest.raises(ReservationError):
        start = operating_hours_data.tomorrow.start
        end = operating_hours_data.tomorrow.start + ONE_HOUR
        reservation = reservation_svc.draft_reservation(
            user_data.ambassador,
            reservation_data.test_request(
                {
                    "seats": [
                        SeatIdentity(**seat.model_dump())
                        for seat in seat_data.unreservable_seats
                    ],
                    "start": start,
                    "end": end,
                }
            ),
        )


def test_draft_reservation_all_closed_seats(reservation_svc: ReservationService):
    """Request with all closed seats errors."""
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.ambassador,
            reservation_data.test_request(
                {
                    "seats": [
                        SeatIdentity(
                            **reservation_data.reservation_1.seats[0].model_dump()
                        ),
                    ]
                }
            ),
        )


def test_draft_reservation_has_reservation_conflict(
    reservation_svc: ReservationService,
):
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.user,
            reservation_data.test_request(
                {"users": [UserIdentity(**user_data.user.model_dump())]}
            ),
        )


def test_draft_reservation_has_no_users(reservation_svc: ReservationService):
    with pytest.raises(ReservationError):
        reservation = reservation_svc.draft_reservation(
            user_data.user, reservation_data.test_request({"users": []})
        )


def test_draft_reservation_permissions(reservation_svc: ReservationService):
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation = reservation_svc.draft_reservation(
        user_data.root, reservation_data.test_request()
    )
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        user_data.root,
        "coworking.reservation.manage",
        f"user/{user_data.ambassador.id}",
    )


def test_draft_reservation_one_user_for_now(reservation_svc: ReservationService):
    with pytest.raises(ReservationError):
        reservation_svc.draft_reservation(
            user_data.ambassador,
            reservation_data.test_request(
                {
                    "users": [
                        UserIdentity(**user_data.root.model_dump()),
                        UserIdentity(**user_data.ambassador.model_dump()),
                    ]
                }
            ),
        )


def test_change_reservation_not_found(reservation_svc: ReservationService):
    request_reservation = ReservationPartial(id=999)
    with pytest.raises(LookupError):
        reservation_svc.change_reservation(user_data.user, request_reservation)


def test_change_reservation_without_permission(reservation_svc: ReservationService):
    with pytest.raises(UserPermissionError):
        reservation = reservation_svc.change_reservation(
            user_data.user, ReservationPartial(id=4, state=ReservationState.CONFIRMED)
        )


def test_change_reservation_enforces_permissions(reservation_svc: ReservationService):
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation = reservation_svc.change_reservation(
        user_data.root, ReservationPartial(id=5, state=ReservationState.CONFIRMED)
    )
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        user_data.root,
        "coworking.reservation.manage",
        f"user/{reservation_data.reservation_5.users[0].id}",
    )


def test_change_reservation_state_confirmed(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=5, state=ReservationState.CONFIRMED)
    )
    assert reservation_data.reservation_5.id == reservation.id
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_state_confirmed_idempotent(
    reservation_svc: ReservationService,
):
    reservation = reservation_svc.change_reservation(
        user_data.ambassador, ReservationPartial(id=4, state=ReservationState.CONFIRMED)
    )
    assert ReservationState.CONFIRMED == reservation.state


def test_change_reservation_state_noop(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=1, state=ReservationState.CONFIRMED)
    )
    assert reservation_data.reservation_1.state == reservation.state
    assert ReservationState.CONFIRMED != reservation.state


def test_change_reservation_cancel_draft(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=5, state=ReservationState.CANCELLED)
    )
    assert ReservationState.CANCELLED == reservation.state


def test_change_reservation_cancel_confirmed(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.ambassador, ReservationPartial(id=4, state=ReservationState.CANCELLED)
    )
    assert ReservationState.CANCELLED == reservation.state


def test_change_reservation_cancel_checkedin_noop(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=1, state=ReservationState.CANCELLED)
    )
    assert ReservationState.CHECKED_IN == reservation.state


def test_change_reservation_checkout(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=1, state=ReservationState.CHECKED_OUT)
    )
    assert ReservationState.CHECKED_OUT == reservation.state


def test_change_reservation_checkout_draft_noop(reservation_svc: ReservationService):
    reservation = reservation_svc.change_reservation(
        user_data.user, ReservationPartial(id=5, state=ReservationState.CHECKED_OUT)
    )
    assert ReservationState.DRAFT == reservation.state


def test_change_reservation_checkout_confirmed_noop(
    reservation_svc: ReservationService,
):
    reservation = reservation_svc.change_reservation(
        user_data.ambassador,
        ReservationPartial(id=4, state=ReservationState.CHECKED_OUT),
    )
    assert ReservationState.CONFIRMED == reservation.state
