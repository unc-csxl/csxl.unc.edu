"""RoomDetails provides more information about a room in the coworking space.

Importantly, it includes a room's seats, if seats are reservable as in the XL collab.
"""

from .room import Room
from .coworking.seat import Seat

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class RoomDetails(Room):
    """
    Pydantic model to represent an `Room`, including back-populated
    relationship fields.

    This model is based on the `RoomEntity` model, which defines the shape
    of the `Room` database in the PostgreSQL database.
    """
    building: str
    room: str
    capacity: int
    reservable: bool
    seats: list[Seat] = []
    section_id: int | None = None

    def to_room(self) -> Room:
        """Converts the details model to a room model.

        Returns:
            Room: The model representation of the entity."""
        return Room(id=self.id, nickname=self.nickname)
