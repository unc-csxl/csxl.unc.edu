from ..academics.section import Section
from oh_event import OfficeHoursEvent
from oh_section import OfficeHoursSection

__authors__ = ["Sadie Amato"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursSectionDetails(OfficeHoursSection):
    """
    Pydantic model to represent an `OfficeHoursSection`, including back-populated
    relationship fields.

    This model is based on the `OfficeHoursSectionEntity` model, which defines the shape
    of the `OfficeHoursSection` database in the PostgreSQL database.
    """

    sections: list[Section]
    events: list[OfficeHoursEvent]
    