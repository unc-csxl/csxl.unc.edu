from pydantic import BaseModel
from articles import ArticleOverview
from .public_user import PublicUser
from .coworking import OperatingHours, SeatAvailability
from .event import EventOverview
from typing import Sequence
from .room_details import RoomDetails

__authors__ = ["Will Zahrt", "Andrew Lockard", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SignageOverviewSlow(BaseModel):
    """Encapsulates data for the tv."""

    latest_news: list[ArticleOverview]
    # TODO: Need a list of the top ten checkins.
    registered_events: list[EventOverview]
    announcements: list[str] | None


class SignageOverviewFast(BaseModel):
    """Encapsulates data for the tv."""

    # TODO: office_hours: list[ArticleOverview]
    available_rooms: list[str]
    seat_availability: Sequence[SeatAvailability]
