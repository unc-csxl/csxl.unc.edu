"""
The Article Service allows the API to manipulate article data in the database.
"""

from fastapi import Depends
from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import db_session
from .exceptions import ResourceNotFoundException

from ..services.event import EventService
from ..services.permission import PermissionService
from ..services.coworking import PolicyService, OperatingHoursService

from ..entities import (
    ArticleEntity,
    UserEntity,
    EventEntity,
    EventRegistrationEntity,
    article_author_table,
)
from ..entities.coworking import ReservationEntity, reservation_user_table

from ..models import User
from ..models.articles import (
    WelcomeOverview,
    ArticleState,
    ArticleOverview,
    ArticleDraft,
)
from ..models.coworking import TimeRange
from ..models.pagination import Paginated, PaginationParams

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ArticleService:
    """Service that performs all of the actions on the `article` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
        policies_svc: PolicyService = Depends(),
        operating_hours_svc: OperatingHoursService = Depends(),
    ):
        """Initializes the session"""
        self._session = session
        self._permission_svc = permission_svc
        self._policies_svc = policies_svc
        self._operating_hours_svc = operating_hours_svc

    def get_welcome_overview(self, subject: User | None) -> WelcomeOverview:
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
            .where(ArticleEntity.is_announcement == False)
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

        # Load future reservations for a given user.
        # For now, this will load a maximum of 3 future reservations.
        future_reservations = []
        if subject:
            future_reservations_query = (
                select(ReservationEntity)
                .join(ReservationEntity.users)
                .where(UserEntity.id == subject.id)
                .where(ReservationEntity.start > datetime.now())
            )
            future_reservations_entities = self._session.scalars(
                future_reservations_query
            ).all()
            future_reservations = [
                reservation.to_overview_model()
                for reservation in future_reservations_entities
            ]

        # Finally, load future event registrations.
        registered_events = []
        if subject:
            registered_events_query = (
                select(EventRegistrationEntity)
                .where(EventRegistrationEntity.user_id == subject.id)
                .join(EventEntity)
                .where(EventEntity.start >= now)
                .order_by(EventEntity.start)
            )

            registered_events_entities = self._session.scalars(
                registered_events_query
            ).all()

            registered_events = [
                registration.event.to_overview_model(subject)
                for registration in registered_events_entities
            ]

        # Construct the welcome overview and return
        return WelcomeOverview(
            announcement=announcement,
            latest_news=news,
            operating_hours=operating_hours,
            upcoming_reservations=future_reservations,
            registered_events=registered_events,
        )

    def get_article(self, slug: str) -> ArticleOverview:
        """Access a single article by slug"""
        article_query = select(ArticleEntity).where(ArticleEntity.slug == slug)
        article_entity = self._session.scalars(article_query).one_or_none()
        return article_entity.to_overview_model() if article_entity else None

    def list(
        self, subject: User, pagination_params: PaginationParams
    ) -> Paginated[ArticleOverview]:
        """List Articles.

        The subject must have the 'article.list' permission on the 'article/' resource.

        Args:
            subject: The user performing the action.
            pagination_params: The pagination parameters.

        Returns:
            Paginated[ArticleOverview]: The paginated list of articles.

        Raises:
            PermissionException: If the subject does not have the required permission.
        """
        self._permission_svc.enforce(subject, "article.list", "article/")

        statement = select(ArticleEntity).order_by(ArticleEntity.published.desc())
        length_statement = select(func.count()).select_from(ArticleEntity)
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size
        statement = statement.offset(offset).limit(limit)
        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(
            items=[entity.to_overview_model() for entity in entities],
            length=length,
            params=pagination_params,
        )

    def create_article(self, subject: User, article: ArticleDraft) -> ArticleOverview:
        """Enables the creation of articles."""
        # 1. Enforce permissions
        self._permission_svc.enforce(subject, "article.create", "article/")
        article_entity = ArticleEntity.from_draft(article)

        # 2. Persist article
        self._session.add(article_entity)
        self._session.commit()

        # 3. Persist authors
        for author in article.authors:
            self._session.execute(
                article_author_table.insert().values(
                    {"user_id": author.id, "article_id": article_entity.id}
                )
            )
        self._session.commit()

        # 5. Return
        return article_entity.to_overview_model()

    def edit_article(self, subject: User, article: ArticleDraft) -> ArticleOverview:
        """Enables the editing of articles."""
        # 1. Enforce permissions
        self._permission_svc.enforce(subject, "article.edit", "article/")

        # 2. Ensure that the article exists
        article_entity = self._session.get(ArticleEntity, article.id)
        if article_entity is None:
            raise ResourceNotFoundException(
                f"Found no article with the ID: {article.id}"
            )

        # 3. Edit the article
        article_entity.slug = article.slug
        article_entity.state = article.state
        article_entity.title = article.title
        article_entity.image_url = article.image_url
        article_entity.synopsis = article.synopsis
        article_entity.body = article.body
        article_entity.published = article.published
        article_entity.last_modified = article.last_modified
        article_entity.is_announcement = article.is_announcement
        article_entity.organization_id = article.organization_id

        # 3. Persist article
        self._session.commit()

        # 4. Persist authors
        self._session.execute(
            delete(article_author_table).filter(
                article_author_table.c.article_id == article.id
            )
        )
        self._session.commit()

        for author in article.authors:
            self._session.execute(
                article_author_table.insert().values(
                    {"user_id": author.id, "article_id": article_entity.id}
                )
            )
        self._session.commit()

        # 5. Return
        return article_entity.to_overview_model()

    def delete_article(self, subject: User, article_id: int):
        """Enables the deletion of articles."""
        # 1. Enforce permissions
        self._permission_svc.enforce(subject, "article.delete", "article/")

        # 2. Ensure that the article exists
        article_entity = self._session.get(ArticleEntity, article_id)
        if article_entity is None:
            raise ResourceNotFoundException(
                f"Found no article with the ID: {article_id}"
            )

        # 3. Delete the article
        self._session.delete(article_entity)
        self._session.commit()
