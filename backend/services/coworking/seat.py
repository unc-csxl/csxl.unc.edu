"""Service that manages seats in the coworking space."""

from fastapi import Depends
from sqlalchemy.orm import Session
from ...database import db_session
from ...models.coworking import Seat, SeatDetails
from ...entities.coworking import SeatEntity

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SeatService:
    """SeatService is the access layer to coworking seats."""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes a new RoomService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session

    def list(self) -> list[SeatDetails]:
        """Returns all seats in the coworking space.

        Returns:
            list[SeatDetails]: All rooms in the coworking space orderd by increasing capacity.
        """
        entities = self._session.query(SeatEntity).all()
        return [entity.to_model() for entity in entities]
