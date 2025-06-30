from pydantic import BaseModel
from enum import Enum
from .public_user import PublicUser
from .academics import Term

__authors__ = ["Alanna Zhang, Alexander Feng"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OrganizationMembershipStatus(Enum):
    """Enum to represent the status of an organization membership."""

    ACTIVE = "Active"
    PENDING = "Membership pending"


class OrganizationPermissionLevel(Enum):
    """Enum to represent the level of administrative permissions in an organization."""

    ADMIN = "Admin"
    MEMBER = "Member"


class OrganizationMembership(BaseModel):
    """Pydantic model to represent an organization membership in the roster."""

    id: int | None = None
    user: PublicUser
    organization_id: int
    organization_name: str
    organization_slug: str
    title: str
    permission_level: OrganizationPermissionLevel
    status: OrganizationMembershipStatus
    term: Term


class OrganizationMembershipRegistration(BaseModel):
    """Pydantic model for creating a new membership"""

    id: int | None = None
    user_id: int
    organization_id: int
    title: str = "Member"
    permission_level: OrganizationPermissionLevel = OrganizationPermissionLevel.MEMBER
    status: OrganizationMembershipStatus = OrganizationMembershipStatus.ACTIVE
    term_id: str | None = None
