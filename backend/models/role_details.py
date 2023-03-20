from pydantic import BaseModel
from . import User, Permission

class RoleDetails(BaseModel):
    id: int | None = None
    name: str
    permissions: list[Permission]
    users: list[User]