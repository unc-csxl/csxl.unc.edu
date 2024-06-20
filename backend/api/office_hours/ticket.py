"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics.my_courses import MyCoursesService
from ...models.user import User
from ...models.office_hours.ticket import OfficeHoursTicketDraft

from ...models.academics.my_courses import OfficeHourTicketOverview

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours/ticket")


@api.put("/{id}/call", tags=["Office Hours"])
def call_ticket(
    id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Calls a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.call_ticket(subject, id)


@api.put("/{id}/cancel", tags=["Office Hours"])
def cancel_ticket(
    id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Cancels a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.cancel_ticket(subject, id)


@api.put("/{id}/close", tags=["Office Hours"])
def close_ticket(
    id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Closes a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.close_ticket(subject, id)


@api.post("/", tags=["Office Hours"])
def new_oh_ticket(
    oh_ticket: OfficeHoursTicketDraft,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Adds a new OH ticket to the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket created
    """
    return my_courses_svc.create_ticket(subject, oh_ticket)
