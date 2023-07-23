from .event import Event
from .organization import Organization
from .user import User
from .registration import Registration

class EventDetail(Event):
    """
    Model to represent `EventDetail` connections between users and organizations
    
    This model is based on the `EventEntity` model, which defines the shape
    of the `EventDetail` database in the PostgreSQL database
    """
    
    organization: Organization # Stores the organization hosting the event (generated from relationship with "organization" table)

    users: list[User] = []
    user_associations: list[Registration] = []