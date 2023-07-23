from pydantic import BaseModel
from .user import User
from .organization import Organization

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
    
    organization: Organization = None
    user: User | None = None
