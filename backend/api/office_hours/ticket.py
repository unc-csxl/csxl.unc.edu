"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends

from ..authentication import registered_user
from ...services.office_hours.ticket import OfficeHourTicketService
from ...services.office_hours.ticket_tag import OfficeHourTicketTagService
from ...models.user import User
from ...models.office_hours.ticket import (
    NewOfficeHoursTicket,
    OfficeHoursTicketClosePayload,
)
from ...models.office_hours.ticket_tag import NewOfficeHoursTicketTag, OfficeHoursTicketTag

from ...models.academics.my_courses import OfficeHourTicketOverview

__authors__ = [
    "Ajay Gandecha",
    "Jade Keegan",
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
    payload: OfficeHoursTicketClosePayload,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Closes a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_ticket_svc.close_ticket(subject, id, payload)


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

@api.get("/{site_id}/tag", tags=["Office Hours"])
def get_ticket_tags(
    site_id: int,
    subject: User = Depends(registered_user),
    oh_ticket_tag_svc: OfficeHourTicketTagService = Depends(),
) -> list[OfficeHoursTicketTag]:
    """
    Get all ticket tags for the course site.

    Returns:
        list[OfficeHoursTicketTagDetails]: List of ticket tags
    """
    return oh_ticket_tag_svc.get_course_site_tags(subject, site_id)

@api.post("/{site_id}/tag", tags=["Office Hours"])
def new_ticket_tag(
    site_id: int,
    tag: NewOfficeHoursTicketTag,
    subject: User = Depends(registered_user),
    oh_ticket_tag_svc: OfficeHourTicketTagService = Depends(),
) -> OfficeHoursTicketTag:
    """
    Create a new ticket tag for the course site.

    Returns:
        OfficeHoursTicketTag: Ticket tag created
    """
    return oh_ticket_tag_svc.create(subject, site_id, tag)

@api.put("/{site_id}/tag", tags=["Office Hours"])
def update_ticket_tag(
    site_id: int,
    tag: OfficeHoursTicketTag,
    subject: User = Depends(registered_user),
    oh_ticket_tag_svc: OfficeHourTicketTagService = Depends(),
) -> OfficeHoursTicketTag:
    """
    Update an existing ticket tag.

    Returns:
        OfficeHoursTicketTag: Updated ticket tag
    """
    return oh_ticket_tag_svc.update(subject, site_id, tag)

@api.delete("/{site_id}/tag/{tag_id}", tags=["Office Hours"])
def delete_ticket_tag(
    site_id: int,
    tag_id: int,
    subject: User = Depends(registered_user),
    oh_ticket_tag_svc: OfficeHourTicketTagService = Depends(),
):
    """
    Delete an existing ticket tag.
    """
    oh_ticket_tag_svc.delete(subject, site_id, tag_id)