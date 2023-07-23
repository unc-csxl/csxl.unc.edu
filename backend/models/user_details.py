from .permission import Permission
from .event import Event
from .registration import Registration
from .organization import Organization
from .org_role import OrgRole
from .user import User

class UserDetails(User):
    """UserDetails extends User model to include relations."""
    permissions: list['Permission'] = []
    events: list[Event] = []
    event_associations: list[Registration] = []
    organizations: list[Organization] = []
    organization_associations: list[OrgRole] = []

