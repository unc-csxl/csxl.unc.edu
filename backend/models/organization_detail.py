from .organization import Organization
from .event import Event
from .user import User
from .org_role import OrgRole

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class OrganizationDetail(Organization):
    """Represent a Role, but also include its events, members (users), and organization roles (user_associations)."""
    
    # Stores the list of events that the OrganizationDetail has (generated from relationship with "event" table)
    events: list[Event] = []
    users: list[User] = []
    user_associations: list[OrgRole] = []