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
