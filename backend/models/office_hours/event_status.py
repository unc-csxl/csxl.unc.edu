"""Represent the status of an office hours event."""

from pydantic import BaseModel
from typing import Sequence

from .ticket import OfficeHoursTicket

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class TAOfficeHoursEventStatus(BaseModel):
    """Pydantic model to represent the status of a given event, including tickets in the queue, for a given TA."""

    open_and_queued_tickets: Sequence[OfficeHoursTicket]
    open_tickets_count: int
    queued_tickets_count: int


class OfficeHoursEventStatus(BaseModel):
    """Pydantic model to represent the status of a given event, including their position in the queues, for a given student."""

    open_tickets_count: int
    queued_tickets_count: int


class StudentOfficeHoursEventStatus(OfficeHoursEventStatus):
    """Pydantic model to represent the position a student is in in the queue."""

    ticket_position: int


class StaffHelpingStatus(BaseModel):
    """Pydantic model to represent the ticket a staff member is currently working on.
    Ticket id will be null if no ticket is being worked on."""

    ticket_id: int | None


class StudentQueuedTicketStatus(BaseModel):
    """Pydantic model to represent the ticket a student currently has in the queue.
    Ticket id will be null if no ticket is in the queue."""

    ticket_id: int | None
