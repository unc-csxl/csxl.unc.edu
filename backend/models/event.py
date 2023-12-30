from pydantic import BaseModel
from datetime import datetime

from .event_member import EventMember

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
    can_register: bool
    organization_id: int
    organizers: list[EventMember] = []


class Event(DraftEvent):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int
    registration_count: int = 0
    is_attendee: bool = False
    attendees: list[EventMember] = []
    is_organizer: bool = False
