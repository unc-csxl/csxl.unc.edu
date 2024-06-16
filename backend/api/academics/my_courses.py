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
