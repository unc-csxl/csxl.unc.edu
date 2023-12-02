"""Definition of SQLAlchemy table-backed object mapping entity for Course."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class CourseEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Course` table"""

    # Name for the course table in the PostgreSQL database
    __tablename__ = "course"

    # Course properties (columns in the database table)

    # Unique ID for the course
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Suject for the course (for example, the subject of COMP 110 would be COMP)
    subject: Mapped[str] = mapped_column(String, default="")
    # Code for the course (for example, the code of COMP 110 would be 110)
    code: Mapped[str] = mapped_column(String, default="")
    # Title or name for the course
    title: Mapped[str] = mapped_column(String, default="")

    # NOTE: This field establishes a one-to-many relationship between the course and section tables.
    events: Mapped[list["SectionEntity"]] = relationship(
        back_populates="course", cascade="all,delete"
    )
