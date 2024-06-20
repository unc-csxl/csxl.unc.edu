"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.office_hours.event import OfficeHourEventService
from ...models.user import User

from ...models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours/event")


@api.get("/{id}/queue", tags=["Office Hours"])
def get_oh_queue(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHourEventService = Depends(),
) -> OfficeHourQueueOverview:
    """
    Gets the queue overview for an office hour event.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_event_svc.get_office_hour_queue(subject, id)


@api.get("/{id}/role", tags=["Office Hours"])
def get_oh_role(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHourEventService = Depends(),
) -> OfficeHourEventRoleOverview:
    """
    Gets a user's role for a given office hour event.

    Returns:
        OfficeHourEventRoleOverview
    """
    return oh_event_svc.get_oh_event_role(subject, id)


@api.get("/{id}/get-help", tags=["Office Hours"])
def get_oh_help(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHourEventService = Depends(),
) -> OfficeHourGetHelpOverview:
    """
    Gets information about getting help in office hours.

    Returns:
        OfficeHourGetHelpOverview
    """
    return oh_event_svc.get_office_hour_get_help_overview(subject, id)
