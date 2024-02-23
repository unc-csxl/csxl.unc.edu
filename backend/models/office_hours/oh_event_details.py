from oh_ticket import OfficeHoursTicket
from ..room import Room
from oh_event import OfficeHoursEvent
from oh_section import OfficeHoursSection

__authors__ = ["Sadie Amato"]
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
    location: Room
    tickets: list[OfficeHoursTicket]



    