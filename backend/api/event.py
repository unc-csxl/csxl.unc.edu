from fastapi import APIRouter, Depends, HTTPException
from backend.services.event import EventService
from backend.models.event import EventDetail, Event
from datetime import datetime
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
import jwt
from ..env import getenv

from backend.services.user import UserService

api = APIRouter(prefix="/api/events")

_JWT_SECRET = getenv('JWT_SECRET')
_JST_ALGORITHM = 'HS256'

@api.get("", tags=['Event'])
def get_events(event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events
    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table
    """

    # Return all events
    return event_service.all()

@api.get("/org/{id}", tags=['Event'])
def get_events_from_org_id(org_id: int, event_service: EventService = Depends()) -> list[Event]:
    """
    Get all events from an organization
    Returns:
        list[Event]: All `Event`s in the `Event` database table from a specific organization
    """

    # Return all events
    return event_service.get_events_from_org_id(org_id)

@api.post("", tags=['Event'])
def new_event(event: Event, event_service: EventService = Depends()) -> Event:
    """
    Create event

    Parameters:
        event: a valid Event model
        event_service: a valid EventService

    Returns:
        Event: latest iteration of the created or updated event after changes made
    """

    # Try to create event
    try:
        # Return created event
        return event_service.create(event)
    except Exception as e:
        # Raise 422 exception if creation fails
        # - This would occur if the request body is shaped incorrectly
        raise HTTPException(status_code=422, detail=str(e))
    
@api.get("/{id}", responses={404: {"model": None}}, tags=['Event'])
def get_event_from_id(id: int, event_service: EventService = Depends()) -> Event:
    """
    Get event with matching id

    Parameters:
        id: an int representing a unique event ID
        event_service: a valid EventService
    
    Returns:
        Event: Event with matching id
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
def update_event(event: Event, event_service: EventService = Depends()) -> Event:
    """
    Update event

    Parameters:
        event: a valid Event model
        event_service: a valid EventService

    Returns:
        Event: Updated event
    """

    try: 
        # Return updated event
        return event_service.update(event)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['Event'])
def delete_event(id: int, event_service = Depends(EventService)):
    """
    Delete event based on id

    Parameters:
        id: an int representing a unique event ID
        event_service: a valid EventService
    """
   
    try:
        # Try to delete event
        event_service.delete(id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))