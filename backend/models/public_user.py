from pydantic import BaseModel
from datetime import datetime
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

    # Makes `PublicUser` hashable, enabling it to be used in sets.
    def __hash__(self) -> int:
        return self.onyen.__hash__()

    id: int | None
    onyen: str
    first_name: str
    last_name: str
    pronouns: str
    email: str
    github_avatar: str | None = None
    github: str | None = None
    bio: str | None = None
    linkedin: str | None = None
    website: str | None = None
    profile_emoji: str | None = None
    emoji_expiration: datetime | None = None
