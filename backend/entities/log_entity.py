"""Definition of SQLAlchemy table-backed object mapping entity for Audit Log listings."""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase

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
