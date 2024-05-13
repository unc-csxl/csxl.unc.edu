"""RoomDetails provides more information about a room in the coworking space.

Importantly, it includes a room's seats, if seats are reservable as in the XL collab.
"""

from .room import Room
from .coworking.seat import Seat

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RoomDetails(Room):
    building: str
    room: str
    capacity: int
    reservable: bool
    description: str
    seats: list[Seat] = []

    def to_room(self) -> Room:
        """Converts the details model to a room model.

        Returns:
            Room: The model representation of the entity."""
        return Room(id=self.id, nickname=self.nickname)
