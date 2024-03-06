"""Enum for the state of an office hours ticket."""

from enum import Enum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class TicketState(Enum):
    """
    Determines the state of a ticket.
    """

    QUEUED = 0
    CALLED = 1
    CLOSED = 2
    CANCELED = 3
