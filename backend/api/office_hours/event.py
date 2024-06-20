"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics.my_courses import MyCoursesService
from ...models.user import User
from ...models.office_hours.ticket import OfficeHoursTicketDraft

from ...models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourTicketOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours/event")


@api.get("/{oh_event_id}/queue", tags=["Office Hours"])
def get_oh_queue(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourQueueOverview:
    """
    Gets the queue overview for an office hour event.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.get_office_hour_queue(subject, oh_event_id)


@api.get("/{oh_event_id}/role", tags=["Office Hours"])
def get_oh_role(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourEventRoleOverview:
    """
    Gets a user's role for a given office hour event.

    Returns:
        OfficeHourEventRoleOverview
    """
    return my_courses_svc.get_oh_event_role(subject, oh_event_id)


@api.get("/{oh_event_id}/get-help", tags=["Office Hours"])
def get_oh_help(
    oh_event_id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourGetHelpOverview:
    """
    Gets information about getting help in office hours.

    Returns:
        OfficeHourGetHelpOverview
    """
    return my_courses_svc.get_office_hour_get_help_overview(subject, oh_event_id)
