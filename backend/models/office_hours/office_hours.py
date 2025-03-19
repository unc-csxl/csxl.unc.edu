from datetime import datetime
from zoneinfo import ZoneInfo
from enum import Enum
from pydantic import BaseModel, field_validator, ValidationInfo

from .office_hours_recurrence_pattern import OfficeHoursRecurrencePattern
from .event_type import OfficeHoursEventModeType, OfficeHoursEventType

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


# TODO: Figure Out Better Place For These
class Weekday(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

    def __str__(self):
        return "%s" % self.value


class NewOfficeHours(BaseModel):
    """
    Pydantic model to represent new office hours.

    This model is based on the `OfficeHoursEntity` model, which defines the shape
    of the office hours database in the PostgreSQL database.
    """

    type: OfficeHoursEventType
    mode: OfficeHoursEventModeType
    description: str
    location_description: str
    start_time: datetime
    end_time: datetime
    course_site_id: int
    room_id: str
    recurrence_pattern_id: int | None

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def remove_timezone(cls, value: datetime):
        if type(value) == str:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            dt = dt.astimezone(ZoneInfo("America/New_York"))
            dt = dt.replace(tzinfo=None)
            return dt
        return value

    @field_validator("end_time")
    @classmethod
    def check_end_greater_than_start(cls, v: datetime, info: ValidationInfo):
        if v <= info.data["start_time"]:
            raise ValueError("end must be greater than start")
        return v


class OfficeHours(NewOfficeHours):
    """
    Pydantic model to represent an `OfficeHours`.

    This model is based on the `OfficeHoursEntity` model, which defines the shape
    of the `OfficeHours` database in the PostgreSQL database.
    """

    id: int
