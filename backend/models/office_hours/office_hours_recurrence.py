from datetime import date

from pydantic import BaseModel

__authors__ = [
    "Jade Keegan"
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class NewOfficeHoursRecurrence(BaseModel):
  """
  Pydantic model to represent new office hours recurrence.

  This model is based on the `OfficeHoursRecurrenceEntity` model, which 
  defines the shape of the office hours recurrence table in the 
  PostgreSQL database.
  """

  start_date: date
  end_date: date
  recur_monday: bool
  recur_tuesday: bool
  recur_wednesday: bool
  recur_thursday: bool
  recur_friday: bool
  recur_saturday: bool
  recur_sunday: bool

class OfficeHoursRecurrence(NewOfficeHoursRecurrence):
  """
  Pydantic model to represent office hours recurrence.

  This model is based on the `OfficeHoursRecurrenceEntity` model, which 
  defines the shape of the office hours recurrence table in the 
  PostgreSQL database.
  """
    
  id: int