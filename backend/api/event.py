from fastapi import APIRouter, Depends, HTTPException
from ..services.event import EventService
from ..models.event import Event
from ..models.event_detail import EventDetail
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
def new_event(event: Event, event_service: EventService = Depends(),
              user_service: UserService = Depends(),
              token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())) -> EventDetail:
    """
    Create event
    Returns:
        EventDetail: Latest iteration of the created or updated event after changes made
    """

    # Try to create event
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM]
            )
            user = user_service.get(auth_info['pid'])
            if user:
                org_roles = [org_role for org_role in user.organization_associations if
                             org_role.org_id == event.org_id and org_role.membership_type > 0]
                if(len(org_roles) <=0):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                try:
                    # Return created event
                    return event_service.create(event)
                except Exception as e:
                    # Raise 422 exception if creation fails
                    # - This would occur if the request body is shaped incorrectly
                    raise HTTPException(status_code=422, detail=str(e))
        except:
            ...
    raise HTTPException(status_code=401, detail='Unauthorized')

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
def update_event(event: EventDetail, event_service: EventService = Depends(),
              user_service: UserService = Depends(),
              token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())) -> EventDetail:
    """
    Update event
    Returns:
        EventDetail: Updated event
    """
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM]
            )
            user = user_service.get(auth_info['pid'])
            if user:
                org_roles = [org_role for org_role in user.organization_associations if
                             org_role.org_id == event.org_id and org_role.membership_type > 0]
                if(len(org_roles) <=0):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                # Try to update event
                try: 
                    # Return updated event
                    return event_service.update(event)
                except Exception as e:
                    # Raise 404 exception if search fails
                    # - This would occur if there is no response
                    raise HTTPException(status_code=404, detail=str(e))
        except:
            ...
    raise HTTPException(status_code=401, detail='Unauthorized')

@api.delete("/{id}", tags=['Event'])
def delete_event(id: int, event_service = Depends(EventService),
              user_service: UserService = Depends(),
              token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())):
    """
    Delete event based on id
    """
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM]
            )
            user = user_service.get(auth_info['pid'])
            if user:
                event = event_service.get_from_id(id)
                org_roles = [org_role for org_role in user.organization_associations if
                             org_role.org_id == event.org_id and org_role.membership_type > 0]
                if(len(org_roles) <=0):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                # Try to update event
                # Try to delete event
                try:
                    # Return deleted event
                    return event_service.delete(id)
                except Exception as e:
                    # Raise 404 exception if search fails
                    # - This would occur if there is no response or if item to delete does not exist
                    raise HTTPException(status_code=404, detail=str(e))
        except:
            ...
    raise HTTPException(status_code=401, detail='Unauthorized')