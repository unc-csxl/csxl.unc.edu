"""Definition of SQLAlchemy table-backed object mapping entity for Terms."""

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TermEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Term` table"""

    # Name for the term table in the PostgreSQL database
    __tablename__ = "term"

    # Term properties (columns in the database table)

    # Unique ID for the term
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the term (for example, "Fall 2023")
    name: Mapped[str] = mapped_column(String, default="")
    # Starting date for the term
    start_date: Mapped[datetime] = mapped_column(DateTime)
    # Ending date for the term
    end_date: Mapped[datetime] = mapped_column(DateTime)

    # NOTE: This field establishes a one-to-many relationship between the term and section tables.
    course_sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="term", cascade="all,delete"
    )
