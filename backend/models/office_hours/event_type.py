"""Enum for the type of an office hours event."""

from enum import Enum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventType(Enum):
    """
    Determines the type of an office hours event.
    """

    OFFICE_HOURS = 0
    TUTORING = 1
    REVIEW_SESSION = 2


class OfficeHoursEventModeType(Enum):
    """
    Determines the office hours event mode.
    """

    IN_PERSON = 0
    VIRTUAL_STUDENT_LINK = 1
    VIRTUAL_OUR_LINK = 2
