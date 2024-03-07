"""Room models the essential information about a room in the coworking space."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Room(BaseModel):
    id: str
    nickname: str = ""


class RoomPartial(Room):
    nickname: str | None = None
