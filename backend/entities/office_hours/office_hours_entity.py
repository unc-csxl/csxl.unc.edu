"""Definition of SQLAlchemy table-backed object mapping entity for Office Hours."""

from datetime import datetime
from typing import Self
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.academics.my_courses import OfficeHoursOverview
from backend.models.office_hours.ticket_state import TicketState
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ...models.office_hours.office_hours_details import (
    OfficeHoursDetails,
    PrimaryOfficeHoursDetails,
)

from ...models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)

from ..entity_base import EntityBase
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = [
    "Ajay Gandecha",
    "Madelyn Andrews",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Jade Keegan",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHours` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours"

    # Unique id for OfficeHoursEvent
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Type of event
    type: Mapped[OfficeHoursEventType] = mapped_column(
        SQLAlchemyEnum(OfficeHoursEventType, name="office_hours__event__type"),
        nullable=False,
    )

    # Mode of event
    mode: Mapped[OfficeHoursEventModeType] = mapped_column(
        SQLAlchemyEnum(OfficeHoursEventModeType, name="office_hours__event__mode"),
        nullable=False,
    )

    # Description of event
    description: Mapped[str] = mapped_column(String, default="", nullable=False)
    # Description of the location; allows for instructors to write note about attending office hours
    location_description: Mapped[str] = mapped_column(
        String, default="", nullable=False
    )
    # Time the event starts
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Time the event ends
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # NOTE: Many-to-one relationship of OfficeHoursEvents to OH section
    course_site_id: Mapped[int] = mapped_column(
        ForeignKey("course_site.id"), nullable=False
    )
    course_site: Mapped["CourseSiteEntity"] = relationship(
        back_populates="office_hours"
    )

    # NOTE: Many-to-one relationship of OfficeHoursEvents to OfficeHoursRecurrencePattern
    recurrence_pattern_id: Mapped[int] = mapped_column(
        ForeignKey("office_hours_recurrence_pattern.id"), nullable=True
    )
    recurrence_pattern: Mapped["OfficeHoursRecurrencePatternEntity"] = relationship(
        back_populates="office_hours"
    )

    # NOTE: Unidirectional relationship to Room
    room_id: Mapped[str] = mapped_column(ForeignKey("room.id"), nullable=False)
    room: Mapped["RoomEntity"] = relationship("RoomEntity")

    # NOTE: One-to-many relationship of OfficeHoursEvent to tickets
    tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(
        back_populates="office_hours", cascade="all, delete"
    )

    @classmethod
    def from_new_model(cls, model: NewOfficeHours) -> Self:
        """
        Class method that converts an `NewOfficeHours` model into a `OfficeHoursEntity`

        Parameters:
            - model (NewOfficeHours): Model to convert into an entity
        Returns:
            OfficeHoursEntity: Entity created from model
        """
        return cls(
            type=model.type,
            mode=model.mode,
            description=model.description,
            location_description=model.location_description,
            start_time=model.start_time,
            end_time=model.end_time,
            course_site_id=model.course_site_id,
            room_id=model.room_id,
            recurrence_pattern_id=model.recurrence_pattern_id,
        )

    @classmethod
    def from_model(cls, model: OfficeHours) -> Self:
        """
        Class method that converts an `OfficeHours` model into a `OfficeHoursEntity`

        Parameters:
            - model (OfficeHours): Model to convert into an entity
        Returns:
            OfficeHoursEntity: Entity created from model
        """
        return cls(
            id=model.id,
            type=model.type,
            mode=model.mode,
            description=model.description,
            location_description=model.location_description,
            start_time=model.start_time,
            end_time=model.end_time,
            course_site_id=model.course_site_id,
            room_id=model.room_id,
        )

    def to_model(self) -> OfficeHours:
        """
        Converts a `OfficeHoursEntity` object into a `OfficeHours` model object

        Returns:
            OfficeHours: `OfficeHours` object from the entity
        """
        return OfficeHours(
            id=self.id,
            type=self.type,
            mode=self.mode,
            description=self.description,
            location_description=self.location_description,
            start_time=self.start_time,
            end_time=self.end_time,
            course_site_id=self.course_site_id,
            room_id=self.room_id,
            recurrence_pattern_id=self.recurrence_pattern_id,
        )

    def to_primary_details_model(self) -> PrimaryOfficeHoursDetails:
        """
        Converts a `OfficeHoursEntity` object into a `PrimaryOfficeHoursDetails` model object

        Returns:
            OfficeHours: `OfficeHours` object from the entity
        """
        return PrimaryOfficeHoursDetails(
            id=self.id,
            type=self.type,
            mode=self.mode,
            description=self.description,
            location_description=self.location_description,
            start_time=self.start_time,
            end_time=self.end_time,
            course_site_id=self.course_site_id,
            room_id=self.room_id,
            recurrence_pattern_id=self.recurrence_pattern_id,
            recurrence_pattern=(
                self.recurrence_pattern.to_model() if self.recurrence_pattern else None
            ),
        )

    def to_details_model(self) -> OfficeHoursDetails:
        """
        Converts a `OfficeHoursEntity` object into a `OfficeHoursDetails` model object

        Returns:
            OfficeHoursDetails: `OfficeHoursDetails` object from the entity
        """
        return OfficeHoursDetails(
            id=self.id,
            type=self.type,
            mode=self.mode,
            description=self.description,
            location_description=self.location_description,
            start_time=self.start_time,
            end_time=self.end_time,
            course_site_id=self.course_site_id,
            room_id=self.room_id,
            course_site=self.course_site.to_model(),
            recurrence_pattern_id=self.recurrence_pattern_id,
            recurrence_pattern=self.recurrence_pattern.to_model(),
            room=self.room.to_model(),
            tickets=[ticket.to_model() for ticket in self.tickets],
        )
