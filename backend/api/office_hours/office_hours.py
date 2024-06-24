"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.office_hours.office_hours import OfficeHoursService
from ...models.user import User
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ...models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours")


@api.get("/{id}/queue", tags=["Office Hours"])
def get_office_hours_queue(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHourQueueOverview:
    """
    Gets the queue overview for an office hour event.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_event_svc.get_office_hour_queue(subject, id)


@api.get("/{id}/role", tags=["Office Hours"])
def get_office_hours_role(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHourEventRoleOverview:
    """
    Gets a user's role for a given office hour event.

    Returns:
        OfficeHourEventRoleOverview
    """
    return oh_event_svc.get_oh_event_role(subject, id)


@api.get("/{id}/get-help", tags=["Office Hours"])
def get_office_hours_help(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHourGetHelpOverview:
    """
    Gets information about getting help in office hours.

    Returns:
        OfficeHourGetHelpOverview
    """
    return oh_event_svc.get_office_hour_get_help_overview(subject, id)


@api.post("/{site_id}", tags=["Office Hours"])
def create_office_hours(
    site_id: int,
    oh: NewOfficeHours,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHours:
    """
    Creates new office hours.

    Returns:
        OfficeHours
    """
    return oh_event_svc.create(subject, site_id, oh)


@api.put("/{site_id}", tags=["Office Hours"])
def update_office_hours(
    site_id: int,
    oh: OfficeHours,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHours:
    """
    Updates new office hours.

    Returns:
        OfficeHours
    """
    return oh_event_svc.update(subject, site_id, oh)


@api.delete("/{site_id}/{oh_id}", tags=["Office Hours"])
def delete_office_hours(
    site_id: int,
    oh_id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
):
    """
    Deletes office hours.
    """
    oh_event_svc.delete(subject, site_id, oh_id)


@api.get("/{site_id}/{oh_id}", tags=["Office Hours"])
def get_office_hours(
    site_id: int,
    oh_id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHours:
    """
    Gets office hours.
    """
    return oh_event_svc.get(subject, site_id, oh_id)
