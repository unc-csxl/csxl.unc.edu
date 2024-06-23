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

    @classmethod
    def from_string(cls, str: str):
        if str == "Conceptual Help":
            return TicketType.CONCEPTUAL_HELP
        if str == "Assignment Help":
            return TicketType.ASSIGNMENT_HELP

    def to_string(self) -> str:
        if self == TicketType.CONCEPTUAL_HELP:
            return "Conceptual Help"
        if self == TicketType.ASSIGNMENT_HELP:
            return "Assignment Help"
