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
    event: 'EventSummary' = None
    user: 'UserSummary' = None


from backend.models.event import EventSummary;
from backend.models.user import UserSummary;
OrgRole.update_forward_refs()

