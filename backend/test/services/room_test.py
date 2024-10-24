"""Tests for Coworking Rooms Service."""

from unittest.mock import create_autospec
import pytest
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ...services import RoomService
from ...models import RoomDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import room_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .role_data import fake_data_fixture as fake_role_data_fixture
from .user_data import fake_data_fixture as fake_user_data_fixture
from .room_data import fake_data_fixture as fake_room_data_fixture

# Import the fake model data in a namespace for test assertions
from . import room_data
from . import user_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_list(room_svc: RoomService):
    rooms = room_svc.all()
    assert len(rooms) == len(room_data.rooms)
    assert isinstance(rooms[0], RoomDetails)


def test_list_ordered_by_capacity(room_svc: RoomService):
    rooms = room_svc.all()
    for i in range(1, len(rooms)):
        assert rooms[i - 1].capacity <= rooms[i].capacity


def test_get_by_id(room_svc: RoomService):
    room = room_svc.get_by_id(room_data.group_a.id)

    assert isinstance(room, RoomDetails)
    assert room.id == room_data.group_a.id


def test_get_by_id_not_found(room_svc: RoomService):
    with pytest.raises(ResourceNotFoundException):
        room = room_svc.get_by_id("500")
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(room_svc: RoomService):
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    room = room_svc.create(user_data.root, room_data.new_room)

    permission_svc.enforce.assert_called_with(user_data.root, "room.create", "room/")
    assert isinstance(room, RoomDetails)
    assert room.id == room_data.new_room.id


def test_create_as_user(room_svc: RoomService):
    with pytest.raises(UserPermissionException):
        room = room_svc.create(user_data.user, room_data.new_room)
        pytest.fail()


def test_update_as_root(room_svc: RoomService):
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    room = room_svc.update(user_data.root, room_data.edited_xl)

    permission_svc.enforce.assert_called_with(
        user_data.root, "room.update", f"room/{room.id}"
    )
    assert isinstance(room, RoomDetails)
    assert room.id == room_data.edited_xl.id


def test_update_as_root_not_found(room_svc: RoomService):
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        room = room_svc.update(user_data.root, room_data.new_room)
        pytest.fail()


def test_update_as_user(room_svc: RoomService):
    with pytest.raises(UserPermissionException):
        room = room_svc.create(user_data.user, room_data.edited_xl)
        pytest.fail()


def test_delete_as_root(room_svc: RoomService):
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    room_svc.delete(user_data.root, room_data.group_b.id)

    permission_svc.enforce.assert_called_with(
        user_data.root, "room.delete", f"room/{room_data.group_b.id}"
    )

    rooms = room_svc.all()
    assert len(rooms) == len(room_data.rooms) - 1


def test_delete_as_root_not_found(room_svc: RoomService):
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        room = room_svc.delete(user_data.root, room_data.new_room.id)
        pytest.fail()


def test_delete_as_user(room_svc: RoomService):
    with pytest.raises(UserPermissionException):
        room = room_svc.delete(user_data.user, room_data.the_xl.id)
        pytest.fail()
