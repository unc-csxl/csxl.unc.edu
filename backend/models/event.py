from pydantic import BaseModel
from datetime import datetime

from .public_user import PublicUser

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class DraftEvent(BaseModel):
    """
    Pydantic model to represent an `Event` that has not been created yet.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    name: str
    time: datetime
    location: str
    description: str
    public: bool
    registration_limit: int
    organization_id: int
    organizers: list[PublicUser] = []


class Event(DraftEvent):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int
    registration_count: int = 0
    is_attendee: bool = False
    is_organizer: bool = False
