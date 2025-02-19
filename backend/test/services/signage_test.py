"""Tests for the RoleService class."""

# Tested Dependencies
import pytest

from sqlalchemy.orm import Session

from backend.models.public_user import PublicUser

from ...models import SignageOverviewFast, SignageOverviewSlow
from ...services import SignageService

# Imported fixtures provide dependencies injected for the tests as parameters.

from .fixtures import signage_svc
from .coworking.time import time
from .coworking.fixtures import *

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture as insert_order_0
from .academics.term_data import fake_data_fixture as insert_order_1
from .academics.course_data import fake_data_fixture as insert_order_2
from .academics.section_data import fake_data_fixture as insert_order_3
from .room_data import fake_data_fixture as insert_order_4
from .coworking.seat_data import fake_data_fixture as insert_order_5
from .coworking.operating_hours_data import fake_data_fixture as insert_order_6
from .coworking.reservation.reservation_data import (
    fake_data_fixture as insert_order_7,
)

from .office_hours.office_hours_data import (
    fake_data_fixture as insert_order_8,
)
from .signage_data import fake_data_fixture as insert_order_9
from .articles.article_data import fake_data_fixture as insert_order_10


#  Import the fake model data in a namespace for test assertions
from .coworking import seat_data
from . import room_data, user_data
from .coworking.reservation import reservation_data
from .office_hours import office_hours_data
from .articles import article_data
from .event import event_test_data
from . import signage_data


__authors__ = ["Will Zahrt", "Andrew Lockard"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_fast_data(signage_svc: SignageService):
    """Ensure that the fast data script returns the values as expected."""
    fast_data = signage_svc.get_fast_data()

    assert len(fast_data.active_office_hours) == 2
    assert (
        fast_data.active_office_hours[0].id
        == office_hours_data.comp_110_current_office_hours.id
    )

    assert room_data.pair_a.id not in fast_data.available_rooms

    available_seats = [seat for seat in fast_data.seat_availability if seat.reservable]
    assert seat_data.monitor_seat_01 not in available_seats
    assert seat_data.monitor_seat_11 not in available_seats


def test_get_slow_data(signage_svc: SignageService):
    """Ensures that the slow data returns the values as expected."""
    slow_data = signage_svc.get_slow_data()

    assert article_data.announcement not in slow_data.newest_news
    assert len(slow_data.newest_news) == 2

    assert len(slow_data.events) == 3

    assert len(slow_data.top_users) == 3
    assert slow_data.top_users[0].id == user_data.ambassador.id
    assert slow_data.top_users[1].id == user_data.root.id
    assert slow_data.top_users[2].id == user_data.user.id

    assert len(slow_data.announcements) == 1
    assert slow_data.announcements[0].title == "Sample Announcement"
