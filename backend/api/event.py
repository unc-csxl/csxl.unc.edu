from fastapi import APIRouter, Depends, HTTPException
from backend.api.authentication import registered_user
from backend.models.user import User
from backend.services.event import EventNotFoundException, EventService
from backend.models.event import Event, EventDetails
from backend.services.permission import UserPermissionException

api = APIRouter(prefix="/api/events")

@api.get("", tags=['Event'])
def get_events(event_service: EventService = Depends()) -> list[EventDetails]:
    """
    Get all events
    Returns:
        list[Event]: All `Event`s in the `Event` database table
    """

    # Return all events
    return event_service.all()

@api.get("/organization/{id}", tags=['Event'])
def get_events_from_organization_id(organization_id: int, event_service: EventService = Depends()) -> list[EventDetails]:
    """
    Get all events from an organization
    Returns:
        list[Event]: All `Event`s in the `Event` database table from a specific organization
    """

    # Return all events
    return event_service.get_events_from_organization_id(organization_id)

@api.post("", tags=['Event'])
def new_event(event: Event, subject: User = Depends(registered_user), event_service: EventService = Depends()) -> EventDetails:
    """
    Create event

    Parameters:
        event: a valid Event model
        event_service: a valid EventService

    Returns:
        Event: latest iteration of the created or updated event after changes made

    Raises:
        HTTPException 404 if create() raises an Exception
    """

    # Try to create event
    try:
        # Return created event
        return event_service.create(subject, event)
    except Exception as e:
        # Raise 422 exception if creation fails
        # - This would occur if the request body is shaped incorrectly
        raise HTTPException(status_code=422, detail=str(e))
    
@api.get("/{id}", responses={404: {"model": None}}, tags=['Event'])
def get_event_from_id(id: int, event_service: EventService = Depends()) -> EventDetails:
    """
    Get event with matching id

    Parameters:
        id: an int representing a unique event ID
        event_service: a valid EventService
    
    Returns:
        Event: Event with matching id
    
    Raises:
        HTTPException 404 if update() raises an Exception
    """
    
    # Try to get event with matching id
    try: 
        # Return event
        return event_service.get_from_id(id)
    except (EventNotFoundException, UserPermissionException) as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.put("", responses={404: {"model": None}}, tags=['Event'])
def update_event(event: Event, subject: User = Depends(registered_user), event_service: EventService = Depends()) -> EventDetails:
    """
    Update event

    Parameters:
        event: a valid Event model
        event_service: a valid EventService

    Returns:
        Event: Updated event

    Raises:
        HTTPException 404 if update() raises an Exception
    """

    try: 
        # Return updated event
        return event_service.update(subject, event)
    except (EventNotFoundException, UserPermissionException) as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['Event'])
def delete_event(id: int, subject: User = Depends(registered_user), event_service = Depends(EventService)):
    """
    Delete event based on id

    Parameters:
        id: an int representing a unique event ID
        event_service: a valid EventService
    
    Raises:
        HTTPException 404 if delete() raises an Exception
    """
   
    try:
        # Try to delete event
        event_service.delete(subject, id)
    except (EventNotFoundException, UserPermissionException) as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))