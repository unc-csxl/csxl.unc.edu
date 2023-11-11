from pydantic import BaseModel
from .event import Event
from .user import User

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EventRegistration(BaseModel):
    """
    Pydantic model to represent an `EventRegistration`.

    This model is based on the `EventRegistrationEntity` model, which
    defines the shape of the `EventRegistration` table in the PostgreSQL database
    """

    event_id: int
    user_id: int
    event: Event
    user: User
