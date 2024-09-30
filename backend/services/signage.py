"""
Service to collect and organize the information for CSXL Signage
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session

from datetime import datetime, timedelta
from ..models.coworking import TimeRange

from ..models.signage import SignageOverviewFast, SignageOverviewSlow
from ..services.coworking import ReservationService, SeatService
from ..services import RoomService

from ..entities import ArticleEntity
from ..models.articles import ArticleState

__authors__ = ["Andrew Lockard", "Will Zahrt", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SignageService:
    """
    Service to collect and organize the information for CSXL Signage
    """

    def __init__(
        self,
        reservation_svc: ReservationService = Depends(),
        session: Session = Depends(db_session),
        seat_svc: SeatService = Depends(),
        room_svc: RoomService = Depends(),
    ):
        self._reservation_svc = reservation_svc
        self._session = session
        self._seat_svc = seat_svc
        self.room_svc = room_svc

    def get_fast_data(self) -> SignageOverviewFast:
        """
        Gets the data for the fast API route
        """
        # Office Hours

        # Rooms
        all_rooms = self.room_svc.all()
        available_rooms = list[str]

        # Putting the names of all the available rooms into a list to return
        for room in all_rooms:
            if room.reservable:
                available_rooms.append(room.room)

        # Seats
        now = datetime.now()
        walkin_window = TimeRange(
            start=now,
            end=now
            + timedelta(
                hours=6, minutes=10
            ),  # Makes sure open seats are available for 2hr walkin reservation
        )
        seats = self._seat_svc.list()  # All Seats are fair game for walkin purposes
        seat_availability = self._reservation_svc.seat_availability(
            seats, walkin_window
        )

        return SignageOverviewFast(
            available_rooms=available_rooms, seat_availability=seat_availability
        )

    def get_slow_data(self) -> SignageOverviewSlow:
        # Newest News

        # Checkin Leaderboard
        # Suggestion: Use a query to make a table with a new column that adds up the number of rows for checkins.

        # Newest Events

        # Announcements
        announcement_query = (
            select(ArticleEntity)
            .where(ArticleEntity.is_announcement)
            .where(ArticleEntity.state == ArticleState.PUBLISHED)
            .order_by(ArticleEntity.published.desc())
            .limit(3)
        )
        announcement_entities = self._session.scalars(announcement_query).all()
        announcements = [
            announcement.to_overview_model() for announcement in announcement_entities
        ]

        return SignageOverviewSlow(announcements=announcements)
