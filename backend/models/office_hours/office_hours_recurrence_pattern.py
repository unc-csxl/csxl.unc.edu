from typing import TYPE_CHECKING, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator, ValidationInfo
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from ...entities.office_hours.office_hours_entity import OfficeHoursEntity


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursRecurrencePatternBase(SQLModel):
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=False)
    recur_monday: bool = Field(default=False, nullable=False)
    recur_tuesday: bool = Field(default=False, nullable=False)
    recur_wednesday: bool = Field(default=False, nullable=False)
    recur_thursday: bool = Field(default=False, nullable=False)
    recur_friday: bool = Field(default=False, nullable=False)
    recur_saturday: bool = Field(default=False, nullable=False)
    recur_sunday: bool = Field(default=False, nullable=False)


class OfficeHoursRecurrencePattern(OfficeHoursRecurrencePatternBase, table=True):
    id: int = Field(primary_key=True)
    office_hours: list["OfficeHoursEntity"] = Relationship(
        back_populates="recurrence_pattern", cascade_delete=True
    )


class NewOfficeHoursRecurrencePattern(OfficeHoursRecurrencePatternBase):
    """
    Pydantic model to represent new office hours recurrence pattern.

    This model is based on the `OfficeHoursRecurrencePatternEntity` model, which
    defines the shape of the office hours recurrence pattern table in the
    PostgreSQL database.
    """

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


# class OfficeHoursRecurrencePattern(NewOfficeHoursRecurrencePattern):
#     """
#     Pydantic model to represent office hours recurrence pattern.

#     This model is based on the `OfficeHoursRecurrencePatternEntity` model, which
#     defines the shape of the office hours recurrence pattern table in the
#     PostgreSQL database.
#     """

#     id: int
