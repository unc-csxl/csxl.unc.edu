"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel
from .unregistered_user import UnregisteredUser


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"



class User(UnregisteredUser):
    """A user is a registered user of the application."""
    id: int | None = None
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None


class ProfileForm(BaseModel):
    """A profile form is a form for updating a user's profile."""
    first_name: str
    last_name: str
    email: str
    pronouns: str
