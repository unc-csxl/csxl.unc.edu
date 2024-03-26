from pydantic import BaseModel
from datetime import datetime

from ...models.user import UserIdentity

from ..academics.section_member import SectionMember
from .event import OfficeHoursEvent, OfficeHoursEventPartial
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

    oh_event: OfficeHoursEventPartial
    description: str
    type: TicketType
    creators: list[UserIdentity] = []


class OfficeHoursTicket(OfficeHoursTicketDraft):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    created_at: datetime
    state: TicketState = TicketState.QUEUED
    have_concerns: bool = False
    caller_notes: str = ""
    called_at: datetime | None = None
    closed_at: datetime | None = None
    oh_event: OfficeHoursEvent
    creators: list[SectionMember] = []


class OfficeHoursTicketPartial(OfficeHoursTicket):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    description: str | None = None
    type: TicketType | None = None
    state: TicketState | None = None
    called_at: datetime | None = None
    closed_at: datetime | None = None
    caller_id: int | None = None
    have_concerns: bool | None = None
    caller_notes: str | None = None
    oh_event: OfficeHoursEventPartial
