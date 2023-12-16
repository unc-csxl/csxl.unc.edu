from .permission import Permission
from .user import User, UserIdentity
from .roster_role import RosterRole

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


class SectionStaffUser(UserIdentity):
    """
    Pydantic model to represent the information about a user who is a
    staff of a section of a course.

    This model is based on the `UserEntity` model, which defines the shape
    of the `User` database in the PostgreSQL database
    """

    first_name: str
    last_name: str
    pronouns: str
    member_type: RosterRole
