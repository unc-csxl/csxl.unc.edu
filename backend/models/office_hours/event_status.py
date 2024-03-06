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


class StudentOfficeHoursEventStatus(BaseModel):
    """Pydantic model to represent the status of a given event, including their position in the queues, for a given student."""

    open_tickets_count: int
    queued_tickets_count: int
    queue_position: int
