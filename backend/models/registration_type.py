"""Determines the type of an event registration."""

from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RegistrationType(Enum):
    """
    Determines the type of an event registration.
    """

    ATTENDEE = 0
    ORGANIZER = 1
