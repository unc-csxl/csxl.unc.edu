from pydantic import BaseModel
from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationReviewStatus(Enum):
    NOT_PREFERRED = "Not Preferred"
    NOT_PROCESSED = "Not Processed"
    PREFERRED = "Preferred"
