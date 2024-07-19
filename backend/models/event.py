from pydantic import BaseModel
from datetime import datetime

from .public_user import PublicUser
from .registration_type import RegistrationType

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2024"
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
    image_url: str | None = None


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


class EventOverview(BaseModel):
    id: int
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    number_registered: int
    registration_limit: int
    organization_slug: str
    organization_icon: str
    organization_name: str
    organizers: list[PublicUser]
    user_registration_type: RegistrationType | None
    image_url: str | None
