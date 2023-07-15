from pydantic import BaseModel

class OrgRole(BaseModel):
    """
    Model to represent `Role` connections between users and organizations
    
    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database
    """
    
    id: int | None=None
    user_id: int
    org_id: int
    membership_type: int
    
class OrgRoleDetail(OrgRole):
    """
    Model to represent `Role` connections between users and organizations
    
    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database
    """
    
    organization: 'Organization' = None
    user: 'UserSummary' = None

from backend.models.organization import Organization
from backend.models.user import UserSummary;
OrgRoleDetail.update_forward_refs()

