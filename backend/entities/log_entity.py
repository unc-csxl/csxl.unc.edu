"""Definition of SQLAlchemy table-backed object mapping entity for Audit Log listings."""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.log import Log, LogDetails

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class LogEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `log` table"""

    # Name for the log table in the PostgreSQL database
    __tablename__ = "log"

    # Log properties (columns in the database table)

    # Unique ID for the log
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Description of action taken
    description: Mapped[str] = mapped_column(String)

    # User for the log
    # NOTE: This defines a one-to-many relationship between the user and log tables.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="logs")

    @classmethod
    def from_model(cls, model: Log) -> Self:
        """
        Class method that converts a `Log` model into a `LogEntity`

        Parameters:
            - model (Log): Model to convert into an entity
        Returns:
            LogEntity: Entity created from model
        """
        return cls(id=model.id, description=model.description, user_id=model.user_id)

    def to_detail_model(self) -> LogDetails:
        """
        Converts a `LogEntity` object into a `Log` model object

        Returns:
            Log: `Log` object from the entity
        """
        return LogDetails(
            id=self.id,
            description=self.description,
            user_id=self.user_id,
            user=self.user,
        )
