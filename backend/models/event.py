from pydantic import BaseModel
from datetime import datetime

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


class Event(DraftEvent):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int


class UserEvent(Event):
    """
    Pydantic model to represent a `UserEvent`.

    This model contains an extra "is registered" field denoting whether the
    currently logged in user is registered for an event or not.
    """

    is_registered: bool = False
