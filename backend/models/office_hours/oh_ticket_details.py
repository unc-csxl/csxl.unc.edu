from ..academics.section_member import SectionMember
from oh_event import OfficeHoursEvent
from oh_ticket import OfficeHoursTicket

__authors__ = ["Sadie Amato"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketDetails(OfficeHoursTicket):
    """
    Pydantic model to represent an `OfficeHoursSection`, including back-populated
    relationship fields.

    This model is based on the `OfficeHoursSectionEntity` model, which defines the shape
    of the `OfficeHoursSection` database in the PostgreSQL database.
    """

    event: OfficeHoursEvent
    creators: list[SectionMember]
    caller: SectionMember