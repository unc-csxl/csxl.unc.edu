from backend.models.event import Event
from backend.models.organization import Organization

class NewEvent(Event):
    """
    Model to represent a new `Event` request, containing an organization ID
    to be linked to an organization in the PostgreSQL database
    """
    
    organization_id: int

    
class EventDetails(NewEvent):
    """
    Model to represent `Event` connections between users and organizations
    """
    
    organization: Organization | None = None