from pydantic import BaseModel
from datetime import datetime, date

from room import RoomPartial

from .section import OfficeHoursSectionPartial
from .event_type import OfficeHoursEventType

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventDraft(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursEvent` that has not been created yet.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database
    """

    office_hours_section: OfficeHoursSectionPartial
    room: RoomPartial
    type: OfficeHoursEventType
    description: str = ""
    location_description: str = ""
    date: date
    start_time: datetime
    end_time: datetime


class OfficeHoursEvent(OfficeHoursEventDraft):
    """
    Pydantic model to represent an `OfficeHoursEvent`.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database.
    """

    id: int


class OfficeHoursEventPartial(OfficeHoursEvent):
    """
    Pydantic model to represent a partial `OfficeHoursEvent`.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database.
    """

    office_hours_section: OfficeHoursSectionPartial | None = None
    room: RoomPartial | None = None
    type: OfficeHoursEventType | None = None
    description: str | None = None
    location_description: str | None = None
    date: date | None = None  # type: ignore
    start_time: datetime | None = None
    end_time: datetime | None = None
