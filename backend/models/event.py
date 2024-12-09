from pydantic import BaseModel
from datetime import datetime

from .public_user import PublicUser
from .organization_join_type import OrganizationJoinType
from .registration_type import RegistrationType

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class EventDraft(BaseModel):
    """Represents the model used to create new events."""

    # Makes `EventDraft` hashable, enabling it to be used in sets.
    def __hash__(self) -> int:
        return self.id.__hash__()

    id: int | None = None
    name: str
    start: datetime
    end: datetime
    location: str
    description: str
    registration_limit: int
    organization_slug: str
    organizers: list[PublicUser] = []
    image_url: str | None = None
    override_registration_url: str | None = None


class EventOverview(BaseModel):
    id: int
    name: str
    start: datetime
    end: datetime
    location: str
    description: str
    public: bool
    # join_type: OrganizationJoinType
    number_registered: int
    registration_limit: int
    organization_id: int
    organization_slug: str
    organization_icon: str
    organization_name: str
    organizers: list[PublicUser]
    user_registration_type: RegistrationType | None
    image_url: str | None
    override_registration_url: str | None


class EventStatusOverview(BaseModel):
    featured: EventOverview | None
    registered: list[EventOverview]
