"""My Courses API

APIs relative to a specific user."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics.my_courses import MyCoursesService
from ...models.user import User
from ...models.academics.my_courses import OfficeHoursTicketDraft

from ...models.academics.my_courses import (
    TermOverview,
    CourseMemberOverview,
    CourseOfficeHourEventOverview,
    OfficeHourQueueOverview,
    OfficeHourTicketOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)
from ...models.pagination import PaginationParams, Paginated

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/academics/my-courses")


@api.get("", tags=["My Courses"])
def get_user_courses(
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> list[TermOverview]:
    """
    Get the courses for the current user organized by term.

    Returns:
        list[TermOverview]
    """
    return my_courses_svc.get_user_courses(subject)


@api.get("/{term_id}/{course_id}/roster", tags=["My Courses"])
def get_course_roster(
    term_id: str,
    course_id: str,
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> Paginated[CourseMemberOverview]:
    """
    Get the roster overview for a course.

    Returns:
        CourseRosterOverview
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return my_courses_svc.get_course_roster(
        subject, term_id, course_id, pagination_params
    )


@api.get("/{term_id}/{course_id}/oh-events/current", tags=["Office Hours"])
def get_current_oh_events(
    term_id: str,
    course_id: str,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> list[CourseOfficeHourEventOverview]:
    """
    Gets the current office hour event overviews for a given class.

    Returns:
        list[CourseOfficeHourEventOverview]
    """
    return my_courses_svc.get_current_office_hour_events(subject, term_id, course_id)


@api.get("/{term_id}/{course_id}/oh-events/future", tags=["Office Hours"])
def get_future_oh_events(
    term_id: str,
    course_id: str,
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> Paginated[CourseOfficeHourEventOverview]:
    """
    Gets the future office hour event overviews for a given class.

    Returns:
        Paginated[CourseOfficeHourEventOverview]
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return my_courses_svc.get_future_office_hour_events(
        subject, term_id, course_id, pagination_params
    )


@api.get("/{term_id}/{course_id}/oh-events/history", tags=["Office Hours"])
def get_past_oh_events(
    term_id: str,
    course_id: str,
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> Paginated[CourseOfficeHourEventOverview]:
    """
    Gets the past office hour event overviews for a given class.

    Returns:
        Paginated[CourseOfficeHourEventOverview]
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return my_courses_svc.get_past_office_hour_events(
        subject, term_id, course_id, pagination_params
    )


@api.get("/oh-events/{oh_event_id}/queue", tags=["Office Hours"])
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


@api.put("/oh-events/ticket/{ticket_id}/call", tags=["Office Hours"])
def call_ticket(
    ticket_id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Calls a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.call_ticket(subject, ticket_id)


@api.put("/oh-events/ticket/{ticket_id}/cancel", tags=["Office Hours"])
def cancel_ticket(
    ticket_id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Cancels a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.cancel_ticket(subject, ticket_id)


@api.put("/oh-events/ticket/{ticket_id}/close", tags=["Office Hours"])
def close_ticket(
    ticket_id: int,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Closes a ticket in an office hour queue.

    Returns:
        OfficeHourQueueOverview
    """
    return my_courses_svc.close_ticket(subject, ticket_id)


@api.get("/oh-events/{oh_event_id}/role", tags=["Office Hours"])
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


@api.get("/oh-events/{oh_event_id}/get-help", tags=["Office Hours"])
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


@api.post("/oh-events/ticket/", tags=["Office Hours"])
def new_oh_ticket(
    oh_ticket: OfficeHoursTicketDraft,
    subject: User = Depends(registered_user),
    my_courses_svc: MyCoursesService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Adds a new OH ticket to the database

    Returns:
        OfficeHoursTicketDetails: OH Ticket created
    """
    return my_courses_svc.create_ticket(subject, oh_ticket)
