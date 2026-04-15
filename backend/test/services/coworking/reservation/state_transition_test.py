"""ReservationService#_state_transition tests"""

from datetime import timedelta

import pytest
from unittest.mock import create_autospec

from .....services.coworking import PolicyService
from .....models.coworking import ReservationState

# Some internal methods use SQLAlchemy layer and are tested here
from sqlalchemy.orm import Session
from .....entities.coworking import ReservationEntity
from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import NOW, time_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_state_transition_reservation_entities_by_time_noop(
    session: Session,
):
    # Arrange
    time = time_data()
    scenario = arrange_standard_reservation_scenario(session, time)
    reservation_svc = make_reservation_service(session)
    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in scenario.active_reservations
    ]

    # Act
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        time[NOW], entities
    )

    # Assert
    assert collected is not entities
    assert collected == entities


def test_state_transition_reservation_entities_by_time_expired_active(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)
    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in scenario.active_reservations
    ]
    cutoff = entities[0].end

    # Act
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )

    # Assert
    assert len(collected) == len(entities) - 1
    reservation = session.get(ReservationEntity, entities[0].id, populate_existing=True)
    assert reservation.state == ReservationState.CHECKED_OUT


def test_state_transition_reservation_entities_by_time_active_draft(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    policy_svc = PolicyService()
    reservation_svc = make_reservation_service(session, policy_svc=policy_svc)
    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in scenario.draft_reservations
    ]
    cutoff = entities[0].created_at + policy_svc.reservation_draft_timeout()

    # Act
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )

    # Assert
    assert len(collected) == len(entities)
    assert collected[0].state == ReservationState.DRAFT


def test_state_transition_reservation_entities_by_time_expired_draft(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    policy_svc = PolicyService()
    reservation_svc = make_reservation_service(session)

    policy_mock = create_autospec(PolicyService)
    policy_mock.reservation_draft_timeout.return_value = (
        policy_svc.reservation_draft_timeout()
    )
    reservation_svc._policy_svc = policy_mock

    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in scenario.draft_reservations
    ]
    cutoff = (
        entities[0].created_at
        + policy_svc.reservation_draft_timeout()
        + timedelta(seconds=1)
    )

    # Act
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )

    # Assert
    assert len(collected) == len(entities) - 1

    reservation = session.get(ReservationEntity, entities[0].id, populate_existing=True)
    assert reservation.state == ReservationState.CANCELLED

    policy_mock.reservation_draft_timeout.assert_called_once()


def test_state_transition_reservation_entities_by_time_checkin_timeout(
    session: Session,
):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    policy_svc = PolicyService()
    reservation_svc = make_reservation_service(session)

    policy_mock = create_autospec(PolicyService)
    policy_mock.reservation_checkin_timeout.return_value = (
        policy_svc.reservation_checkin_timeout()
    )
    reservation_svc._policy_svc = policy_mock

    entities: list[ReservationEntity] = [
        session.get(ReservationEntity, reservation.id)
        for reservation in scenario.confirmed_reservations
    ]
    cutoff = (
        entities[0].start
        + policy_svc.reservation_checkin_timeout()
        + timedelta(seconds=1)
    )

    # Act
    collected = reservation_svc._state_transition_reservation_entities_by_time(
        cutoff, entities
    )

    # Assert
    assert len(collected) == len(entities) - 1

    reservation = session.get(ReservationEntity, entities[0].id, populate_existing=True)
    assert reservation.state == ReservationState.CANCELLED

    policy_mock.reservation_checkin_timeout.assert_called_once()
