"""Permissions grant acccess to actions + resources for users and roles."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Permission(BaseModel):
    """A permission grants access to an action on a resource."""
    id: int | None = None
    action: str
    resource: str