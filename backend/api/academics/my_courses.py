"""My Courses API

APIs relative to a specific user."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics.my_courses import MyCoursesService
from ...models.user import User
from ...models.academics.my_courses import (
    TermOverview,
    CourseMemberOverview,
    CourseOfficeHourEventOverview,
    OfficeHourQueueOverview,
    OfficeHourTicketOverview,
)
from ...models.pagination import PaginationParams, Paginated

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/academics/my-courses")


@api.get("", tags=["Academics"])
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


@api.get("/{term_id}/{course_id}/roster", tags=["Academics"])
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


@api.get("/{term_id}/{course_id}/oh-events/current", tags=["Academics"])
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


@api.get("/{term_id}/{course_id}/oh-events/future", tags=["Academics"])
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


@api.get("/{term_id}/{course_id}/oh-events/history", tags=["Academics"])
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


@api.get("/oh-events/{oh_event_id}/queue", tags=["Academics"])
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


@api.put("/oh-events/ticket/{ticket_id}/call", tags=["Academics"])
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


@api.put("/oh-events/ticket/{ticket_id}/cancel", tags=["Academics"])
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


@api.put("/oh-events/ticket/{ticket_id}/close", tags=["Academics"])
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
