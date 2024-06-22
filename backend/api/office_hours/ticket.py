"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.office_hours.ticket import OfficeHourTicketService
from ...models.user import User
from ...models.office_hours.ticket import NewOfficeHoursTicket

from ...models.academics.my_courses import OfficeHourTicketOverview

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours/ticket")


@api.put("/{id}/call", tags=["Office Hours"])
def call_ticket(
    id: int,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Calls a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_ticket_svc.call_ticket(subject, id)


@api.put("/{id}/cancel", tags=["Office Hours"])
def cancel_ticket(
    id: int,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Cancels a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_ticket_svc.cancel_ticket(subject, id)


@api.put("/{id}/close", tags=["Office Hours"])
def close_ticket(
    id: int,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Closes a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_ticket_svc.close_ticket(subject, id)


@api.post("/", tags=["Office Hours"])
def new_oh_ticket(
    ticket: NewOfficeHoursTicket,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Adds a new OH ticket to the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket created
    """
    return oh_ticket_svc.create_ticket(subject, ticket)
