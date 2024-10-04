from pydantic import BaseModel
from .articles import ArticleOverview
from .user import User
from .coworking import OperatingHours, SeatAvailability
from .office_hours import OfficeHours
from .event import EventOverview
from typing import Sequence
from .room_details import RoomDetails

__authors__ = ["Will Zahrt", "Andrew Lockard", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SignageOverviewSlow(BaseModel):
    """Encapsulates data for the tv."""

    newest_news: list[ArticleOverview]
    events: list[EventOverview]
    top_users: list[User]  # May want to make this a PublicUser
    announcements: list[str] | None


class SignageOverviewFast(BaseModel):
    """Encapsulates data for the tv."""

    office_hours: list[OfficeHours]
    available_rooms: list[str]
    seat_availability: Sequence[SeatAvailability]
