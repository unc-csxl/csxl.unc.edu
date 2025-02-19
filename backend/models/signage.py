from pydantic import BaseModel
from .articles import ArticleOverview
from .public_user import PublicUser
from .coworking import SeatAvailability
from .event import EventOverview
from typing import Sequence

__authors__ = ["Will Zahrt", "Andrew Lockard", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SignageOfficeHours(BaseModel):
    """Stores necessary info for displaying the office hours signage widget"""

    id: int
    mode: str
    course: str
    location: str
    queued: int


class SignageAnnouncement(BaseModel):
    """Stores all fields sent as announcment data"""

    title: str


class SignageOverviewSlow(BaseModel):
    """Encapsulates less frequent data for the tv."""

    newest_news: list[ArticleOverview]
    events: list[EventOverview]
    top_users: list[PublicUser]
    announcements: list[SignageAnnouncement]


class SignageOverviewFast(BaseModel):
    """Encapsulates frequent data for the tv."""

    active_office_hours: list[SignageOfficeHours]
    available_rooms: list[str]
    seat_availability: Sequence[SeatAvailability]
