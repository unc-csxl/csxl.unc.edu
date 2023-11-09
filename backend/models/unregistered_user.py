"""Unregistered User model prior to completing registration."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UnregisteredUser(BaseModel):
    """
    Pydantic model to represent an `User` that is newly created.
    This model is used as the request to create a user in the service.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database.
    """

    pid: int
    onyen: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
