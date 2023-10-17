"""Unregistered User model prior to completing registration."""

from pydantic import BaseModel


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