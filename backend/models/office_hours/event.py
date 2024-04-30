from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

from ..room import Room, RoomPartial
from .section import OfficeHoursSection, OfficeHoursSectionPartial
from .event_type import OfficeHoursEventModeType, OfficeHoursEventType

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventDraft(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursEvent` that has not been created yet.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database
    """

    oh_section: OfficeHoursSectionPartial
    room: RoomPartial
    mode: OfficeHoursEventModeType
    type: OfficeHoursEventType
    description: str = ""
    location_description: str = ""
    event_date: date
    start_time: datetime
    end_time: datetime


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


class OfficeHoursEventDailyRecurringDraft(BaseModel):

    draft: OfficeHoursEventDraft
    recurring_start_date: date
    recurring_end_date: date


class OfficeHoursEventWeeklyRecurringDraft(OfficeHoursEventDailyRecurringDraft):

    selected_week_days: list[Weekday]


class OfficeHoursEvent(OfficeHoursEventDraft):
    """
    Pydantic model to represent an `OfficeHoursEvent`.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database.
    """

    id: int
    oh_section: OfficeHoursSection
    room: Room


class OfficeHoursEventPartial(OfficeHoursEvent):
    """
    Pydantic model to represent a partial `OfficeHoursEvent`.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database.
    """

    oh_section: OfficeHoursSection | None = None
    room: Room | None = None
    mode: OfficeHoursEventModeType | None = None
    type: OfficeHoursEventType | None = None
    description: str | None = None
    location_description: str | None = None
    event_date: date | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
