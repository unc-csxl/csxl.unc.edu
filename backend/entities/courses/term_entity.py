"""Definition of SQLAlchemy table-backed object mapping entity for Terms."""

from typing import Self
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from datetime import datetime
from ...models.courses.term import Term
from ...models.courses.term_details import TermDetails

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TermEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Term` table"""

    # Name for the term table in the PostgreSQL database
    __tablename__ = "courses__term"

    # Term properties (columns in the database table)

    # Unique ID for the term
    # Format: <S|F|M|SuI|SuII<##>
    # For example, F23
    id: Mapped[str] = mapped_column(String(6), primary_key=True)

    # Name of the term (for example, "Fall 2023")
    name: Mapped[str] = mapped_column(String, default="")
    # Starting date for the term
    start: Mapped[datetime] = mapped_column(DateTime)
    # Ending date for the term
    end: Mapped[datetime] = mapped_column(DateTime)

    # NOTE: This field establishes a one-to-many relationship between the term and section tables.
    course_sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="term", cascade="all,delete"
    )

    @classmethod
    def from_model(cls, model: Term) -> Self:
        """
        Class method that converts a `Term` model into a `TermEntity`

        Parameters:
            - model (Term): Model to convert into an entity
        Returns:
            TermEntity: Entity created from model
        """
        return cls(id=model.id, name=model.name, start=model.start, end=model.end)

    def to_model(self) -> Term:
        """
        Converts a `TermEntity` object into a `Term` model object

        Returns:
            Term: `Term` object from the entity
        """
        return Term(id=self.id, name=self.name, start=self.start, end=self.end)

    def to_details_model(self) -> TermDetails:
        """
        Converts a `TermEntity` object into a `TermDetails` model object

        Returns:
            TermDetails: `TermDetails` object from the entity
        """
        return TermDetails(
            id=self.id,
            name=self.name,
            start=self.start,
            end=self.end,
            course_sections=[section.to_model() for section in self.course_sections],
        )
