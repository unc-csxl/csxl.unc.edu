"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class User(BaseModel):
    """A user is a registered user of the application."""
    id: int | None = None
    pid: int
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None
    permissions: list['Permission'] = []


class NewUser(BaseModel):
    """A new user is a user that has not yet been registered."""
    pid: int
    onyen: str
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    pronouns: str = ''
    permissions: list['Permission'] = []


class ProfileForm(BaseModel):
    """A profile form is a form for updating a user's profile."""
    first_name: str
    last_name: str
    email: str
    pronouns: str


# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .permission import Permission
User.update_forward_refs()
NewUser.update_forward_refs()
