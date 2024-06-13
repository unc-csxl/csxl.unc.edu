"""My Courses API

APIs relative to a specific user."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics.my_courses import MyCoursesService
from ...models.user import User
from ...models.academics.my_courses import TermOverview, CourseRosterOverview
from ...models.pagination import PaginationParams

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
) -> CourseRosterOverview:
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
