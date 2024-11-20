from pydantic import BaseModel
from . import User, Organization
from .organization_role import OrganizationRole

__authors__ = ["Alanna Zhang"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OrganizationMembership(BaseModel):
    """Pydantic model to represent an organization member in the roster."""

    id: int | None = None
    user: User
    organization_id: int
    organization_slug: str
    organization_role: OrganizationRole
