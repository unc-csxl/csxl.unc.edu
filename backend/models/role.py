"""Role is the data object for groups of related access controls users can be added to."""

from pydantic import BaseModel
from . import User, Permission


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Role(BaseModel):
    """A role is a group of related access controls users can be added to."""
    id: int | None = None
    name: str
    
class RoleDetails(Role):
    permissions: list[Permission]
    users: list[User]