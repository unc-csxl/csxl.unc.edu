from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    """
    Model to represent an `EventDetail` object in a relationship

    This model is based on the `EventDetail` model, which defines the shape
    of the `EventDetail` database in the PostgreSQL database

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
    
class EventDetail(Event):
    """
    Model to represent `EventDetail` connections between users and organizations
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `EventDetail` database in the PostgreSQL database
    """
    
    organization: 'Organization' # Stores the organization hosting the event (generated from relationship with "organization" table)

    users: list['UserSummary'] = []
    user_associations: list['RegistrationDetail'] = []

from backend.models.organization import Organization
from backend.models.registration import RegistrationDetail;
from backend.models.user import UserSummary;

EventDetail.update_forward_refs()
Event.update_forward_refs()
