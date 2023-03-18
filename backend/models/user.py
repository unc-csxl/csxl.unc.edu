"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class User(BaseModel):
    id: int | None = None
    pid: int
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""


class ProfileForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    pronouns: str
