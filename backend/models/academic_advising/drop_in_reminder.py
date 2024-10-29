from pydantic import BaseModel
from ..user import User
from .drop_in import DropIn

__authors__ = ["Emmalyn Foster"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class NewDropInReminder(BaseModel):
    """
    Pydantic model to represent an `EventRegistration`.

    This model is based on the `EventRegistrationEntity` model, which
    defines the shape of the `EventRegistration` table in the PostgreSQL database

    This model is needed for the creation of new registrations in the event service
    """

    drop_in_id: int
    user_id: int


class DropInReminder(NewDropInReminder):
    """
    Pydantic model to represent an `EventRegistration`.

    This model is based on the `EventRegistrationEntity` model, which
    defines the shape of the `EventRegistration` table in the PostgreSQL database
    """

    drop_in: DropIn
    user: User
