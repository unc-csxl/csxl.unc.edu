from datetime import datetime

from pydantic import BaseModel

__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class NewOfficeHoursRecurrencePattern(BaseModel):
    """
    Pydantic model to represent new office hours recurrence pattern.

    This model is based on the `OfficeHoursRecurrencePatternEntity` model, which
    defines the shape of the office hours recurrence pattern table in the
    PostgreSQL database.
    """

    start_date: datetime
    end_date: datetime
    recur_monday: bool
    recur_tuesday: bool
    recur_wednesday: bool
    recur_thursday: bool
    recur_friday: bool
    recur_saturday: bool
    recur_sunday: bool


class OfficeHoursRecurrencePattern(NewOfficeHoursRecurrencePattern):
    """
    Pydantic model to represent office hours recurrence pattern.

    This model is based on the `OfficeHoursRecurrencePatternEntity` model, which
    defines the shape of the office hours recurrence pattern table in the
    PostgreSQL database.
    """

    id: int
