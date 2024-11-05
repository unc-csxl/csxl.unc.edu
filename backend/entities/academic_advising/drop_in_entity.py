"""Definition of SQLAlchemy table-backed object mapping entity for Advising Drop-in Sessions."""

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from datetime import datetime
from ...models.academic_advising import DropIn

__author__ = "Emmalyn Foster"
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class DropInEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Drop-in` table"""

    # Name of the table PostgreSQL database
    __tablename__ = "drop_in"

    # Unique ID for the drop-in
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Title of the drop-in session (whose session this is)
    title: Mapped[str] = mapped_column(String)
    # Start time of the drop-in session
    start: Mapped[datetime] = mapped_column(DateTime)
    # End time of the drop-in session
    end: Mapped[datetime] = mapped_column(DateTime)
    # Link to reroute to individual event in Google Calendar
    link: Mapped[str] = mapped_column(String)

    # Drop-ins added to the user's "My Drop-ins"
    # NOTE: This is part of a many-to-many relationship between drop-ins and users, via the drop-in reminders table.
    drop_in_reminders: Mapped[list["DropInReminderEntity"]] = relationship(
        back_populates="drop_in", cascade="all,delete"
    )

    @classmethod
    def from_model(cls, model: DropIn) -> Self:
        """
        Create a DropInEntity from a DropIn model.

        Args:
            model (DropIn): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """

        return cls(
            id=model.id,
            title=model.title,
            start=model.start,
            end=model.end,
            link=model.link,
        )

    @classmethod
    def to_model(self) -> DropIn:
        return DropIn(
            id=self.id,
            title=self.title,
            start=self.start,
            end=self.end,
            link=self.link,
        )
