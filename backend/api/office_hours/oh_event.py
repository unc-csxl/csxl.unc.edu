"""OH Event API

This API is used to access OH Event data."""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from backend.models.coworking.time_range import TimeRange
from backend.models.office_hours.oh_event import OfficeHoursEventDraft
from backend.models.office_hours.oh_event_details import OfficeHoursEventDetails

from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Bailey DeSouza"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/office-hours")
openapi_tags = {
    "name": "Office Hours",
    "description": "Office hours event, event, and ticket functionality",
}


@api.post("/event", response_model=OfficeHoursEventDetails, tags=["Office Hours"])
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


@api.put("", response_model=OfficeHoursEventDetails, tags=["Academics"])
def update_oh_event(
    oh_event: OfficeHoursEventDraft,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> OfficeHoursEventDetails:
    """
    Updates an OfficeHoursEvent to the database

    Returns:
        OfficeHoursEventDetails: OH Event updated
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
    return oh_event_service.delete(subject, oh_event_id)


@api.get("", response_model=list[OfficeHoursEventDetails], tags=["Office Hours"])
def get_oh_events_by_section(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_event_service: OfficeHoursEventService = Depends(),
) -> list[OfficeHoursEventDetails]:
    """
    Gets list of OH events by section ID

    Returns:
        list[OfficeHoursSectionDetails]: OH events associated with a given section
    """
    return oh_event_service.get_events_by_section(subject, oh_section_id)


@api.get("", response_model=list[OfficeHoursEventDetails], tags=["Office Hours"])
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


@api.get("", response_model=list[OfficeHoursEventDetails], tags=["Office Hours"])
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
