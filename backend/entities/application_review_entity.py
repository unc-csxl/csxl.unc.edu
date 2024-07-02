"""Definition of SQLAlchemy table-backed object mapping entity for Application Reviews."""

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.event_details import EventDetails
from .entity_base import EntityBase
from typing import Self
from ..models.event import DraftEvent, Event
from ..models.registration_type import RegistrationType
from ..models.user import User
from sqlalchemy import Enum as SQLAlchemyEnum

from ..models.application_review import ApplicationReviewStatus

from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationReviewEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `ApplicationReview` table"""

    # Name for the review table in the PostgreSQL database
    __tablename__ = "application_review"

    # Properties (columns in the database table)

    # Unique ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Application
    application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
    application: Mapped["ApplicationEntity"] = relationship(back_populates="reviews")
    # Status
    state: Mapped[ApplicationReviewStatus] = mapped_column(
        SQLAlchemyEnum(ApplicationReviewStatus),
        default=ApplicationReviewStatus.NOT_PROCESSED,
        nullable=False,
    )
    # Preference
    preference: Mapped[int] = mapped_column(Integer)
    # Notes
    notes: Mapped[str] = mapped_column(String)
