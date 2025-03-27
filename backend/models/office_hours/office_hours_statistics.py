from datetime import datetime
from pydantic import BaseModel

from backend.models.public_user import PublicUser

__authors__ = ["Ajay Gandecha", "Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class StatisticsFilterData(BaseModel):
    students: list[PublicUser]
    staff: list[PublicUser]
    term_start: datetime
    term_end: datetime
