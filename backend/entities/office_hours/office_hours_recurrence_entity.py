from typing import Self

from ...models.office_hours.office_hours_recurrence import NewOfficeHoursRecurrence, OfficeHoursRecurrence
from ..entity_base import EntityBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, Integer, Boolean
from datetime import date

__authors__ = [
    "Jade Keegan"
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

class OfficeHoursRecurrenceEntity(EntityBase):
  """Serves as the database model schema defining the shape of the `OfficeHoursRecurrence` table"""

  # Name for the recurrence table in the PostgreSQL database
  __tablename__ = "office_hours_recurrence"

  # Unique id for OfficeHoursRecurrence
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

  # Date recurrence starts
  start_date: Mapped[date] = mapped_column(Date, nullable=False)
  
  # Date recurrence ends
  end_date: Mapped[date] = mapped_column(Date, nullable=False)

  # Days of the week the event should recur on
  recur_monday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  recur_tuesday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  recur_wednesday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  recur_thursday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  recur_friday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  recur_saturday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  recur_sunday: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

  # NOTE: One-to-many relationship of OfficeHoursRecurrence to OfficeHoursEvent
  events: Mapped[list["OfficeHoursEntity"]] = relationship(
    back_populates="office_hours_recurrence", cascade="all, delete"
    )

  @classmethod
  def from_new_model(cls, model: NewOfficeHoursRecurrence) -> Self:
    """
    Class method that converts a `NewOfficeHoursRecurrence` model into a 
    `OfficeHoursRecurrenceEntity`

    Parameters:
        - model (NewOfficeHoursRecurrence): Model to convert into an entity
    Returns:
        OfficeHoursRecurrenceEntity: Entity created from model
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
  def from_model(cls, model: OfficeHoursRecurrence) -> Self:
    """
    Class method that converts a `OfficeHoursRecurrence` model into a 
    `OfficeHoursRecurrenceEntity`

    Parameters:
        - model (OfficeHoursRecurrence): Model to convert into an entity
    Returns:
        OfficeHoursRecurrenceEntity: Entity created from model
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
  
  def to_model(self) -> OfficeHoursRecurrence:
    """
    Converts an `OfficeHoursRecurrenceEntity` object into an
    `OfficeHoursRecurrence` model object

    Returns
      OfficeHoursRecurrence: `OfficeHoursRecurrence` object from the entity
    """
    return OfficeHoursRecurrence(
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