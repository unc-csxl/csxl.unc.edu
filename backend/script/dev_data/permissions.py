"""Sample permissions."""

from ...models import Permission
from . import roles

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

pairs = [
    (roles.sudoer, Permission(action="*", resource="*")),
    (roles.staff, Permission(action="admin.*", resource="*")),
    (roles.staff, Permission(action="user.*", resource="*")),
    (roles.staff, Permission(action="role.*", resource="*")),
    (roles.staff, Permission(action="checkin.*", resource="*")),
    (roles.staff, Permission(action="organizations.*", resource="*")),
    (roles.ambassador, Permission(action="user.search", resource="*")),
    (roles.ambassador, Permission(action="checkin.*", resource="*"))
]
