"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel
from .permission import Permission


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UnregisteredUser(BaseModel):
    """A new user is a user that has not yet been registered."""
    pid: int
    onyen: str
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    pronouns: str = ''


class User(UnregisteredUser):
    """A user is a registered user of the application."""
    id: int | None = None
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None


class UserDetails(User):
    """UserDetails extends User model to include permissions."""
    permissions: list['Permission'] = []


class ProfileForm(BaseModel):
    """A profile form is a form for updating a user's profile."""
    first_name: str
    last_name: str
    email: str
    pronouns: str
