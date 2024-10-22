"""
Service to collect and organize the information for CSXL Signage
"""

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.models.coworking.reservation import ReservationState

from ..database import db_session

from datetime import datetime, timedelta
from ..models.coworking import TimeRange

from ..models.signage import SignageOverviewFast, SignageOverviewSlow
from ..services.coworking import ReservationService, SeatService
from ..services import RoomService

from ..entities import ArticleEntity, RoomEntity, UserEntity, EventEntity
from ..entities.coworking import ReservationEntity
from ..entities.office_hours import OfficeHoursEntity
from ..models.articles import ArticleState

__authors__ = ["Andrew Lockard", "Will Zahrt", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

MAX_ARTICLES = 5
MAX_LEADERBOARD_SLOTS = 10
MAX_EVENTS = 5
MAX_ANNOUCEMENTS = 3


# TODO: Create Tests for this Service
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
        now = datetime.now()
        office_hours_query = select(OfficeHoursEntity).filter(
            OfficeHoursEntity.start_time <= now, OfficeHoursEntity.end_time >= now
        )
        active_office_hours_entities = self._session.scalars(office_hours_query).all()
        active_office_hours = [
            office_hours.to_overview_model()
            for office_hours in active_office_hours_entities
        ]

        # Rooms
        room_query = (
            select(RoomEntity)
            .where(RoomEntity.reservable)
            .order_by(RoomEntity.room.desc())
        )
        room_entities = self._session.scalars(room_query).all()
        available_rooms = [room.to_model().id for room in room_entities]

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
            active_office_hours=active_office_hours,
            available_rooms=available_rooms,
            seat_availability=seat_availability,
        )

    def get_slow_data(self) -> SignageOverviewSlow:
        # Newest News
        news_query = (
            select(ArticleEntity)
            .where(ArticleEntity.is_announcement == False)
            .where(ArticleEntity.state == ArticleState.PUBLISHED)
            .order_by(ArticleEntity.published.desc())
            .limit(MAX_ARTICLES)
        )
        news_entities = self._session.scalars(news_query).all()
        newest_news = [news.to_overview_model() for news in news_entities]

        # Checkin Leaderboard
        start_of_month = datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        top_users_query = (
            select(
                UserEntity, func.count(ReservationEntity.id).label("reservation_count")
            )
            .join(ReservationEntity.users)
            .where(ReservationEntity.end >= start_of_month)
            .where(ReservationEntity.state == ReservationState.CHECKED_OUT)
            .group_by(UserEntity.id)
            .order_by(func.count(ReservationEntity.id).desc())
            .limit(MAX_LEADERBOARD_SLOTS)
        )

        user_entities = self._session.scalars(top_users_query).all()
        top_users = [user.to_public_model() for user in user_entities]

        # Newest Events
        events_query = (
            select(EventEntity).order_by(EventEntity.start.desc()).limit(MAX_EVENTS)
        )
        event_entities = self._session.scalars(events_query).all()
        events = [event.to_overview_model() for event in event_entities]

        # Announcements
        announcement_query = (
            select(ArticleEntity)
            .where(ArticleEntity.is_announcement)
            .where(ArticleEntity.state == ArticleState.PUBLISHED)
            .order_by(ArticleEntity.published.desc())
            .limit(MAX_ANNOUCEMENTS)
        )
        announcement_entities = self._session.scalars(announcement_query).all()
        announcement_titles = [
            announcement.to_overview_model().title
            for announcement in announcement_entities
        ]

        return SignageOverviewSlow(
            newest_news=newest_news,
            events=events,
            top_users=top_users,
            announcement_titles=announcement_titles,
        )
