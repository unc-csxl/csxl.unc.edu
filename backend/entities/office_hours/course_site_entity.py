"""Definition of SQLAlchemy table-backed object mapping entity for Course Sites."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...models.office_hours.course_site import CourseSite
from ...models.office_hours.course_site_details import CourseSiteDetails


from ..entity_base import EntityBase
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = [
    "Ajay Gandecha",
    "Madelyn Andrews",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class CourseSiteEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `CourseSite` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "course_site"

    # Unique id for OfficeHoursSections
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Title of OH section
    title: Mapped[str] = mapped_column(String, nullable=False)

    # Term the section is in
    # NOTE: This defines a one-to-many relationship between the term and the course site tables.
    term_id: Mapped[str] = mapped_column(ForeignKey("academics__term.id"))
    term: Mapped["TermEntity"] = relationship(back_populates="course_sites")

    # NOTE: One-to-many relationship of OfficeHoursSection to academic sections
    sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="course_site", cascade="all, delete"
    )

    # NOTE: One-to-many relationship of OfficeHoursSection to events
    office_hours: Mapped[list["OfficeHoursEntity"]] = relationship(
        back_populates="course_site", cascade="all, delete"
    )

    @classmethod
    def from_model(cls, model: CourseSite) -> Self:
        """
        Class method that converts an `CourseSite` model into a `CourseSiteEntity`

        Parameters:
            - model (CourseSite): Model to convert into an entity
        Returns:
            CourseSiteEntity: Entity created from model
        """
        return cls(id=model.id, title=model.title, term_id=model.term_id)

    def to_model(self) -> CourseSite:
        """
        Converts a `CourseSiteEntity` object into a `CourseSite` model object

        Returns:
            CourseSite: `CourseSite` object from the entity
        """
        return CourseSite(id=self.id, title=self.title, term_id=self.term_id)

    def to_details_model(self) -> CourseSiteDetails:
        """
        Converts a `CourseSiteEntity` object into a `CourseSiteDetails` model object

        Returns:
            CourseSiteDetails: `CourseSiteDetails` object from the entity
        """
        return CourseSiteDetails(
            id=self.id,
            title=self.title,
            term_id=self.term_id,
            sections=[section.to_model() for section in self.sections],
            events=[event.to_model() for event in self.events],
        )
