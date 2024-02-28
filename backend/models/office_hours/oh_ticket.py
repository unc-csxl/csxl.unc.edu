from pydantic import BaseModel
from datetime import datetime
from ticket_type import TicketType
from ticket_state import TicketState

__authors__ = ["Sadie Amato"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketDraft(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursTicket` that has not been created yet.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int | None = None
    office_hours_event_id: int
    description: str
    type: TicketType
    state: TicketState
    created_at: datetime
    closed_at: datetime
    caller_id: int
    have_concerns: bool
    caller_notes: str


class OfficeHoursTicket(OfficeHoursTicketDraft):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int | None = None
