"""Event API

Event routes are used to create, retrieve, and update Events."""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from typing import Sequence
from backend.models.public_user import PublicUser
from backend.models.pagination import EventPaginationParams, Paginated, PaginationParams

from backend.services.organization import OrganizationService

from ...services.event import EventService
from ...services.user import UserService
from ...services.exceptions import ResourceNotFoundException, UserPermissionException
from ...models.event import EventDraft, EventOverview, EventStatusOverview
from ...models.coworking.time_range import TimeRange
from ...api.authentication import registered_user
from ...models.user import User

__authors__ = [
    "Ajay Gandecha",
    "Jade Keegan",
    "Brianna Ta",
    "Audrey Toney",
    "Kris Jordan",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/events")
openapi_tags = {
    "name": "Events",
    "description": "Create, update, delete, and retrieve CS Events.",
}


@api.get("/unauthenticated/paginate", tags=["Events"])
def list_events(
    event_service: EventService = Depends(),
    order_by: str = "time",
    ascending: str = "true",
    filter: str = "",
    range_start: str = "",
    range_end: str = "",
) -> Paginated[EventOverview]:
    """List events in time range via standard backend pagination query parameters."""

    pagination_params = EventPaginationParams(
        order_by=order_by,
        ascending=ascending,
        filter=filter,
        range_start=range_start,
        range_end=range_end,
    )
    return event_service.get_paginated_events(pagination_params, None)


@api.get("/paginate", tags=["Events"])
def list_events(
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
    order_by: str = "time",
    ascending: str = "true",
    filter: str = "",
    range_start: str = "",
    range_end: str = "",
) -> Paginated[EventOverview]:
    """List events in time range via standard backend pagination query parameters."""

    pagination_params = EventPaginationParams(
        order_by=order_by,
        ascending=ascending,
        filter=filter,
        range_start=range_start,
        range_end=range_end,
    )
    return event_service.get_paginated_events(pagination_params, subject)


@api.get("/unauthenticated/status", tags=["Events"])
def get_status(
    event_service: EventService = Depends(),
) -> EventStatusOverview:
    """Retrieves the featured event and user's registrations."""
    return event_service.get_event_status_unauthenticated()


@api.get("/status", tags=["Events"])
def get_status(
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventStatusOverview:
    """Retrieves the featured event and user's registrations."""
    return event_service.get_event_status(subject)


@api.get(
    "/{id}",
    responses={404: {"model": None}},
    tags=["Events"],
)
def get_event_by_id(
    id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventOverview:
    """
    Get event with matching id

    Args:
        id: an int representing a unique Event ID
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        EventDetails: a valid EventDetails model corresponding to the given event id
    """
    return event_service.get_by_id(id, subject)


@api.post("", tags=["Events"])
def new_event(
    event: EventDraft,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventOverview:
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


@api.put("", tags=["Events"])
def update_event(
    event: EventDraft,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> EventOverview:
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
) -> PublicUser:
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

    event: EventOverview = event_service.get_by_id(event_id, subject)
    return event_service.register(subject, user, event)


@api.get("/{event_id}/registration", tags=["Events"])
def get_event_registration_of_user(
    event_id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
) -> PublicUser:
    """
    Check the registration status of a user for an event, raise ResourceNotFound if unregistered.

    Args:
        event_id: the int identifier of an Event
        subject: the logged in user making the request
        event_service: the backing service
    """
    event: EventOverview = event_service.get_by_id(event_id, subject)
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
) -> Sequence[PublicUser]:
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
        subject, event_service.get_by_id(event_id, subject)
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

    event: EventOverview = event_service.get_by_id(event_id, subject)
    event_service.unregister(subject, user, event)


@api.get("/{event_id}/registrations/users", tags=["Events"])
def get_registered_users_of_event(
    event_id: int,
    subject: User = Depends(registered_user),
    event_service: EventService = Depends(),
    page: int = 0,
    page_size: int = 10,
    order_by: str = "first_name",
    filter: str = "",
) -> Paginated[User]:
    """
        List registered users for an event via standard backend pagination query parameters.

    Args:
        event_id: an int representing a unique Event
        subject: a valid User model representing the currently logged in User
        event_service: a valid EventService

    Returns:
        Paginated[User]: All `User`s registered for an event in Paginated form
    """
    try:
        pagination_params = PaginationParams(
            page=page, page_size=page_size, order_by=order_by, filter=filter
        )
        return event_service.get_registered_users_of_event(
            subject, event_id, pagination_params
        )
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
