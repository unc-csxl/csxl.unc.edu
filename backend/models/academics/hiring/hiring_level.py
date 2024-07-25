from pydantic import BaseModel
from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringLevelClassification(Enum):
    IOR = "Instructor of Record"
    PHD = "PhD"
    MS = "MS"
    UG = "UG"
