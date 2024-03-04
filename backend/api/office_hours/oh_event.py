"""OH Event API

This API is used to access OH Event data."""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.oh_event import OfficeHoursEvent, OfficeHoursEventDraft
from ...models.office_hours.oh_event_details import OfficeHoursEventDetails
from ...services.office_hours.oh_event import OfficeHoursEventService

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


@api.post("", response_model=OfficeHoursEventDetails, tags=["Office Hours"])
def new_oh_event(
    oh_event: OfficeHoursEventDraft,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEventDetails:
    """
    Adds a new OH event to the database

    Returns:
        OfficeHoursEventDetails: OH Event created
    """
    return oh_event_service.create(subject, oh_event)


@api.put("/{oh_event_id}", response_model=OfficeHoursEventDetails, tags=["Office Hours"])
def update_oh_event(
    oh_event_id: int,
    oh_event: OfficeHoursEvent,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEventDetails:
    """
    Updates an OfficeHoursEvent to the database

    Returns:
        OfficeHoursEventDetails: OH Event updated
    """
    return oh_event_service.update(subject, oh_event_id, oh_event)


@api.delete("/{oh_event_id}", response_model=None, tags=["Office Hours"])
def delete_oh_event(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
):
    """
    Deletes an OfficeHoursEvent from the database
    """
    oh_event: OfficeHoursEventDetails = oh_event_service.get_event_by_id(oh_event_id)
    return oh_event_service.delete(subject, oh_event)

@api.get("/{oh_event_id}", response_model=OfficeHoursEventDetails, tags=["Office Hours"])
def get_oh_section_by_id(
    oh_event_id: int, subject: User = Depends(registered_user), oh_event_service: OfficeHoursEventService = Depends()
) -> OfficeHoursEventDetails:
    """
    Gets an OH event by OH event ID

    Returns:
        OfficeHoursEventDetails: The OH event with the given OH event id
    """
    return oh_event_service.get_event_by_id(subject, oh_event_id)


@api.get("/section/{section_id}/upcoming", response_model=list[OfficeHoursEventDetails], tags=["Office Hours"])
def get_upcoming_oh_events_by_section(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    start: datetime = datetime.now(),
    end: datetime = datetime.now() + timedelta(weeks=1),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> list[OfficeHoursEventDetails]:
    """
    Gets list of upcoming OH events within a time range by section ID

    Returns:
        list[OfficeHoursSectionDetails]: OH events associated with a given section in a time range
    """
    time_range = TimeRange(start=start, end=end)
    return oh_event_service.get_upcoming_events_by_section(
        subject, oh_section_id, time_range
    )


@api.get("/upcoming", response_model=list[OfficeHoursEventDetails], tags=["Office Hours"])
def get_upcoming_oh_events_by_user(
    start: datetime = datetime.now(),
    subject: User = Depends(registered_user),
    end: datetime = datetime.now() + timedelta(weeks=1),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> list[OfficeHoursEventDetails]:
    """
    Gets list of upcoming OH events within a time range by user

    Returns:
        list[OfficeHoursSectionDetails]: OH events associated with a given user in a time range
    """
    time_range = TimeRange(start=start, end=end)
    return oh_event_service.get_upcoming_events_by_user(subject, time_range)
