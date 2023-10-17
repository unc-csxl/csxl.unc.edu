"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UserIdentity(BaseModel):
    """Users are identified in the system by their `id` field."""

    id: int | None = None


class User(UserIdentity, BaseModel):
    """A user is a registered user of the application."""

    pid: int = 0
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None


class NewUser(User, BaseModel):
    id: int | None = None


class ProfileForm(BaseModel):
    """A profile form is a form for updating a user's profile."""

    first_name: str
    last_name: str
    email: str
    pronouns: str
