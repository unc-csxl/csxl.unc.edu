"""Definition of SQLAlchemy table-backed object mapping entity for Course."""

from typing import Self
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from ...models.courses import Course
from ...models.courses import CourseDetails

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
    # Credit hours for a course (-1 = variable / not set)
    credit_hours: Mapped[int] = mapped_column(Integer, default=-1)

    # NOTE: This field establishes a one-to-many relationship between the course and section tables.
    sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="course", cascade="all,delete"
    )

    @classmethod
    def from_model(cls, model: Course) -> Self:
        """
        Class method that converts a `Course` model into a `CourseEntity`

        Parameters:
            - model (Course): Model to convert into an entity
        Returns:
            CourseEntity: Entity created from model
        """
        return cls(
            id=model.id,
            subject_code=model.subject_code,
            number=model.number,
            title=model.title,
            description=model.description,
            credit_hours=model.credit_hours,
        )

    def to_model(self) -> Course:
        """
        Converts a `CourseEntity` object into a `Course` model object

        Returns:
            Course: `Course` object from the entity
        """
        return Course(
            id=self.id,
            subject_code=self.subject_code,
            number=self.number,
            title=self.title,
            description=self.description,
            credit_hours=self.credit_hours,
        )

    def to_details_model(self) -> CourseDetails:
        """
        Converts a `CourseEntity` object into a `CourseDetails` model object

        Returns:
            CourseDetails: `CourseDetails` object from the entity
        """
        return CourseDetails(
            id=self.id,
            subject_code=self.subject_code,
            number=self.number,
            title=self.title,
            description=self.description,
            credit_hours=self.credit_hours,
            sections=[section.to_model() for section in self.sections],
        )
