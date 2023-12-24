"""
The Room Service allows the API to manipulate rooms data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models import Room
from ..models import RoomDetails
from ..models.user import User
from ..entities import RoomEntity
from .permission import PermissionService

from ..services.exceptions import ResourceNotFoundException
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RoomService:
    """Service that performs all of the actions on the `Room` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def all(self) -> list[RoomDetails]:
        """Retrieves all rooms from the table

        Returns:
            list[RoomDetails]: List of all `RoomDetails`
        """
        # Select all entries in `Room` table
        entities = self._session.query(RoomEntity).order_by(RoomEntity.capacity).all()

        # Convert entries to a model and return
        return [entity.to_details_model() for entity in entities]

    def get_by_id(self, id: str) -> RoomDetails:
        """Gets the room from the table for an id.

        Args:
            id: ID of the room to retrieve.
        Returns:
            RoomDetails: Room based on the id.
        """
        # Select all entries in the `Room` table and sort by end date
        query = select(RoomEntity).filter(RoomEntity.id == id)
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(f"Room with id: {id} does not exist.")

        # Return the model
        return entity.to_details_model()

    def create(self, subject: User, room: RoomDetails) -> RoomDetails:
        """Creates a new room.

        Args:
            subject: a valid User model representing the currently logged in User
            room: Room to add to table

        Returns:
            RoomDetails: Object added to table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "room.create", f"room/")

        # Create new object
        room_entity = RoomEntity.from_model(room)

        # Add new object to table and commit changes
        self._session.add(room_entity)
        self._session.commit()

        # Return added object
        return room_entity.to_details_model()

    def update(self, subject: User, room: RoomDetails) -> RoomDetails:
        """Updates a room.

        Args:
            subject: a valid User model representing the currently logged in User
            room: Room to update

        Returns:
            RoomDetails: Object updated in the table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "room.update", f"room/{room.id}")

        # Find the entity to update
        room_entity = self._session.get(RoomEntity, room.id)

        # Raise an error if no entity was found
        if room_entity is None:
            raise ResourceNotFoundException(f"Room with id: {room.id} does not exist.")

        # Update the entity
        room_entity.nickname = room.nickname
        room_entity.building = room.building
        room_entity.room = room.room
        room_entity.capacity = room.capacity
        room_entity.reservable = room.reservable

        # Commit changes
        self._session.commit()

        # Return edited object
        return room_entity.to_details_model()

    def delete(self, subject: User, id: str) -> None:
        """Deletes a room.

        Args:
            subject: a valid User model representing the currently logged in User
            id: ID of room to delete
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "room.delete", f"room/{id}")

        # Find the entity to delete
        room_entity = self._session.get(RoomEntity, id)

        # Raise an error if no entity was found
        if room_entity is None:
            raise ResourceNotFoundException(f"Room with id: {id} does not exist.")

        # Delete and commit changes
        self._session.delete(room_entity)
        self._session.commit()
