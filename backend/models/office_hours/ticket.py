from pydantic import BaseModel
from datetime import datetime

from .ticket_type import TicketType
from .ticket_state import TicketState

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicket(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    description: str
    type: TicketType
    state: TicketState
    created_at: datetime
    called_at: datetime | None
    closed_at: datetime | None
    have_concerns: bool
    caller_notes: str
    office_hours_id: int
    caller_id: int | None
