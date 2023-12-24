"""Service that manages rooms in the coworking space."""

from fastapi import Depends
from sqlalchemy.orm import Session
from ...database import db_session
from ...models import RoomDetails
from ...entities import RoomEntity

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RoomService:
    """RoomService is the access layer to coworking rooms. And a good pun."""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes a new RoomService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session

    def list(self) -> list[RoomDetails]:
        """Returns all rooms in the coworking space.

        Returns:
            list[RoomDetails]: All rooms in the coworking space ordered by increasing capacity.
        """
        entities = self._session.query(RoomEntity).order_by(RoomEntity.capacity).all()
        return [entity.to_details_model() for entity in entities]
