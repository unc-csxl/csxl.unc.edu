"""Definition of SQLAlchemy table-backed object mapping entity for Course Sections."""

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionEntnity(EntityBase):
    """Serves as the database model schema defining the shape of the `Section` table"""

    # Name for the course section table in the PostgreSQL database
    __tablename__ = "section"

    # Section properties (columns in the database table)

    # Unique ID for the section
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Code of the section (for example, COMP 100-003's code would be "003")
    code: Mapped[str] = mapped_column(String, default="")
    # Starting date for the term
    start_date: Mapped[datetime] = mapped_column(DateTime)
    # Ending date for the term
    end_date: Mapped[datetime] = mapped_column(DateTime)

    # Course the section is for
    # NOTE: This defines a one-to-many relationship between the course and sections tables.
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["CourseEntity"] = relationship(back_populates="sections")

    # Term the section is in
    # NOTE: This defines a one-to-many relationship between the term and sections tables.
    term_id: Mapped[int] = mapped_column(ForeignKey("term.id"))
    term: Mapped["TermEntity"] = relationship(back_populates="course_sections")
