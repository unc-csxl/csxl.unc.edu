"""Enum for the type of an office hours event."""

from enum import Enum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventType(Enum):
    """
    Determines the type of an office hours event.
    """

    OFFICE_HOURS = "Office Hours"
    TUTORING = "Tutoring"
    REVIEW_SESSION = "Review Session"


class OfficeHoursEventModeType(Enum):
    """
    Determines the office hours event mode.
    """

    IN_PERSON = "In-Person"
    VIRTUAL_STUDENT_LINK = "Virtual - Student Link"
    VIRTUAL_OUR_LINK = "Virtual - Our Link"
