"""OH Ticket API

This API is used to access OH ticket data for history purposes."""

from fastapi import APIRouter, Depends

from backend.models.office_hours.oh_ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
)
from backend.models.office_hours.oh_ticket_details import OfficeHoursTicketDetails
from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Bailey DeSouza"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/office-hours/ticket")
openapi_tags = {
    "name": "Office Hours",
    "description": "Office hours ticket functionality",
}


@api.post("", response_model=OfficeHoursTicketDetails, tags=["Office Hours"])
def new_oh_ticket(
    oh_ticket: OfficeHoursTicketDraft,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Adds a new OH ticket to the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket created
    """
    return oh_ticket_service.create(subject, oh_ticket)


@api.get(
    "/{section_id}",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_oh_tickets_by_section(
    section_id: int,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH section

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given section
    """
    return oh_ticket_service.get_tickets_by_section(subject, section_id)


# TODO: check this api route
@api.get("", response_model=list[OfficeHoursTicketDetails], tags=["Office Hours"])
def get_oh_tickets_by_section_and_user(
    section_id: int,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH section and user

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given section and for the specific user
    """
    return oh_ticket_service.get_tickets_by_section_and_user(subject, section_id)


@api.get(
    "/{event_id}", response_model=list[OfficeHoursTicketDetails], tags=["Office Hours"]
)
def get_oh_tickets_by_event(
    event_id: int,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH event

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given event
    """
    return oh_ticket_service.get_tickets_by_event(subject, event_id)


@api.put("", response_model=OfficeHoursTicketDetails, tags=["Academics"])
def update_oh_ticket(
    oh_ticket: OfficeHoursTicket,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Updates an OfficeHoursTicket to the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket updated
    """
    return oh_ticket_service.update(subject, oh_ticket)


# TODO: Please check this api route
@api.put("/state", response_model=OfficeHoursTicketDetails, tags=["Academics"])
def update_oh_ticket_state(
    oh_ticket: OfficeHoursTicket,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Updates an OfficeHoursTicket's state in the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket updated
    """
    return oh_ticket_service.update_state(subject, oh_ticket)
