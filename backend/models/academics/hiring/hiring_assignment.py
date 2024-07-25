from pydantic import BaseModel
from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringAssignmentStatus(Enum):
    DRAFT = "Draft"
    COMMIT = "Commit"
    FINAL = "Final"
