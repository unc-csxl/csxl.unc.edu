from .permission import Permission
from .user import User
from .event_registration import EventRegistration

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UserPermissions(User):
    """
    Pydantic model to represent a `User`, including the permissions
    a user has.

    This model is based on the `UserEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """

    permissions: list["Permission"] = []


class UserDetails(UserPermissions):
    """
    Pydantic model to represent a `User`, including back-populated
    relationship fields.

    This model is based on the `UserEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """

    ...
    event_registrations: list[EventRegistration] = []
