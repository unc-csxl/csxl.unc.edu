from pydantic import BaseModel
from articles import ArticleOverview
from .public_user import PublicUser
from .coworking import OperatingHours
from .event import EventOverview

__authors__ = ["Will Zahrt"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SignageOverviewSlow(BaseModel):
    """Encapsulates data for the tv."""

    latest_news: list[ArticleOverview]
    operating_hours: list[OperatingHours]
    registered_events: list[EventOverview]
    announcement: ArticleOverview | None



class SignageOverviewFast(BaseModel):
    """Encapsulates data for the tv."""

    latest_news: list[ArticleOverview]
    operating_hours: list[OperatingHours]
    registered_events: list[EventOverview]
    seat_availability: Sequence[SeatAvailability]
