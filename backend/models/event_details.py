from backend.models import event
from backend.models.organization import Organization

class EventDetails(event):
    """
    Model to represent `Event` connections between users and organizations
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """
    
    organization_id: int
    organization: Organization