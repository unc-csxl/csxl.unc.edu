from backend.models.office_hours.office_hours_recurrence_pattern import (
    OfficeHoursRecurrencePattern,
)
from .ticket import OfficeHoursTicket
from .office_hours import OfficeHours, CourseSite
from ..room import Room

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
    "Jade Keegan",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursDetails(OfficeHours):
    """
    Pydantic model to represent an `OfficeHours`, including back-populated
    relationship fields.

    This model is based on the `OfficeHoursEntity` model, which defines the shape
    of the `OfficeHours` database in the PostgreSQL database.
    """

    course_site: CourseSite
    room: Room
    recurrence_pattern: OfficeHoursRecurrencePattern
    tickets: list[OfficeHoursTicket]
