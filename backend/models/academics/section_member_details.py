from ...models.academics.section import Section
from ...models.academics.section_member import SectionMember
from ...models.office_hours.ticket import OfficeHoursTicket
from ...models.user import User

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

    user: User
    section: Section
    created_tickets: list[OfficeHoursTicket]
    called_ticket: list[OfficeHoursTicket]
