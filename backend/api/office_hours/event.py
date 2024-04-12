"""OH Event API

This API is used to access OH Event data."""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException

from backend.models.office_hours.event_status import (
    OfficeHoursEventStatus,
    StudentOfficeHoursEventStatus,
)

from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.event import OfficeHoursEvent, OfficeHoursEventDraft
from ...models.office_hours.event_details import OfficeHoursEventDetails
from ...services.office_hours.event import OfficeHoursEventService

from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/office-hours/event")
openapi_tags = {
    "name": "Office Hours",
    "description": "Office hours event functionality",
}


@api.post("", response_model=OfficeHoursEvent, tags=["Office Hours"])
def new_oh_event(
    oh_event: OfficeHoursEventDraft,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEvent:
    """
    Adds a new OH event to the database

    Returns:
        OfficeHoursEvent: OH Event created
    """
    return oh_event_service.create(subject, oh_event)


@api.put("/{oh_event_id}", response_model=OfficeHoursEvent, tags=["Office Hours"])
def update_oh_event(
    oh_event: OfficeHoursEvent,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEvent:
    """
    Updates an OfficeHoursEvent to the database

    Returns:
        OfficeHoursEvent: OH Event updated
    """
    return oh_event_service.update(subject, oh_event)


@api.delete("/{oh_event_id}", response_model=None, tags=["Office Hours"])
def delete_oh_event(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
):
    """
    Deletes an OfficeHoursEvent from the database
    """
    oh_event: OfficeHoursEvent = oh_event_service.get_event_by_id(oh_event_id)
    return oh_event_service.delete(subject, oh_event)


@api.get("/{oh_event_id}", response_model=OfficeHoursEvent, tags=["Office Hours"])
def get_oh_event_by_id(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEvent:
    """
    Gets an OH event by OH event ID

    Returns:
        OfficeHoursEvent: The OH event with the given OH event id
    """
    return oh_event_service.get_event_by_id(subject, oh_event_id)


@api.get("/upcoming", response_model=list[OfficeHoursEvent], tags=["Office Hours"])
def get_upcoming_oh_events_by_user(
    start: datetime = datetime.now(),
    subject: User = Depends(registered_user),
    end: datetime = datetime.now() + timedelta(weeks=1),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> list[OfficeHoursEvent]:
    """
    Gets list of upcoming OH events within a time range by user

    Returns:
        list[OfficeHoursSectionDetails]: OH events associated with a given user in a time range
    """
    time_range = TimeRange(start=start, end=end)
    return oh_event_service.get_upcoming_events_by_user(subject, time_range)


@api.get(
    "/{oh_event_id}/tickets",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_oh_tickets_by_event(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH event

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given event
    """
    oh_event: OfficeHoursEventDetails = oh_event_service.get_event_by_id(
        subject, oh_event_id
    )
    oh_event: OfficeHoursEvent = oh_event_service.get_event_by_id(subject, oh_event_id)
    return oh_event_service.get_event_tickets(subject, oh_event)


@api.get(
    "/{oh_event_id}/queue",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_queued_and_called_oh_tickets_by_event(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of all queued and called OH tickets by OH event

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets fitting the criteria within the given event
    """
    oh_event: OfficeHoursEvent = oh_event_service.get_event_by_id(subject, oh_event_id)
    return oh_event_service.get_queued_and_called_event_tickets(subject, oh_event)


@api.get(
    "/{oh_event_id}/queue-stats",
    response_model=OfficeHoursEventStatus,
    tags=["Office Hours"],
)
def get_queued_and_called_oh_tickets_by_event(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEventStatus:
    """
    Gets Queued and Called Ticket Status Count For Given Event.

    Returns:
        (OfficeHoursEventStatus): Model that contains queued and called ticket count
    """
    try:
        oh_event: OfficeHoursEvent = oh_event_service.get_event_by_id(
            subject, oh_event_id
        )
        return oh_event_service.get_queued_helped_stats_by_oh_event(subject, oh_event)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/{oh_event_id}/student-queue-stats/{ticket_id}",
    response_model=StudentOfficeHoursEventStatus,
    tags=["Office Hours"],
)
def get_queued_and_called_oh_tickets_by_event_for_student(
    oh_event_id: int,
    ticket_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> StudentOfficeHoursEventStatus:
    """
    Gets Queued and Called Ticket Status Count For Given Event.

    Returns:
        (OfficeHoursEventStatus): Model that contains queued and called ticket count
    """
    try:
        oh_event: OfficeHoursEvent = oh_event_service.get_event_by_id(
            subject, oh_event_id
        )
        return oh_event_service.get_queued_helped_stats_by_oh_event_for_student(
            subject, oh_event, ticket_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
