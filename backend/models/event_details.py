from backend.models.event import Event
from backend.models.organization import Organization

class EventDetails(Event):
    """
    Model to represent `Event` connections between users and organizations
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """
    
    organization_id: int
    organization: Organization | None = None