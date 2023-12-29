"""Enum definition for roles in a course section roster."""

from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RosterRole(Enum):
    STUDENT = 0
    UTA = 1
    GTA = 2
    INSTRUCTOR = 3
