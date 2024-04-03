"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour Sections."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...models.office_hours.section import (
    OfficeHoursSection,
    OfficeHoursSectionDraft,
)
from ...models.office_hours.section_details import OfficeHoursSectionDetails


from ..entity_base import EntityBase
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursSectionEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursSection` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours__section"

    # Unique id for OfficeHoursSections
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Title of OH section
    title: Mapped[str] = mapped_column(String, nullable=False)

    # NOTE: One-to-many relationship of OfficeHoursSection to academic sections
    sections: Mapped[list["SectionEntity"]] = relationship(
        back_populates="office_hours_section", cascade="all, delete"
    )

    # NOTE: One-to-many relationship of OfficeHoursSection to events
    events: Mapped[list["OfficeHoursEventEntity"]] = relationship(
        back_populates="office_hours_section", cascade="all, delete"
    )

    @classmethod
    def from_draft_model(cls, model: OfficeHoursSectionDraft) -> Self:
        return cls(title=model.title)

    @classmethod
    def from_model(cls, model: OfficeHoursSection) -> Self:
        """
        Class method that converts an `OfficeHoursSection` model into a `OfficeHoursSectionEntity`

        Parameters:
            - model (OfficeHoursSection): Model to convert into an entity
        Returns:
            OfficeHoursSectionEntity: Entity created from model
        """
        return cls(id=model.id, title=model.title)

    def to_model(self) -> OfficeHoursSection:
        """
        Converts a `OfficeHoursSectionEntity` object into a `OfficeHoursSection` model object

        Returns:
            OfficeHoursSection: `OfficeHoursSection` object from the entity
        """
        return OfficeHoursSection(id=self.id, title=self.title)

    def to_details_model(self) -> OfficeHoursSectionDetails:
        """
        Converts a `OfficeHoursSectionEntity` object into a `OfficeHoursSectionDetails` model object

        Returns:
            OfficeHoursSectionDetails: `OfficeHoursSectionDetails` object from the entity
        """
        return OfficeHoursSectionDetails(
            id=self.id,
            title=self.title,
            sections=[section.to_model() for section in self.sections],
            events=[event.to_model() for event in self.events],
        )
