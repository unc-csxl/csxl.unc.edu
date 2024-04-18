from pydantic import BaseModel

__authors__ = ["Sadie Amato"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursSectionTrailingWeekData(BaseModel):
    """
    Pydantic model to represent the trailing week data gathered for an office hours section's data page.
    Time statistics will be computed in minutes.
    """

    number_of_tickets: int = 0
    number_of_students: int = 0
    average_wait_time: float = 0.0
    standard_deviation_wait_time: float = 0.0
    average_ticket_duration: float = 0.0
    standard_deviation_ticket_duration: float = 0.0
