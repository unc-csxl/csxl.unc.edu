"""
The Article Service allows the API to manipulate article data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import db_session
from .exceptions import ResourceNotFoundException

from ..services.coworking import PolicyService, OperatingHoursService

from ..entities import ArticleEntity, UserEntity
from ..entities.coworking import ReservationEntity, reservation_user_table

from ..models import User
from ..models.articles import WelcomeOverview, ArticleState
from ..models.coworking import TimeRange

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ArticleService:
    """Service that performs all of the actions on the `article` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        policies_svc: PolicyService = Depends(),
        operating_hours_svc: OperatingHoursService = Depends(),
    ):
        """Initializes the session"""
        self._session = session
        self._policies_svc = policies_svc
        self._operating_hours_svc = operating_hours_svc

    def get_welcome_overview(self, subject: User) -> WelcomeOverview:
        """Retrieves the welcome overview."""
        # First, retrieve the latest announcement.
        announcement_query = (
            select(ArticleEntity)
            .where(ArticleEntity.is_announcement)
            .where(ArticleEntity.state == ArticleState.PUBLISHED)
            .order_by(ArticleEntity.published.desc())
        )
        announcement_entity = self._session.scalars(announcement_query).all()
        announcement = (
            announcement_entity[0].to_overview_model()
            if len(announcement_entity) > 0
            else None
        )

        # Next, retrieve the latest news.
        # For now, this will load a maximum of 10 articles.
        news_query = (
            select(ArticleEntity)
            .where(ArticleEntity.state == ArticleState.PUBLISHED)
            .order_by(ArticleEntity.published.desc())
            .limit(10)
        )
        news_entities = self._session.scalars(news_query).all()
        news = [article.to_overview_model() for article in news_entities]

        # Load operating hours
        now = datetime.now()
        operating_hours = self._operating_hours_svc.schedule(
            TimeRange(
                start=now, end=now + self._policies_svc.reservation_window(subject)
            )
        )

        # Finally, load future reservations for a given user.
        # For now, this will load a maximum of 3 future reservations.
        future_reservations_query = (
            select(ReservationEntity)
            .join(ReservationEntity.users)
            .where(UserEntity.id == subject.id)
        )
        future_reservations_entities = self._session.scalars(
            future_reservations_query
        ).all()
        future_reservations = [
            reservation.to_overview_model()
            for reservation in future_reservations_entities
        ]

        # Construct the welcome overview and return
        return WelcomeOverview(
            announcement=announcement,
            latest_news=news,
            operating_hours=operating_hours,
            upcoming_reservations=future_reservations,
        )
