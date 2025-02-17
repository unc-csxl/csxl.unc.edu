from pydantic import BaseModel
from . import User
from .academics import Term

__authors__ = ["Alanna Zhang, Alexander Feng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OrganizationMembership(BaseModel):
    """Pydantic model to represent an organization member in the roster."""

    id: int | None = None
    user: User
    organization_id: int
    organization_name: str
    organization_slug: str
    title: str = "Member"
    is_admin: bool = False
    term: Term | None = None
