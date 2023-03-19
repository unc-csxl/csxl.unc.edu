"""Sample user/role pairings."""

from . import users
from . import roles

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

pairs = [
    (users.root, roles.sudoer),
    (users.merritt_manager, roles.staff),
    (users.arden_ambassador, roles.ambassador)
]
