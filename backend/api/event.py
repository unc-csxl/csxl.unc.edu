"""Event API

Event routes are used to create, retrieve, and update Events."""

from fastapi import APIRouter, Depends, HTTPException
from ..services.event import EventService
from ..models.event import Event
from ..models.event_detail import EventDetail
from datetime import datetime
from backend.api.authentication import registered_user
from backend.models.user import User

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

api = APIRouter(prefix="/api/events")

@api.get("", tags=['Event'])
def get_events(event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events
    
    Parameters:
        event_service: a valid EventService

    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table
    """

    # Return all events
    return event_service.all()

@api.get("/org/{id}/", tags=['Event'])
def get_events_org_id(org_id: int, event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events from an organization

    Parameters:
        org_id: an int representing a unique identifier for an organization
        event_service: a valid EventService

    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table from a specific organization
    """

    # Return all events corresponding to organization
    return event_service.get_from_org_id(org_id)

@api.get("/time/", tags=['Event'])
def get_events_from_time_range(start: datetime, end: datetime, event_service: EventService = Depends()) -> list[EventDetail]:
    """
    Get all events from a time range

    Parameters:
        start: a datetime object representing the start of the range
        end: a datetime object representing the end of the range
        event_service: a valid EventService

    Returns:
        list[EventDetail]: All `EventDetail`s in the `Event` database table in a specific time range
    """

    # Return all events in provided time range
    return event_service.get_from_time_range(start, end)

@api.post("", tags=['Event'])
def new_event(event: Event, subject: User = Depends(registered_user), event_service: EventService = Depends()) -> EventDetail:
    """
    Create event

    Parameters:
        event: a valid Event model
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        EventDetail: Latest iteration of the created or updated event after changes made

    Raises:
        HTTPException 404 if create() raises an Exception
    """

    try:
        # Try to create and return event
        return event_service.create(subject, event)
    except Exception as e:
        # Raise 404 exception if creation fails (request body is shaped incorrectly)
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{id}", responses={404: {"model": None}}, tags=['Event'])
def get_event_from_id(id: int, event_service: EventService = Depends()) -> EventDetail:
    """
    Get event with matching id

    Parameters:
        id: an int representing the id of the event
        subject: a valid User model representing the currently logged in User

    Returns:
        EventDetail: EventDetail with matching id

    Raises:
        HTTPException 404 if get_from_id() raises an Exception
    """
    
    try: 
        # Try to get and return event with matching id
        return event_service.get_from_id(id)
    except Exception as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))

@api.put("", responses={404: {"model": None}}, tags=['Event'])
def update_event(event: EventDetail, subject: User = Depends(registered_user), event_service: EventService = Depends()) -> EventDetail:
    """
    Update event

    Parameters:
        event: a valid EventDetail model
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        EventDetail: Updated event

    Raises:
        HTTPException 404 if update() raises an Exception
    """

    try:
        # Try to update and return Event
        return event_service.update(subject, event)
    except Exception as e:
        # Raise 404 exception if event doesn't exist or user not allowed to update event
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['Event'])
def delete_event(id: int, subject: User = Depends(registered_user), event_service = Depends(EventService)):
    """
    Delete event based on id

    Parameters:
        id: an int representing the id of the event
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    try:
        # Try to delete event
        event_service.delete(subject, id)
    except Exception as e:
        # Raise 404 exception if search fails (no response or item to delete does not exist)
        raise HTTPException(status_code=404, detail=str(e))