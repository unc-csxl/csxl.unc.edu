from pydantic import BaseModel
from datetime import datetime, date
from oh_type import OfficeHoursType

__authors__ = ["Sadie Amato"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEvent(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursEvent` that has not been created yet.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database.
    """
    id: int | None = None
    office_hours_section_id: int
    location_id: int
    type: OfficeHoursType
    title: str
    description: str
    location_description: str
    date: date
    start_time: datetime
    end_time: datetime
    
