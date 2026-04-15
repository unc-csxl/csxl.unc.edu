"""Tests for Coworking Rooms Service."""

from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService

from ...models import RoomDetails
from ...services import RoomService
from .auth_scenario import arrange_auth_scenario
from .fixtures import room_svc
from .room_scenario import arrange_room_scenario

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_list(session: Session, room_svc: RoomService):
    # Arrange
    scenario = arrange_room_scenario(session)

    # Act
    rooms = room_svc.all()

    # Assert
    assert len(rooms) == len(scenario.rooms)
    assert isinstance(rooms[0], RoomDetails)


def test_list_ordered_by_name(session: Session, room_svc: RoomService):
    # Arrange
    arrange_room_scenario(session)

    # Act
    rooms = room_svc.all()

    # Assert
    for i in range(1, len(rooms)):
        assert rooms[i - 1].nickname <= rooms[i].nickname


def test_get_by_id(session: Session, room_svc: RoomService):
    # Arrange
    scenario = arrange_room_scenario(session)

    # Act
    room = room_svc.get_by_id(scenario.group_a.id)

    # Assert
    assert isinstance(room, RoomDetails)
    assert room.id == scenario.group_a.id


def test_get_by_id_not_found(session: Session, room_svc: RoomService):
    # Arrange
    arrange_room_scenario(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        room_svc.get_by_id("500")
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    # Act
    room = room_svc.create(auth.root, scenario.new_room)

    # Assert
    permission_svc.enforce.assert_called_with(auth.root, "room.create", "room/")
    assert isinstance(room, RoomDetails)
    assert room.id == scenario.new_room.id


def test_create_as_user(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        room_svc.create(auth.user, scenario.new_room)
        pytest.fail()


def test_update_as_root(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    # Act
    room = room_svc.update(auth.root, scenario.edited_xl)

    # Assert
    permission_svc.enforce.assert_called_with(
        auth.root, "room.update", f"room/{room.id}"
    )
    assert isinstance(room, RoomDetails)
    assert room.id == scenario.edited_xl.id


def test_update_as_root_not_found(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        room_svc.update(auth.root, scenario.new_room)
        pytest.fail()


def test_update_as_user(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        room_svc.update(auth.user, scenario.edited_xl)
        pytest.fail()


def test_delete_as_root(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    # Act
    room_svc.delete(auth.root, scenario.group_b.id)

    # Assert
    permission_svc.enforce.assert_called_with(
        auth.root, "room.delete", f"room/{scenario.group_b.id}"
    )

    rooms = room_svc.all()
    assert len(rooms) == len(scenario.rooms) - 1


def test_delete_as_root_not_found(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)
    permission_svc = create_autospec(PermissionService)
    room_svc._permission_svc = permission_svc

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        room_svc.delete(auth.root, scenario.new_room.id)
        pytest.fail()


def test_delete_as_user(session: Session, room_svc: RoomService):
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_room_scenario(session)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        room_svc.delete(auth.user, scenario.the_xl.id)
        pytest.fail()
