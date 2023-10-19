"""RoleDetails extends the Role model to include the permissions and users associated with the role."""

from pydantic import BaseModel
from . import User, Permission, Role


class RoleDetails(Role):
    """
    Pydantic model to represent a `Role`, including back-populated
    relationship fields.

    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database.
    """
    permissions: list[Permission]
    users: list[User]
