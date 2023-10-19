from backend.models.event import Event
from backend.models.organization import Organization

class NewEvent(Event):
    """
    Pydantic model to represent an `Organization`, including the ID of
    its related organization. This model primarily exists for requests
    to create new events, since only the organization ID would exist and
    not the organization itself (the organization would not be back-populated
    until after the entity as been committed to the database).

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """
    
    organization_id: int

    
class EventDetails(NewEvent):
    """
    Pydantic model to represent an `Event`, including back-populated
    relationship fields.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """
    
    organization: Organization | None = None