from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator, ValidationInfo

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

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def remove_timezone(cls, value: datetime):
        if type(value) == str:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            dt = dt.astimezone(ZoneInfo("America/New_York"))
            dt = dt.replace(tzinfo=None)
            return dt
        return value

    @field_validator("end_date")
    @classmethod
    def check_end_greater_than_start(cls, v: datetime, info: ValidationInfo):
        if v <= info.data["start_date"]:
            raise ValueError("end must be greater than start")
        return v


class OfficeHoursRecurrencePattern(NewOfficeHoursRecurrencePattern):
    """
    Pydantic model to represent office hours recurrence pattern.

    This model is based on the `OfficeHoursRecurrencePatternEntity` model, which
    defines the shape of the office hours recurrence pattern table in the
    PostgreSQL database.
    """

    id: int
