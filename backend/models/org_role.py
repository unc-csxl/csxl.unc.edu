from pydantic import BaseModel
from .user import User
from .organization import Organization

from datetime import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OrgRole(BaseModel):
    """
    Model to represent `Role` connections between users and organizations

    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database
    """

    id: int | None = None
    user_id: int
    org_id: int
    membership_type: int
    timestamp: datetime


class OrgRoleDetail(OrgRole):
    """
    Model to represent `Role` connections between users and organizations

    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database
    """

    organization: Organization = None
    user: User | None = None
