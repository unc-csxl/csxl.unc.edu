from pydantic import BaseModel

class Organization(BaseModel):
    """
    Model to represent an `Organization` object
    
    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database
    """
    
    id: int | None=None
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
    events: list['Event'] = [] # Stores the list of events that the Organization has (generated from relationship with "event" table)
    users: list['UserSummary'] = []
    user_associations: list['OrgRole'] = []

class OrganizationSummary(BaseModel):
    """
    Model to represent an `Organization` object in a relationship

    This model is based on the `Organization` model, which defines the shape
    of the `Organization` database in the PostgreSQL database

    This model exists to prevent infinite recursion with bidirectional
    relationship mapping.
    """

    id: int | None=None
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

from backend.models.event import Event
from backend.models.user import UserSummary
from backend.models.org_role import OrgRole

Organization.update_forward_refs()