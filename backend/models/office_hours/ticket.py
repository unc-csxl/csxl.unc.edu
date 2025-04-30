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


class NewOfficeHoursTicket(BaseModel):
    """
    Pydantic model to represent a new ticket.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    description: str
    type: TicketType
    office_hours_id: int


class OfficeHoursTicket(NewOfficeHoursTicket):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    state: TicketState = TicketState.QUEUED
    created_at: datetime = datetime.now()
    called_at: datetime | None
    closed_at: datetime | None
    have_concerns: bool = False
    caller_notes: str = ""
    caller_id: int | None


class OfficeHoursTicketCsvRow(BaseModel):
    """
    Pydantic model to represent a user's ticket in CSV format, which is used for
    exporting ticket data to a CSV file in the ticket statistics feature.
    """

    student: str
    description: str
    type: str
    created_at: str
    called_at: str
    called_by: str
    closed_at: str
    duration_minutes: int
    wait_time_minutes: int


class OfficeHoursTicketClosePayload(BaseModel):
    """
    Pydantic model to represent a payload for deleting a ticket.
    """

    has_concerns: bool
    caller_notes: str
