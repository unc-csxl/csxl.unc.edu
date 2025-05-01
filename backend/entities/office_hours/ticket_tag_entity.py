"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets tags."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...models.office_hours.ticket_tag import (
    OfficeHoursTicketTag,
    NewOfficeHoursTicketTag,
    OfficeHoursTicketTagDetails,
)

from ..entity_base import EntityBase
from typing import Self

__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OfficeHoursTicketTagEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursTicketTag` table"""

    # Name for the ticket tags table in the PostgreSQL database
    __tablename__ = "office_hours__ticket_tag"

    # Unique id for OfficeHoursTicketTag
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Tag name
    name: Mapped[str] = mapped_column(String, nullable=False)

    # NOTE: Many-to-one relationship of OfficeHoursEvents to OH section
    course_site_id: Mapped[int] = mapped_column(
        ForeignKey("course_site.id"), nullable=False
    )
    course_site: Mapped["CourseSiteEntity"] = relationship(
        back_populates="ticket_tags"
    )


    @classmethod
    def from_new_model(cls, model: NewOfficeHoursTicketTag) -> Self:
        """
        Class method that converts an `NewOfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (NewOfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            name=model.name,
            course_site_id=model.course_site_id,
        )

    @classmethod
    def from_model(cls, model: OfficeHoursTicketTag) -> Self:
        """
        Class method that converts an `OfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (OfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
            course_site_id=model.course_site_id,
        )

    def to_model(self) -> OfficeHoursTicketTag:
        """
        Converts a `OfficeHoursTicketTagEntity` object into a `OfficeHoursTicketTag` model object

        Returns:
            OfficeHoursTicketTag: `OfficeHoursTicketTag` object from the entity
        """
        return OfficeHoursTicketTag(
            id=self.id,
            name=self.name,
            course_site_id=self.course_site_id,
        )

    def to_details_model(self) -> OfficeHoursTicketTagDetails:
        return OfficeHoursTicketTagDetails(
            id=self.id,
            name=self.name,
            course_site_id=self.course_site_id,
            course_site=self.course_site.to_model(),
        )