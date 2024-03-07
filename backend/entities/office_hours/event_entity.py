"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour Sections."""

from datetime import datetime, date
from typing import Self
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.office_hours.event import OfficeHoursEvent
from backend.models.office_hours.event_details import OfficeHoursEventDetails

from backend.models.office_hours.event_type import OfficeHoursEventType


from ..entity_base import EntityBase
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursEvent` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours__event"

    # Unique id for OfficeHoursEvent
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Type of event
    type: Mapped[OfficeHoursEventType] = mapped_column(
        SQLAlchemyEnum(OfficeHoursEventType), nullable=False
    )
    # Description of event
    description: Mapped[str] = mapped_column(String, default="", nullable=False)
    # Description of the location; allows for instructors to write note about attending office hours
    location_description: Mapped[str] = mapped_column(
        String, default="", nullable=False
    )
    # Date of the event
    date: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore
    # Time the event starts
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Time the event ends
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # NOTE: Many-to-one relationship of OfficeHoursEvents to OH section
    office_hours_section_id: Mapped[int] = mapped_column(
        ForeignKey("office_hours__section.id"), nullable=False
    )
    office_hours_section: Mapped["OfficeHoursSectionEntity"] = relationship(
        back_populates="events"
    )

    # NOTE: Unidirectional relationship to Room
    room_id: Mapped[str] = mapped_column(ForeignKey("room.id"), nullable=False)
    room: Mapped["RoomEntity"] = relationship("RoomEntity")

    # NOTE: One-to-many relationship of OfficeHoursEvent to tickets
    tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(
        back_populates="oh_event", cascade="all, delete"
    )

    @classmethod
    def from_model(cls, model: OfficeHoursEvent) -> Self:
        """
        Class method that converts an `OfficeHoursEvent` model into a `OfficeHoursEventEntity`

        Parameters:
            - model (OfficeHoursEvent): Model to convert into an entity
        Returns:
            OfficeHoursEventEntity: Entity created from model
        """
        return cls(
            id=model.id,
            office_hours_section_id=model.office_hours_section_id,
            room_id=model.room_id,
            type=model.type,
            description=model.description,
            location_description=model.location_description,
            date=model.date,
            start_time=model.start_time,
            end_time=model.end_time,
        )

    def to_model(self) -> OfficeHoursEvent:
        """
        Converts a `OfficeHoursEventEntity` object into a `OfficeHoursEvent` model object

        Returns:
            OfficeHoursEvent: `OfficeHoursEvent` object from the entity
        """
        return OfficeHoursEvent(
            id=self.id,
            office_hours_section_id=self.office_hours_section_id,
            room_id=self.room_id,
            type=self.type,
            description=self.description,
            location_description=self.location_description,
            date=self.date,
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def to_details_model(self) -> OfficeHoursEventDetails:
        """
        Converts a `OfficeHoursEventEntity` object into a `OfficeHoursEventDetails` model object

        Returns:
            OfficeHoursEventDetails: `OfficeHoursEventDetails` object from the entity
        """
        return OfficeHoursEventDetails(
            id=self.id,
            office_hours_section_id=self.office_hours_section_id,
            room_id=self.room_id,
            type=self.type,
            description=self.description,
            location_description=self.location_description,
            date=self.date,
            start_time=self.start_time,
            end_time=self.end_time,
            section=self.office_hours_section.to_model(),
            room=self.room.to_model(),
            tickets=[ticket.to_model() for ticket in self.tickets],
        )
