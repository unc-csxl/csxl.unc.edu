from .organization import Organization
from .event import Event
from .user import User
from .org_role import OrgRole

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class OrganizationDetail(Organization):
    """
    Model to represent an `OrganizationDetail` object
    
    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `OrganizationDetail` database in the PostgreSQL database
    """
    events: list[Event] = [] # Stores the list of events that the OrganizationDetail has (generated from relationship with "event" table)
    users: list[User] = []
    user_associations: list[OrgRole] = []