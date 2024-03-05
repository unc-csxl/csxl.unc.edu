from .ticket import OfficeHoursTicket
from ..room import Room
from .event import OfficeHoursEvent
from .section import OfficeHoursSection


__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventDetails(OfficeHoursEvent):
    """
    Pydantic model to represent an `OfficeHoursEvent`, including back-populated
    relationship fields.

    This model is based on the `OfficeHoursEventEntity` model, which defines the shape
    of the `OfficeHoursEvent` database in the PostgreSQL database.
    """

    section: OfficeHoursSection
    room: Room
    tickets: list[OfficeHoursTicket]
