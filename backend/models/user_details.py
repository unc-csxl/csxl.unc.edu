from .permission import Permission
from .user import User


class UserPermissions(User):
    """UserPermissions adds Permissions to the User model."""

    permissions: list["Permission"] = []


class UserDetails(UserPermissions):
    """UserDetails extends User model to include relations."""
    ...