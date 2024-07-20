from pydantic import BaseModel
from datetime import datetime
from . import ArticleState
from ..public_user import PublicUser
from ..coworking import OperatingHours, Reservation

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ArticleOverview(BaseModel):
    """Data for an article."""

    id: int
    slug: str
    state: ArticleState
    title: str
    image_url: str
    published: datetime
    last_modified: datetime
    is_announcement: bool
    organization_slug: str | None
    organization_logo: str | None
    organization_name: str | None
    authors: list[PublicUser]


class WelcomeOverview(BaseModel):
    """Encapsulates data for the welcome page."""

    announcement: ArticleOverview | None
    latest_news: list[ArticleOverview]
    operating_hours: OperatingHours
    upcoming_reservations: list[Reservation]
