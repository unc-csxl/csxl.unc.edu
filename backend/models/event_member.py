from pydantic import BaseModel
from .registration_type import RegistrationType


__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EventMember(BaseModel):
    """
    Pydantic model to represent the information about a user who is
    registered for an event.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database
    """

    id: int
    registration_type: RegistrationType
