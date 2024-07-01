from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

from ..room import Room, RoomPartial
from .course_site import CourseSite
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


class OfficeHours(NewOfficeHours):
    """
    Pydantic model to represent an `OfficeHours`.

    This model is based on the `OfficeHoursEntity` model, which defines the shape
    of the `OfficeHours` database in the PostgreSQL database.
    """

    id: int
