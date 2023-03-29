from pydantic import BaseModel

class Organization(BaseModel):
    """
    Model to represent an `Organization` object
    
    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database
    """
    
    id: int
    name: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str
    events: list['Event'] # Stores the list of events that the Organization has (generated from relationship with "event" table)

from backend.models.event import Event

Organization.update_forward_refs()