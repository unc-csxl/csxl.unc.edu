"""Enum for the type of an office hours event."""

from enum import Enum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OfficeHoursType(Enum):
    """
    Determines the type of an office hours.
    """

    OFFICE_HOURS = 0
    TUTORING = 1
    REVIEW_SESSION = 2
    VIRTUAL_OFFICE_HOURS = 3
    VIRTUAL_TUTORING = 4
    VIRTUAL_REVIEW_SESSION = 5
