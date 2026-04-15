"""Tests for ReservationService#get_map_reservations_for_date and helper functions."""

import pytest
from sqlalchemy.orm import Session

from .scenario import arrange_standard_reservation_scenario, make_reservation_service
from ..time import time_data

__authors__ = [
    "Yuvraj Jain",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_get_total_time_user_reservations_student(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    hours = reservation_svc.get_total_time_user_reservations(scenario.user)

    # Assert
    assert hours == "4.5"


def test_get_total_time_user_reservations_ambassador(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    hours = reservation_svc.get_total_time_user_reservations(scenario.ambassador)

    # Assert
    assert hours == "6"


def test_get_total_time_user_reservations_root(session: Session):
    # Arrange
    scenario = arrange_standard_reservation_scenario(session, time_data())
    reservation_svc = make_reservation_service(session)

    # Act
    hours = reservation_svc.get_total_time_user_reservations(scenario.root)

    # Assert
    assert hours == "6"
