"""Tests for the RoleService class."""

# Tested Dependencies
import pytest

from ...models import SignageOverviewFast, SignageOverviewSlow
from ...services import SignageService

# Imported fixtures provide dependencies injected for the tests as parameters.

from .coworking.fixtures import (
    operating_hours_svc,
    policy_svc,
    reservation_svc,
    seat_svc,
)
from .fixtures import permission_svc, room_svc, signage_svc
from .signage_scenario import SignageScenario, arrange_signage_scenario


__authors__ = ["Will Zahrt", "Andrew Lockard"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def signage_scenario(session) -> SignageScenario:
    return arrange_signage_scenario(session)


def test_get_fast_data(signage_svc: SignageService, signage_scenario: SignageScenario):
    """Ensure that the fast data script returns the values as expected."""
    fast_data = signage_svc.get_fast_data()

    assert len(fast_data.active_office_hours) == 2
    assert (
        fast_data.active_office_hours[0].id
        == signage_scenario.comp_110_current_office_hours.id
    )

    assert signage_scenario.reservation.pair_a.id not in fast_data.available_rooms

    available_seats = [seat for seat in fast_data.seat_availability if seat.reservable]
    assert signage_scenario.reservation.monitor_seat_01 not in available_seats
    assert signage_scenario.reservation.monitor_seat_11 not in available_seats


def test_get_slow_data(signage_svc: SignageService, signage_scenario: SignageScenario):
    """Ensures that the slow data returns the values as expected."""
    slow_data = signage_svc.get_slow_data()

    assert all(article.title != signage_scenario.announcement.title for article in slow_data.newest_news)
    assert len(slow_data.newest_news) == 2

    assert len(slow_data.events) == 3

    assert len(slow_data.top_users) == 3
    assert slow_data.top_users[0].first_name == signage_scenario.reservation.ambassador.first_name
    assert slow_data.top_users[0].last_name == signage_scenario.reservation.ambassador.last_name
    assert slow_data.top_users[1].first_name == signage_scenario.reservation.root.first_name
    assert slow_data.top_users[1].last_name == signage_scenario.reservation.root.last_name
    assert slow_data.top_users[2].first_name == signage_scenario.reservation.user.first_name
    assert slow_data.top_users[2].last_name == signage_scenario.reservation.user.last_name

    assert len(slow_data.announcements) == 1
    assert slow_data.announcements[0].title == "Sample Announcement"
