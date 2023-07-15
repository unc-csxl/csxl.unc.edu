from pydantic import BaseModel

class OrganizationDetail(BaseModel):
    """
    Model to represent an `OrganizationDetail` object
    
    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `OrganizationDetail` database in the PostgreSQL database
    """
    
    id: int | None=None
    name: str
    slug: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str
    events: list['EventDetail'] = [] # Stores the list of events that the OrganizationDetail has (generated from relationship with "event" table)
    users: list['UserSummary'] = []
    user_associations: list['OrgRoleDetail'] = []

class Organization(BaseModel):
    """
    Model to represent an `OrganizationDetail` object in a relationship

    This model is based on the `OrganizationDetail` model, which defines the shape
    of the `OrganizationDetail` database in the PostgreSQL database

    This model exists to prevent infinite recursion with bidirectional
    relationship mapping.
    """

    id: int | None=None
    name: str
    slug: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str

from backend.models.event import EventDetail
from backend.models.user import UserSummary
from backend.models.org_role import OrgRoleDetail

OrganizationDetail.update_forward_refs()
Organization.update_forward_refs()