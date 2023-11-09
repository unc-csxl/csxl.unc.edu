"""Tests for Coworking Rooms Service."""

from ....services.coworking import RoomService
from ....models.coworking import RoomDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import room_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .room_data import fake_data_fixture

# Import the fake model data in a namespace for test assertions
from . import room_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_list(room_svc: RoomService):
    rooms = room_svc.list()
    assert len(rooms) == len(room_data.rooms)
    assert isinstance(rooms[0], RoomDetails)


def test_list_ordered_by_capacity(room_svc: RoomService):
    rooms = room_svc.list()
    for i in range(1, len(rooms)):
        assert rooms[i - 1].capacity <= rooms[i].capacity
