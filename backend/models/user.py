"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel
from .unregistered_user import UnregisteredUser


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class User(UnregisteredUser, BaseModel):
    """A user is a registered user of the application."""

    id: int | None = None
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None


class UserPartial(User, BaseModel):
    pid: int | None = None
    onyen: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    pronouns: str | None = None
    github: str | None = None
    github_id: int | None = None
    github_avatar: str | None = None


class UserIdentity(UserPartial, BaseModel):
    id: int


class ProfileForm(BaseModel):
    """A profile form is a form for updating a user's profile."""

    first_name: str
    last_name: str
    email: str
    pronouns: str
