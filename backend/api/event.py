from fastapi import APIRouter, Depends, HTTPException
from backend.services.event import EventService
from backend.models.event import EventDetail, Event
from datetime import datetime

api = APIRouter(prefix="/api/events")

@api.get("", tags=['EventDetail'])
def get_events(event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table
    """

    # Return all events
    return event_service.all()

@api.get("/org/{id}/", tags=['EventDetail'])
def get_events_org_id(org_id: int, event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events from an organization
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table from a specific organization
    """

    # Return all events
    return event_service.get_from_org_id(org_id)

@api.get("/time/", tags=['EventDetail'])
def get_events_from_time_range(start: datetime, end: datetime, event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events from a time range
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table in a specific time range
    """

    # Return all events
    return event_service.get_from_time_range(start, end)

@api.post("", tags=['EventDetail'])
def new_event(event: Event, event_service: EventService = Depends()) -> EventDetail:
    """
    Create event
    Returns:
        EventDetail: Latest iteration of the created or updated event after changes made
    """

    # Try to create event
    try:
        # Return created event
        return event_service.create(event)
    except Exception as e:
        # Raise 422 exception if creation fails
        # - This would occur if the request body is shaped incorrectly
        raise HTTPException(status_code=422, detail=str(e))

@api.get("/{id}", responses={404: {"model": None}}, tags=['EventDetail'])
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

@api.put("", responses={404: {"model": None}}, tags=['EventDetail'])
def update_event(organization: EventDetail, event_service: EventService = Depends()) -> EventDetail:
    """
    Update event
    Returns:
        EventDetail: Updated event
    """

    # Try to update event
    try: 
        # Return updated event
        return event_service.update(organization)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['EventDetail'])
def delete_event(id: int, event_service = Depends(EventService)):
    """
    Delete event based on id
    """

    # Try to delete event
    try:
        # Return deleted event
        return event_service.delete(id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))