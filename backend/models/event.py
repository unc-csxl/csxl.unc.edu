from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    """
    Model to represent `Event` connections between users and organizations
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """
    
    id: int
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    org_id: int
    organization: 'Organization' # Stores the organization hosting the event (generated from relationship with "organization" table)

from backend.models.organization import Organization
Event.update_forward_refs()