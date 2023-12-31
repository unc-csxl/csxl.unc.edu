"""Enum definition for types of room assignments for room section assignments."""

from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RoomAssignmentType(Enum):
    LECTURE_ROOM = 0
    OFFICE_HOURS = 1
