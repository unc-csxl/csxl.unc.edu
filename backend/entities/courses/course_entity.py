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
    __tablename__ = "courses__course"

    # Course properties (columns in the database table)

    # Unique ID for the course
    # Course IDs are serialized in the following format: <SUBJECT><NUM><H?>
    # Examples: COMP110, COMP283H
    id: Mapped[str] = mapped_column(String(9), primary_key=True)
    # Subject for the course (for example, the subject of COMP 110 would be COMP)
    subject_code: Mapped[str] = mapped_column(String(4), default="")
    # Number for the course (for example, the code of COMP 110 would be 110)
    number: Mapped[str] = mapped_column(String(4), default="")
    # Title or name for the course
    title: Mapped[str] = mapped_column(String, default="")
    # Course description for the course
    description: Mapped[str] = mapped_column(String, default="")

    # NOTE: This field establishes a one-to-many relationship between the course and section tables.
    sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="course", cascade="all,delete"
    )
