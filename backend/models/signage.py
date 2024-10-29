from pydantic import BaseModel
from .articles import ArticleOverview
from .public_user import PublicUser
from .coworking import OperatingHours, SeatAvailability
from .academics.my_courses import OfficeHoursOverview
from .event import EventOverview
from typing import Sequence
from .room_details import RoomDetails

__authors__ = ["Will Zahrt", "Andrew Lockard", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SignageOverviewSlow(BaseModel):
    """Encapsulates less frequent data for the tv."""

    newest_news: list[ArticleOverview]
    events: list[EventOverview]
    top_users: list[PublicUser]
    announcement_titles: list[str] | None


class SignageOverviewFast(BaseModel):
    """Encapsulates frequent data for the tv."""

    active_office_hours: list[OfficeHoursOverview]
    available_rooms: list[str]
    seat_availability: Sequence[SeatAvailability]
