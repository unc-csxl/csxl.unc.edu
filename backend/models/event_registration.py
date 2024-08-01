from pydantic import BaseModel
from .user import User
from .registration_type import RegistrationType
from .event import EventOverview

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class NewEventRegistration(BaseModel):
    """
    Pydantic model to represent an `EventRegistration`.

    This model is based on the `EventRegistrationEntity` model, which
    defines the shape of the `EventRegistration` table in the PostgreSQL database

    This model is needed for the creation of new registrations in the event service
    """

    event_id: int
    user_id: int
    registration_type: RegistrationType


class EventRegistration(NewEventRegistration):
    """
    Pydantic model to represent an `EventRegistration`.

    This model is based on the `EventRegistrationEntity` model, which
    defines the shape of the `EventRegistration` table in the PostgreSQL database
    """

    event: EventOverview
    user: User
