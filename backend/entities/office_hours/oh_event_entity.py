"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour Sections."""

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.office_hours.oh_type import OfficeHoursType


from ..entity_base import EntityBase
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = ["Madelyn Andrews"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OfficeHoursEventEntity(EntityBase):
    #TODO: write description
    """Serves as the database model schema defining the shape of the `OfficeHoursEvent` table


    """

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours__event"

    #TODO: add comments
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[OfficeHoursType] = mapped_column(SQLAlchemyEnum(OfficeHoursType), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    location_description: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime,nullable=False)

    office_hours_section_id: Mapped[int] = mapped_column(ForeignKey("office_hours__section.id"), nullable=False)
    office_hours_section: Mapped["OfficeHoursSectionEntity"] = relationship(back_populates="events")

    # Unidirectional relationship to Room
    location_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=False)
    location: Mapped["RoomEntity"] = relationship("RoomEntity")

    # Tickets that have been created during the event
    tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(back_populates="event", cascade="all, delete")