from datetime import datetime
from pydantic import BaseModel

from backend.models.office_hours.ticket_tag import OfficeHoursTicketTag
from backend.models.public_user import PublicUser

__authors__ = ["Ajay Gandecha", "Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class StatisticsFilterData(BaseModel):
    students: list[PublicUser]
    staff: list[PublicUser]
    tags: list[OfficeHoursTicketTag]
    term_start: datetime
    term_end: datetime
