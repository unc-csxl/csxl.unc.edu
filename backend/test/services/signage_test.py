"""Tests for the RoleService class."""

# Tested Dependencies
import pytest

from sqlalchemy.orm import Session

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


#  Import the fake model data in a namespace for test assertions
from .coworking import seat_data
from . import room_data, user_data
from .coworking.reservation import reservation_data
from .office_hours import office_hours_data

__authors__ = ["Will Zahrt", "Andrew Lockard"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

def test_get_fast_data(signage_svc: SignageService):
    fast_data = signage_svc.get_fast_data()
    assert len(fast_data.active_office_hours) == 1
    assert (
        fast_data.active_office_hours[0].id
        == office_hours_data.comp_110_current_office_hours.id
    )
    available_rooms = [room.id for room in room_data.rooms]
    assert room_data.pair_a.id not in available_rooms

    available_seats = [seat for seat in fast_data.seat_availability if seat.reservable]
    assert seat_data.monitor_seat_01 not in available_seats
    assert seat_data.monitor_seat_11 not in available_seats
