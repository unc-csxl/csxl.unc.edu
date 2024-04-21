"""Tests for Coworking Rooms Service."""

from ....services.coworking import SeatService
from ....models.coworking import SeatDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import seat_svc

# Import core data to ensure all data loads for the tests.
from ..core_data import setup_insert_data_fixture

# Import the fake model data in a namespace for test assertions
from . import seat_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_list(seat_svc: SeatService):
    seats = seat_svc.list()
    assert len(seats) == len(seat_data.seats)
    assert isinstance(seats[0], SeatDetails)
