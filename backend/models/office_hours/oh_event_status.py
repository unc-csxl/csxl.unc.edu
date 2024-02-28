"""Represent the status of an office hours event."""

from pydantic import BaseModel
from typing import Sequence

from oh_ticket import OfficeHoursTicket

__authors__ = ["Sadie Amato, Bailey DeSouza, Meghan Sun, Maddy Andrews"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class TAOfficeHoursEventStatus(BaseModel):
    """Pydantic model to represent the status of a given event, including tickets in the queue, for a given TA."""

    active_tickets: Sequence[OfficeHoursTicket]
    num_open: int
    num_pending: int


class StudentOfficeHoursEventStatus(BaseModel):
    """Pydantic model to represent the status of a given event, including their position in the queues, for a given student."""

    num_open: int
    num_pending: int
    position: int
