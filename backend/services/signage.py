"""
Service to collect and organize the information for CSXL Signage
"""

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..database import db_session

from datetime import datetime, timedelta
from ..models.coworking import TimeRange

from ..models.signage import SignageOverviewFast, SignageOverviewSlow
from ..services.coworking import ReservationService, SeatService
from ..services import RoomService

from ..entities import ArticleEntity, RoomEntity, UserEntity
from ..entities.coworking import ReservationEntity
from ..entities.office_hours import OfficeHoursEntity
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
        # TODO: Office Hours
        now = datetime.now
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
            .order_by(RoomEntity.nickname.desc())
        )
        room_entities = self._session.scalars(room_query).all()
        available_rooms = [room.to_overview_model() for room in room_entities]

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
            active_office_hour=active_office_hours,
            available_rooms=available_rooms,
            seat_availability=seat_availability,
        )

    def get_slow_data(self) -> SignageOverviewSlow:
        # TODO: Newest News

        # TODO: Checkin Leaderboard
        top_users_query = (
            self._session.query(
                UserEntity, func.count(ReservationEntity.id).label("reservation_count")
            )
            .join(ReservationEntity)
            .group_by(UserEntity.id)
            .order_by(func.count(ReservationEntity.id).desc())
            .limit(10)
        )

        user_entities = self._session.scalars(top_users_query).all()
        top_users = [user.to_overview_model() for user in user_entities]

        # TODO: Newest Events

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

        return SignageOverviewSlow(top_users=top_users, announcements=announcements)
