"""RoleDetails extends the Role model to include the permissions and users associated with the role."""

from pydantic import BaseModel
from . import User, Permission, Role


class RoleDetails(Role):
    """Represent a Role, but also include its permissions and members (users)."""

    permissions: list[Permission]
    users: list[User]
