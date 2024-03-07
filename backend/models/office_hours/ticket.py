from pydantic import BaseModel
from datetime import datetime

from .event import OfficeHoursEventPartial
from public_user import PublicUser
from .ticket_type import TicketType
from .ticket_state import TicketState

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketDraft(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursTicket` that has not been created yet.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    office_hours_event: OfficeHoursEventPartial
    description: str
    type: TicketType
    state: TicketState
    closed_at: datetime | None = None


class OfficeHoursTicket(OfficeHoursTicketDraft):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    created_at: datetime
    caller_id: int | None = None
    have_concerns: bool = False
    caller_notes: str = ""


class OfficeHoursTicketPartial(OfficeHoursTicket):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    description: str | None = None
    type: TicketType | None = None
    state: TicketState | None = None
    closed_at: datetime | None = None
    caller_id: int | None = None
    have_concerns: bool | None = None
    caller_notes: str | None = None
