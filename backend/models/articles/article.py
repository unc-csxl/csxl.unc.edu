from pydantic import BaseModel
from datetime import datetime
from . import ArticleState
from ..public_user import PublicUser
from ..coworking import OperatingHours, ReservationOverview
from ..event import EventOverview

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ArticleDraft(BaseModel):
    """Data for an article draft (for creation and editing)."""

    id: int | None = None
    slug: str
    state: ArticleState
    title: str
    image_url: str
    synopsis: str
    body: str
    published: datetime
    last_modified: datetime | None
    is_announcement: bool
    organization_slug: str | None
    authors: list[PublicUser]


class ArticleOverview(BaseModel):
    """Data for an article."""

    id: int
    slug: str
    state: ArticleState
    title: str
    image_url: str
    synopsis: str
    body: str
    published: datetime
    last_modified: datetime | None
    is_announcement: bool
    organization_slug: str | None
    organization_logo: str | None
    organization_name: str | None
    authors: list[PublicUser]


class WelcomeOverview(BaseModel):
    """Encapsulates data for the welcome page."""

    announcement: ArticleOverview | None
    latest_news: list[ArticleOverview]
    operating_hours: list[OperatingHours]
    upcoming_reservations: list[ReservationOverview]
    registered_events: list[EventOverview]
