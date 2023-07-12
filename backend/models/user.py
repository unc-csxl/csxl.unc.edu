"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class User(BaseModel):
    """A user is a registered user of the application."""
    id: int | None = None
    pid: int
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None
    permissions: list['Permission'] = []
    events: list['Event'] = []
    event_associations: list['RegistrationDetail'] = []
    organizations: list['Organization'] = []
    organization_associations: list['OrgRoleDetail'] = []


class UserSummary(BaseModel):
    id: int | None = None
    pid: int
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    github: str = ""
    github_id: int | None = None
    github_avatar: str | None = None
    permissions: list['Permission'] = []
    events: list['Event'] = []
    event_associations: list['RegistrationDetail'] = []
    organizations: list['Organization'] = []
    organization_associations: list['OrgRoleDetail'] = []

class NewUser(BaseModel):
    """A new user is a user that has not yet been registered."""
    pid: int
    onyen: str
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    pronouns: str = ''
    permissions: list['Permission'] = []


class ProfileForm(BaseModel):
    """A profile form is a form for updating a user's profile."""
    first_name: str
    last_name: str
    email: str
    pronouns: str


# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .permission import Permission
from backend.models.event import Event;
from backend.models.registration import RegistrationDetail;
from backend.models.org_role import OrgRoleDetail;
from backend.models.organization import Organization;

User.update_forward_refs()
NewUser.update_forward_refs()
UserSummary.update_forward_refs()
