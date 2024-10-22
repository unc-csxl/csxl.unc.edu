"""Tests for the RoleService class."""

# Tested Dependencies
from ...models import SignageOverviewFast, SignageOverviewSlow
from ...services import SignageService

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .coworking import seat_data
from .room_data import *
from .coworking.reservation import reservation_data
from .office_hours import office_hours_data

__authors__ = ["Will Zahrt", "Andrew Lockard"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_get_fast_data(signage_svc: SignageService):
    fast_data = signage_svc.get_fast_data()
    assert len(fast_data.active_office_hours) == 1
    assert (
        fast_data.active_office_hours[0].id
        == office_hours_data.comp_110_current_office_hours.id
    )
