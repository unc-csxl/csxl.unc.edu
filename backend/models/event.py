from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    """
    Model to represent `Event` connections between users and organizations
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """
    
    id: int | None=None
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    org_id: int
    organization: 'OrganizationSummary' # Stores the organization hosting the event (generated from relationship with "organization" table)

    users: list['UserSummary'] = []
    user_associations: list['Registration'] = []

class EventSummary(BaseModel):
    """
    Model to represent an `Event` object in a relationship

    This model is based on the `Event` model, which defines the shape
    of the `Event` database in the PostgreSQL database

    This model exists to prevent infinite recursion with bidirectional
    relationship mapping.
    """

    id: int | None=None
    name: str
    time: datetime
    location: str
    description: str
    public: bool
    org_id: int
    organization: 'OrganizationSummary' # Stores the organization hosting the event (generated from relationship with "organization" table)

from backend.models.organization import OrganizationSummary
from backend.models.registration import Registration;
from backend.models.user import UserSummary;

Event.update_forward_refs()
EventSummary.update_forward_refs()
