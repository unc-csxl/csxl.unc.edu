"""Sample permissions."""

from models import Permission
from . import roles

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

models = [
    Permission(action="*", resource="*", role=roles.admin),
    Permission(action="user/*", resource="user/*", roles=roles.staff),
    Permission(action="checkin/*", resource="checkin/*", roles=roles.staff),
    Permission(action="user/search", resource="user/*", role=roles.ambassador),
    Permission(action="checkin/*", resource="checkin/*", role=roles.ambassador)
]
