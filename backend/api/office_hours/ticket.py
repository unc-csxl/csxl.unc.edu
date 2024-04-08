"""OH Ticket API

This API is used to access OH ticket data for history purposes."""

from fastapi import APIRouter, Depends, HTTPException

from ...models.office_hours.ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
    OfficeHoursTicketPartial,
)
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...services.office_hours.ticket import OfficeHoursTicketService
from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/office-hours/ticket")
openapi_tags = {
    "name": "Office Hours",
    "description": "Office hours ticket functionality",
}


# TODO: Fix Comments
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
    "/{oh_ticket_id}",
    response_model=OfficeHoursTicketDetails,
    tags=["Office Hours"],
)
def get_oh_ticket_by_id(
    oh_ticket_id: int,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Gets an OH ticket by its id

    Returns:
        OfficeHoursTicketDetails: OH ticket with the given id
    """
    try:
        return oh_ticket_service.get_ticket_by_id(subject, oh_ticket_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# @api.put(
#     "/{oh_ticket_id}", response_model=OfficeHoursTicketDetails, tags=["Office Hours"]
# )
# def update_oh_ticket(
#     oh_ticket: OfficeHoursTicketPartial,
#     subject: User = Depends(registered_user),
#     oh_ticket_service: OfficeHoursTicketService = Depends(),
# ) -> OfficeHoursTicketDetails:
#     """
#     Updates an OfficeHoursTicket to the database

#     Returns:
#         OfficeHoursTicketDetails: OH Ticket updated
#     """
#     return oh_ticket_service.update(subject, oh_ticket)


@api.put(
    "/called/{oh_ticket_id}",
    response_model=OfficeHoursTicketDetails,
    tags=["Office Hours"],
)
def update_oh_ticket_when_called(
    oh_ticket: OfficeHoursTicketPartial,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Updates an OfficeHoursTicket to the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket updated
    """
    try:
        return oh_ticket_service.update_called_state(subject, oh_ticket)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.put(
    "/cancel/{oh_ticket_id}",
    response_model=OfficeHoursTicketDetails,
    tags=["Office Hours"],
)
def cancel_oh_ticket(
    oh_ticket: OfficeHoursTicketPartial,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Updates an OfficeHoursTicket's state in the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket updated
    """
    try:
        oh_ticket_model = oh_ticket_service.get_ticket_by_id(subject, oh_ticket.id)
        return oh_ticket_service.cancel_ticket(subject, oh_ticket_model)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put(
    "/close/{oh_ticket_id}",
    response_model=OfficeHoursTicketDetails,
    tags=["Office Hours"],
)
def close_oh_ticket(
    oh_ticket: OfficeHoursTicketPartial,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Updates an OfficeHoursTicket's state in the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket updated
    """
    try:
        oh_ticket_model = oh_ticket_service.get_ticket_by_id(subject, oh_ticket.id)
        return oh_ticket_service.close_ticket(subject, oh_ticket_model)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put(
    "/feedback/{oh_ticket_id}",
    response_model=OfficeHoursTicketDetails,
    tags=["Office Hours"],
)
def update_oh_ticket_feedback(
    oh_ticket: OfficeHoursTicketPartial,
    subject: User = Depends(registered_user),
    oh_ticket_service: OfficeHoursTicketService = Depends(),
) -> OfficeHoursTicketDetails:
    """
    Updates an OfficeHoursTicket's state in the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket updated
    """
    try:
        return oh_ticket_service.update_ticket_feedback(subject, oh_ticket)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
