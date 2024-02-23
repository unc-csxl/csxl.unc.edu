"""Enum for the type of an office hours ticket."""

from enum import Enum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class TicketType(Enum):
    """
    Determines the type of a ticket.
    """

    CONCEPTUAL_HELP = 0
    ASSIGNMENT_HELP = 1
