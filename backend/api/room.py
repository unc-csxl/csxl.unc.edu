"""Room API

Room routes are used to create, retrieve, and update Rooms."""

from fastapi import APIRouter, Depends

from ..services import RoomService
from ..models import Room
from ..models import RoomDetails
from ..api.authentication import registered_user
from ..models.user import User

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/room")
openapi_tags = {
    "name": "Rooms",
    "description": "Create, update, delete, and retrieve rooms.",
}


@api.get("", response_model=list[RoomDetails], tags=["Rooms"])
def get_rooms(
    room_service: RoomService = Depends(),
) -> list[RoomDetails]:
    """
    Get all room

    Parameters:
        room_service: a valid RoomService

    Returns:
        list[RoomDetails]: All rooms in the `Room` database table
    """
    return room_service.all()


@api.get(
    "/{id}",
    response_model=RoomDetails,
    tags=["Rooms"],
)
def get_room_by_id(id: str, room_service: RoomService = Depends()) -> RoomDetails:
    """
    Get room with matching id

    Parameters:
        id: a string representing a unique identifier for a room
        room_service: a valid RoomService

    Returns:
        RoomDetails: RoomDetails with matching slug
    """

    return room_service.get_by_id(id)


@api.post("", response_model=RoomDetails, tags=["Rooms"])
def new_room(
    room: RoomDetails,
    subject: User = Depends(registered_user),
    room_service: RoomService = Depends(),
) -> RoomDetails:
    """
    Create room

    Parameters:
        room: a valid room model
        subject: a valid User model representing the currently logged in User
        room_service: a valid RoomService

    Returns:
        RoomDetails: Created room
    """

    return room_service.create(subject, room)


@api.put(
    "",
    response_model=RoomDetails,
    tags=["Rooms"],
)
def update_room(
    room: RoomDetails,
    subject: User = Depends(registered_user),
    room_service: RoomService = Depends(),
) -> RoomDetails:
    """
    Update room

    Parameters:
        room: a valid Room model
        subject: a valid User model representing the currently logged in User
        room_service: a valid RoomService

    Returns:
        RoomDetails: Updated room
    """

    return room_service.update(subject, room)


@api.delete("/{id}", response_model=None, tags=["Rooms"])
def delete_organization(
    id: str,
    subject: User = Depends(registered_user),
    room_service: RoomService = Depends(),
):
    """
    Delete room based on id

    Parameters:
        id: a string representing a unique identifier for an room
        subject: a valid User model representing the currently logged in User
        room_service: a valid RoomService
    """

    room_service.delete(subject, id)
