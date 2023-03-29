from pydantic import BaseModel

class OrgRole(BaseModel):
    """
    Model to represent `Role` connections between users and organizations
    
    This model is based on the `RoleEntity` model, which defines the shape
    of the `Role` database in the PostgreSQL database
    """
    
    id: int | None
    user_id: int
    org_id: int
    membership_type: int

