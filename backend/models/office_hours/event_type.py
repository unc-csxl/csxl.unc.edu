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

    @classmethod
    def from_string(cls, str: str):
        if str == "Office Hours":
            return OfficeHoursEventType.OFFICE_HOURS
        if str == "Tutoring":
            return OfficeHoursEventType.TUTORING
        if str == "Review Session":
            return OfficeHoursEventType.REVIEW_SESSION

    def to_string(self) -> str:
        if self == OfficeHoursEventType.OFFICE_HOURS:
            return "Office Hours"
        if self == OfficeHoursEventType.TUTORING:
            return "Tutoring"
        if self == OfficeHoursEventType.REVIEW_SESSION:
            return "Review Session"


class OfficeHoursEventModeType(Enum):
    """
    Determines the office hours event mode.
    """

    IN_PERSON = 0
    VIRTUAL_STUDENT_LINK = 1
    VIRTUAL_OUR_LINK = 2

    @classmethod
    def from_string(cls, str: str):
        if str == "In-Person":
            return OfficeHoursEventModeType.IN_PERSON
        if str == "Virtual - Student Link":
            return OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK
        if str == "Virtual - Our Link":
            return OfficeHoursEventModeType.VIRTUAL_OUR_LINK

    def to_string(self) -> str:
        if self == OfficeHoursEventModeType.IN_PERSON:
            return "In-Person"
        if self == OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK:
            return "Virtual - Student Link"
        if self == OfficeHoursEventModeType.VIRTUAL_OUR_LINK:
            return "Virtual - Our Link"
