from pydantic import BaseModel

__authors__ = ["Mira Mohan", "Lauren Ferlito"]

__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OfficeHoursTicketStatistics(BaseModel):
    """
    Pydantic model to represent a user's ticket statistics.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    total_tickets: int
    total_tickets_weekly: int
    average_wait_time: int
    average_duration: int
    total_conceptual: int
    total_assignment: int
