"""Definition of SQLAlchemy table-backed object mapping entity for Feedback."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.feedback import Feedback
from backend.models.feedback_details import FeedbackDetails
from .entity_base import EntityBase
from typing import Self
from ..models.user import User


__authors__ = ["Matt Vu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class FeedbackEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Feedback` table"""

    # Name for the feedback table in the PostgreSQL database
    __tablename__ = "feedback"

    # Unique ID for the feedback
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # User who submitted the feedback ticket
    user_id = mapped_column(Integer, ForeignKey("user.id"))
    user = relationship("UserEntity")
    # Description of the feedback
    description: Mapped[str] = mapped_column(String)
    # Whether the feedback has been resolved or not
    has_resolved: Mapped[bool] = mapped_column(Boolean)

    @classmethod
    def from_draft_model(cls, model: Feedback) -> Self:
        """
        Class method that converts an `DraftFeedback` model into a `FeedbackEntity`

        Parameters:
            - model (DraftFeedback): Model to convert into an entity
        Returns:
            FeedbackEntity: Entity created from model
        """
        return cls(
            id=model.id,
            user_id=model.user_id,
            user=model.user,
            description=model.description,
            has_resolved=model.has_resolved,
        )

    @classmethod
    def from_model(cls, model: Feedback) -> Self:
        """
        Class method that converts an `Feedback` model into a `FeedbackEntity`

        Parameters:
            - model (Feedback): Model to convert into an entity
        Returns:
            FeedbackEntity: Entity created from model
        """
        return cls(
            id=model.id,
            user_id=model.user_id,
            user=model.user,
            description=model.description,
            has_resolved=model.has_resolved,
        )

    def to_model(self, subject: User | None = None) -> Feedback:
        """
        Converts a `FeedbackEntity` object into a `Feedback` model object

        Returns:
            Feedback: `Feedback` object from the entity
        """
        return Feedback(
            id=self.id,
            user_id=self.user_id,
            user=self.user,
            description=self.description,
            has_resolved=self.has_resolved,
        )

    def to_details_model(self, subject: User | None = None) -> FeedbackDetails:
        """Create a FeedbackDetails model from a FeedbackEntity

        Returns:
            FeedbackDetails: A FeedbackDetails model for API usage.
        """

        feedback = self.to_model(subject)

        return FeedbackDetails(
            id=self.id,
            user_id=self.user_id,
            user=self.user,
            description=self.description,
            has_resolved=self.has_resolved,
        )
