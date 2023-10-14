"""ReservationService#_state_transition tests"""

import pytest
from unittest.mock import create_autospec

from .....services import PermissionService, UserPermissionException
from .....services.coworking import ReservationService, PolicyService
from .....services.coworking.reservation import ReservationError
from .....models.coworking import (
    Reservation,
    TimeRange,
    ReservationState,
    ReservationPartial,
)
from .....models.user import UserIdentity
from .....models.coworking.seat import SeatIdentity

# Some internal methods use SQLAlchemy layer and are tested here
from sqlalchemy.orm import Session
from .....entities.coworking import ReservationEntity

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (seat_svc) are required to be imported in the testing module.
from ..fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)
from ..time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..operating_hours_data import fake_data_fixture as insert_order_1
from ..room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import operating_hours_data
from .. import seat_data
from . import reservation_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


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
