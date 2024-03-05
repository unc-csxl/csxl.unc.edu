from backend.models.academics.section_member import SectionMember
from backend.models.office_hours.ticket import OfficeHoursTicket

__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SectionMemberDetails(SectionMember):
    """
    Pydantic model to represent an `SectionMember`, including back-populated
    relationship fields.

    This model is based on the `SectionMemberEntity` model, which defines the shape
    of the `SectionMember` database in the PostgreSQL database.
    """

    created_tickets: list[OfficeHoursTicket]
    called_ticket: list[OfficeHoursTicket]
