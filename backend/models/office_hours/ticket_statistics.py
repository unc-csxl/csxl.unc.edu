from pydantic import BaseModel
from datetime import datetime

from .ticket_type import TicketType
from .ticket_state import TicketState
from .ticket_details import OfficeHoursTicketDetails

__authors__ = ["Mira Mohan", "Lauren Ferlito"]

__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OfficeHoursTicketStatistics(BaseModel):
    """
    Pydantic model to represent a user's ticket statistics.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    average_wait_time: int
    average_duration: int
    total_conceptual: int
    total_assignment: int
    student_total_tickets: int
    student_total_tickets_weekly: int
