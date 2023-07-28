from .permission import Permission
from .event import Event
from .registration import Registration
from .organization import Organization
from .org_role import OrgRole
from .user import User


class UserPermissions(User):
    """UserPermissions adds Permissions to the User model."""

    permissions: list["Permission"] = []


class UserDetails(UserPermissions):
    """UserDetails extends User model to include relations."""

    events: list[Event] = []
    event_associations: list[Registration] = []
    organizations: list[Organization] = []
    organization_associations: list[OrgRole] = []
