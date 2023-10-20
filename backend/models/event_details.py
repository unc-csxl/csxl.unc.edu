from backend.models.event import Event
from backend.models.organization import Organization
    
class EventDetails(Event):
    """
    Model to represent `Event` connections between users and organizations
    """
    
    organization: Organization | None = None