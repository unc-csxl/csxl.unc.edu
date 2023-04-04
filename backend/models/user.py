"""User model serves as the data object for representing registered users across application layers."""

from pydantic import BaseModel


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class User(BaseModel):
    id: int | None = None
    pid: int
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    permissions: list['Permission'] = []
    events: list['EventSummary'] = []
    event_associations: list['Registration'] = []
    organizations: list['OrganizationSummary'] = []
    organization_associations: list['OrgRole'] = []

class UserSummary(BaseModel):
    id: int | None = None
    pid: int
    onyen: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    pronouns: str = ""
    permissions: list['Permission'] = []

class NewUser(BaseModel):
    pid: int
    onyen: str
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    pronouns: str = ''
    permissions: list['Permission'] = []


class ProfileForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    pronouns: str


# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .permission import Permission
from backend.models.event import EventSummary;
from backend.models.registration import Registration;
from backend.models.org_role import OrgRole;
from backend.models.organization import OrganizationSummary;

User.update_forward_refs()
NewUser.update_forward_refs()
UserSummary.update_forward_refs()
