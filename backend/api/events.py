"""Event API

Event routes are used to create, retrieve, and update Events."""

from fastapi import APIRouter, Depends, HTTPException

from ..services.event import EventService
from ..services.user import UserService
from ..models.event import Event
from ..models.event_details import EventDetails
from ..models.event_registration import EventRegistration
from ..api.authentication import registered_user
from ..models.user import User

__authors__ = [
    "Ajay Gandecha",
    "Jade Keegan",
    "Brianna Ta",
    "Audrey Toney",
    "Kris Jordan",
]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/events")
openapi_tags = {
    "name": "Events",
    "description": "Create, update, delete, and retrieve CS Events.",
}


@api.get("", response_model=list[EventDetails], tags=["Events"])
def get_events(event_service: EventService = Depends()) -> list[EventDetails]:
    """
    Get all events

    Returns:
        list[Event]: All `Event`s in the `Event` database table
    """
    return event_service.all()


@api.get("/organization/{slug}", response_model=list[EventDetails], tags=["Events"])
def get_events_from_organization(
    slug: str, event_service: EventService = Depends()
) -> list[EventDetails]:
    """
    Get all events from an organization

    Parameters:
        slug: a valid str representing a unique Organization
        event_service: a valid EventService

    Returns:
        list[EventDetails]: All `EventDetails`s in the `Event` database table from a specific organization
    """
    return event_service.get_events_from_organization(slug)


@api.post("", response_model=EventDetails, tags=["Events"])
def new_event(
    event: Event,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventDetails:
    """
    Create event

    Parameters:
        event: a valid Event model
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        EventDetails: latest iteration of the created or updated event after changes made
    """
    return event_service.create(subject, event)


@api.get(
    "/{id}",
    responses={404: {"model": None}},
    response_model=EventDetails,
    tags=["Events"],
)
def get_event_from_id(id: int, event_service: EventService = Depends()) -> EventDetails:
    """
    Get event with matching id

    Parameters:
        id: an int representing a unique Event ID
        event_service: a valid EventService

    Returns:
        EventDetails: a valid EventDetails model corresponding to the given event id
    """
    return event_service.get_by_id(id)


@api.put(
    "", responses={404: {"model": None}}, response_model=EventDetails, tags=["Events"]
)
def update_event(
    event: EventDetails,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventDetails:
    """
    Update event

    Parameters:
        event: a valid Event model
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        EventDetails: a valid EventDetails model representing the updated Event
    """
    return event_service.update(subject, event)


@api.delete("/{id}", tags=["Events"])
def delete_event(
    id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
):
    """
    Delete event based on id

    Parameters:
        id: an int representing a unique event ID
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService
    """
    event_service.delete(subject, id)


@api.post("/register/{event_id}", tags=["Events"])
def register_for_event(
    event_id: int,
    user_id: int = -1,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
    user_service: UserService = Depends(),
) -> EventRegistration:
    """
    Register a user event based on the event ID.

    If the user_id parameter is not passed to the post method, we will use the
    logged in user's ID as the user_id. Another user's ID is expected when a
    user is being registered by an administrator.

    Args:
        event_id: an int representing a unique event ID
        user_id: (optional) an int representing the user being registered for an event
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService
    """
    if user_id == -1 and subject.id is not None:
        user = subject
    else:
        user = user_service.get_by_id(user_id)

    event = event_service.get_by_id(event_id)
    return event_service.register(subject, user, event)


@api.delete("/register/{event_id}", tags=["Events"])
def unregister_for_event(
    event_id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
):
    """
    Unregister a user event based on the event ID

    Parameters:
        id: an int representing a unique event ID
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService
    """
    event_service.unregister(subject, event_id)
