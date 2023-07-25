from fastapi import APIRouter, Depends, HTTPException
from ..services.event import EventService
from ..models.event import Event
from ..models.event_detail import EventDetail
from datetime import datetime
from backend.api.authentication import registered_user
from backend.models.user import User
from ..env import getenv

from backend.services.user import UserService

api = APIRouter(prefix="/api/events")

@api.get("", tags=['Event'])
def get_events(event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table
    """

    # Return all events
    return event_service.all()

@api.get("/org/{id}/", tags=['Event'])
def get_events_org_id(org_id: int, event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events from an organization
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table from a specific organization
    """

    # Return all events
    return event_service.get_from_org_id(org_id)

@api.get("/time/", tags=['Event'])
def get_events_from_time_range(start: datetime, end: datetime, event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events from a time range
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table in a specific time range
    """

    # Return all events
    return event_service.get_from_time_range(start, end)

@api.post("", tags=['Event'])
def new_event(event: Event, subject: User = Depends(registered_user), event_service: EventService = Depends()) -> EventDetail:
    """
    Create event
    Returns:
        EventDetail: Latest iteration of the created or updated event after changes made
    """

    # Try to create event
    try:
        return event_service.create(subject, event)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{id}", responses={404: {"model": None}}, tags=['Event'])
def get_event_from_id(id: int, event_service: EventService = Depends()) -> EventDetail:
    """
    Get event with matching id
    Returns:
        EventDetail: EventDetail with matching id
    """
    
    # Try to get event with matching id
    try: 
        # Return event
        return event_service.get_from_id(id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.put("", responses={404: {"model": None}}, tags=['Event'])
def update_event(event: EventDetail, subject: User = Depends(registered_user), event_service: EventService = Depends()) -> EventDetail:
    """
    Update event
    Returns:
        EventDetail: Updated event
    """
    try:
        return event_service.update(subject, event)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['Event'])
def delete_event(id: int, subject: User = Depends(registered_user), event_service = Depends(EventService)):
    """
    Delete event based on id
    """
    try:
        return event_service.delete(subject, id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))