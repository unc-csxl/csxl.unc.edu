"""Permissions can grant acccess of actions + resources to users and roles."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Permission(BaseModel):
    id: int | None = None
    action: str
    resource: str