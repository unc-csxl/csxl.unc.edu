"""Tests for Coworking Rooms Service."""

from ....services.coworking import SeatService
from ....models.coworking import SeatDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import seat_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .room_data import fake_data_fixture as insert_room_fake_data
from .seat_data import fake_data_fixture as insert_seat_fake_data

# Import the fake model data in a namespace for test assertions
from . import seat_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_list(seat_svc: SeatService):
    seats = seat_svc.list()
    assert len(seats) == len(seat_data.seats)
    assert isinstance(seats[0], SeatDetails)
