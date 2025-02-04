from typing import Self, TYPE_CHECKING

from ...models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
    OfficeHoursRecurrencePattern,
)
from ..entity_base import EntityBase
from .office_hours_entity import OfficeHoursEntity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, Integer, Boolean
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .office_hours_entity import OfficeHoursEntity


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursRecurrencePattern(SQLModel, table=True):
    """Serves as the database model schema defining the shape of the `OfficeHoursRecurrencePattern` table"""

    # Name for the recurrence table in the PostgreSQL database
    __tablename__ = "office_hours_recurrence_pattern"

    # Unique id for OfficeHoursRecurrence
    id: int | None = Field(default=None, primary_key=True)

    # Date recurrence starts
    start_date: date

    # Date recurrence ends
    end_date: date

    # Days of the week the event should recur on
    recur_monday: bool = False
    recur_tuesday: bool = False
    recur_wednesday: bool = False
    recur_thursday: bool = False
    recur_friday: bool = False
    recur_saturday: bool = False
    recur_sunday: bool = False

    office_hours: list["OfficeHoursEntity"] = Relationship(
        back_populates="recurrence_pattern"
    )


class OfficeHoursRecurrencePatternEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursRecurrencePattern` table"""

    # Name for the recurrence table in the PostgreSQL database
    __tablename__ = "office_hours_recurrence_pattern"

    # Unique id for OfficeHoursRecurrence
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Date recurrence starts
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Date recurrence ends
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Days of the week the event should recur on
    recur_monday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recur_tuesday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recur_wednesday: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    recur_thursday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recur_friday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recur_saturday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recur_sunday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # NOTE: One-to-many relationship of OfficeHoursRecurrence to OfficeHoursEvent
    office_hours: Mapped[list["OfficeHoursEntity"]] = relationship(
        back_populates="recurrence_pattern", cascade="all, delete"
    )

    @classmethod
    def from_new_model(cls, model: NewOfficeHoursRecurrencePattern) -> Self:
        """
        Class method that converts a `NewOfficeHoursRecurrencePattern` model into a
        `OfficeHoursRecurrencePatternEntity`

        Parameters:
            - model (NewOfficeHoursRecurrencePattern): Model to convert into an entity
        Returns:
            OfficeHoursRecurrencePatternEntity: Entity created from model
        """
        return cls(
            start_date=model.start_date,
            end_date=model.end_date,
            recur_monday=model.recur_monday,
            recur_tuesday=model.recur_tuesday,
            recur_wednesday=model.recur_wednesday,
            recur_thursday=model.recur_thursday,
            recur_friday=model.recur_friday,
            recur_saturday=model.recur_saturday,
            recur_sunday=model.recur_sunday,
        )

    @classmethod
    def from_model(cls, model: OfficeHoursRecurrencePattern) -> Self:
        """
        Class method that converts a `OfficeHoursRecurrencePattern` model into a
        `OfficeHoursRecurrencePatternEntity`

        Parameters:
            - model (OfficeHoursRecurrencePattern): Model to convert into an entity
        Returns:
            OfficeHoursRecurrencePatternEntity: Entity created from model
        """
        return cls(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            recur_monday=model.recur_monday,
            recur_tuesday=model.recur_tuesday,
            recur_wednesday=model.recur_wednesday,
            recur_thursday=model.recur_thursday,
            recur_friday=model.recur_friday,
            recur_saturday=model.recur_saturday,
            recur_sunday=model.recur_sunday,
        )

    def to_model(self) -> OfficeHoursRecurrencePattern:
        """
        Converts an `OfficeHoursRecurrencePatternEntity` object into an
        `OfficeHoursRecurrencePattern` model object

        Returns
          OfficeHoursRecurrencePattern: `OfficeHoursRecurrencePattern` object from the entity
        """
        return OfficeHoursRecurrencePattern(
            id=self.id,
            start_date=self.start_date,
            end_date=self.end_date,
            recur_monday=self.recur_monday,
            recur_tuesday=self.recur_tuesday,
            recur_wednesday=self.recur_wednesday,
            recur_thursday=self.recur_thursday,
            recur_friday=self.recur_friday,
            recur_saturday=self.recur_saturday,
            recur_sunday=self.recur_sunday,
        )
