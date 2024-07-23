from pydantic import BaseModel
from .registration_type import RegistrationType


__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class PublicUser(BaseModel):
    """
    Pydantic model to represent public information about users to avoid
    exposing sensitive information about them.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database
    """

    id: int | None
    onyen: str
    first_name: str
    last_name: str
    pronouns: str
    email: str
    github_avatar: str | None = None
    github: str | None = None
    bio: str | None = None
