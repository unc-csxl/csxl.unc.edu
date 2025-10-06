"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel
from datetime import datetime

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UserIdentity(BaseModel):
    """
    Pydantic model to represent how `User`s are identified in the system.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database.
    """

    id: int | None = None


class User(UserIdentity, BaseModel):
    """
    Pydantic model to represent a registered `User`.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database
    """

    pid: int = 0
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None
    accepted_community_agreement: bool = False
    bio: str | None = None
    linkedin: str | None = None
    website: str | None = None
    profile_emoji: str | None = None
    emoji_expiration: datetime | None = None


class NewUser(User, BaseModel):
    """
    Pydantic model to represent how `User`s are once created.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database.
    """

    id: int | None = None


class ProfileForm(BaseModel):
    """
    Pydantic model to represent fields for a form when updating
    a user profile on the frontend.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database
    """

    first_name: str
    last_name: str
    pronouns: str
    email: str
    accepted_community_agreement: bool = False
    bio: str | None = None
    linkedin: str | None = None
    website: str | None = None
    profile_emoji: str | None = None
    emoji_expiration: datetime | None = None
