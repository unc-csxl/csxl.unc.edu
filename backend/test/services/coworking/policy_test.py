"""Tests for Coworking Policy Service."""

from datetime import datetime

import pytest

from ....services.coworking import PolicyService
from ....services.coworking.policy import (
    OH_HOURS,
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY,
)

__authors__ = ["Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.mark.parametrize(
    ("date", "expected_hours"),
    [
        (datetime(2026, 4, 13, 9), OH_HOURS[MONDAY]),
        (datetime(2026, 4, 14, 9), OH_HOURS[TUESDAY]),
        (datetime(2026, 4, 15, 9), OH_HOURS[WEDNESDAY]),
        (datetime(2026, 4, 16, 9), OH_HOURS[THURSDAY]),
        (datetime(2026, 4, 17, 9), OH_HOURS[FRIDAY]),
        (datetime(2026, 4, 18, 9), OH_HOURS[SATURDAY]),
        (datetime(2026, 4, 19, 9), OH_HOURS[SUNDAY]),
    ],
)
def test_office_hours_by_weekday(date: datetime, expected_hours: dict):
    # Arrange
    policy_svc = PolicyService()

    # Act
    office_hours = policy_svc.office_hours(date)

    # Assert
    assert office_hours == expected_hours
