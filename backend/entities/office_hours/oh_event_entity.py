"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour Sections."""

from datetime import datetime, date
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.office_hours.oh_type import OfficeHoursType


from ..entity_base import EntityBase
from typing import Self
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
    type: Mapped[OfficeHoursType] = mapped_column(
        SQLAlchemyEnum(OfficeHoursType), nullable=False
    )
    # Name of event
    title: Mapped[str] = mapped_column(String, nullable=False)
    # Description of event
    description: Mapped[str] = mapped_column(String, nullable=True)
    # Description of the location; allows for instructors to write note about attending office hours
    location_description: Mapped[str] = mapped_column(String, nullable=True)
    # Date of the event
    event_date: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore
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
    location_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=False)
    location: Mapped["RoomEntity"] = relationship("RoomEntity")

    # NOTE: One-to-many relationship of OfficeHoursEvent to tickets
    tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(
        back_populates="event", cascade="all, delete"
    )
