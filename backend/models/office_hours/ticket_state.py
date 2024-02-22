"""Determines the state of an office hours ticket."""

from enum import Enum

__authors__ = ["Madelyn Andrews"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TicketState(Enum):
    """
    Determines the state of a ticket.
    """

    PENDING = 0
    CALLED = 1
    CLOSED = 2
    CANCELED = 3
