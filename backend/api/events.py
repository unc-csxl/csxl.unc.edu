"""Event API

Event routes are used to create, retrieve, and update Events."""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from typing import Sequence

from ..services.event import EventService
from ..services.user import UserService
from ..services.exceptions import ResourceNotFoundException
from ..models.event import Event
from ..models.event_details import EventDetails
from ..models.event_registration import EventRegistration, EventRegistrationStatus
from ..models.coworking.time_range import TimeRange
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
def get_events_by_organization(
    slug: str, event_service: EventService = Depends()
) -> list[EventDetails]:
    """
    Get all events from an organization

    Args:
        slug: a valid str representing a unique Organization
        event_service: a valid EventService

    Returns:
        list[EventDetails]: All `EventDetails`s in the `Event` database table from a specific organization
    """
    return event_service.get_events_by_organization(slug)


@api.post("", response_model=EventDetails, tags=["Events"])
def new_event(
    event: Event,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventDetails:
    """
    Create event

    Args:
        event: a valid Event model
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        EventDetails: latest iteration of the created or updated event after changes made
    """
    return event_service.create(subject, event)


@api.get("/registrations", tags=["Events"])
def get_registrations_of_user(
    subject: User = Depends(registered_user),
    user_id: int = -1,
    start: datetime | None = None,
    end: datetime | None = None,
    event_svc: EventService = Depends(),
    user_svc: UserService = Depends(),
) -> Sequence[EventRegistration]:
    """
    Get a user's event registrations.

    Args:
        subject (User) the registered User making the request
        user_id (int) optional parameter for reading another user's registrations
        start (datetime) optional parameter for specifying start time range of search. Defaults to now.
        end (datetime) optional parameter for specifying end time range of search. Defaults to a year from now.
        event_svc (EventService)
        user_svc (UserService)

    Returns:
        Sequence[EventRegistration]

    Raises:
        UserPermissionException if subject is requesting another user's event registrations but does not have permission.
    """
    user: User
    if user_id == -1:
        user = subject
    else:
        user = user_svc.get_by_id(user_id)

    start = datetime.now() if start is None else start
    end = datetime.now() + timedelta(days=365) if end is None else end
    time_range = TimeRange(start=start, end=end)

    return event_svc.get_registrations_of_user(subject, user, time_range)


@api.get(
    "/{id}",
    responses={404: {"model": None}},
    response_model=EventDetails,
    tags=["Events"],
)
def get_event_by_id(id: int, event_service: EventService = Depends()) -> EventDetails:
    """
    Get event with matching id

    Args:
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

    Args:
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

    Args:
        id: an int representing a unique event ID
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService
    """
    event_service.delete(subject, id)


@api.post("/{event_id}/registration", tags=["Events"])
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

    Returns:
        EventRegistration details
    """
    if user_id == -1 and subject.id is not None:
        user = subject
    else:
        user = user_service.get_by_id(user_id)

    event: EventDetails = event_service.get_by_id(event_id)
    return event_service.register(subject, user, event)


@api.get("/{event_id}/registration", tags=["Events"])
def get_event_registration_of_user(
    event_id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventRegistration:
    """
    Check the registration status of a user for an event, raise ResourceNotFound if unregistered.

    Args:
        event_id: the int identifier of an Event
        subject: the logged in user making the request
        event_service: the backing service
    """
    event: EventDetails = event_service.get_by_id(event_id)
    event_registration = event_service.get_registration(subject, subject, event)
    if event_registration is None:
        raise ResourceNotFoundException("You are not registered for this event")
    else:
        return event_registration


@api.get("/{event_id}/registrations", tags=["Events"])
def get_event_registrations(
    event_id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> Sequence[EventRegistration]:
    """
    Get the registrations of an event.

    Args:
        event_id: the int identifier of an Event
        subject: the logged in user making the request
        event_service: the backing service

    Returns:
        Sequence[EventRegistration]
    """
    return event_service.get_registrations_of_event(
        subject, event_service.get_by_id(event_id)
    )


@api.delete("/{event_id}/registration", tags=["Events"])
def unregister_for_event(
    event_id: int,
    user_id: int = -1,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
    user_service: UserService = Depends(),
):
    """
    Unregister a user event based on the event ID

    Args:
        event_id: an int representing a unique event ID
        user_id: the int of the user whose registration is being deleted (optional)
        subject: a valid User model representing the currently logged in User
        event_service: EventService
        user_service: UserService
    """
    if user_id == -1 and subject.id is not None:
        user = subject
    else:
        user = user_service.get_by_id(user_id)

    event: EventDetails = event_service.get_by_id(event_id)
    event_service.unregister(subject, user, event)


@api.get(
    "/{event_id}/registration/count",
    responses={404: {"model": None}},
    response_model=EventRegistrationStatus,
    tags=["Events"],
)
def get_event_registration_status(
    event_id: int, event_service: EventService = Depends()
) -> EventRegistrationStatus:
    """
    Get the number of event registrations for a given ID

    Args:
        id: an int representing a unique Event ID
        event_service: a valid EventService

    Returns:
        EventDetails: a valid EventDetails model corresponding to the given event id
    """
    return event_service.get_event_registration_status(event_id)
