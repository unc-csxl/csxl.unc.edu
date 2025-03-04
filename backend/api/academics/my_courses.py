"""My Courses API

APIs relative to a specific user."""

import json
from fastapi import APIRouter, Depends

from backend.models.office_hours.ticket_statistics import OfficeHoursTicketStatistics
from ..authentication import registered_user
from ...services.academics.course_site import CourseSiteService
from ...services.office_hours.office_hours_statistics import (
    OfficeHoursStatisticsService,
)
from ...models.user import User

from ...models.academics.my_courses import (
    TermOverview,
    CourseMemberOverview,
    OfficeHoursOverview,
    CourseSiteOverview,
    OfficeHourTicketOverview,
)
from ...models.office_hours.course_site import (
    NewCourseSite,
    CourseSite,
    UpdatedCourseSite,
)
from ...models.office_hours.course_site_details import CourseSiteDetails
from ...models.pagination import PaginationParams, Paginated, TicketPaginationParams

__authors__ = ["Kris Jordan", "Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/my-courses")
openapi_tags = {
    "name": "My Courses",
    "description": "Curates data necessary for the My Courses page.",
}


@api.get("", tags=["My Courses"])
def get_user_courses(
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> list[TermOverview]:
    """
    Get the courses for the current user organized by term.

    Returns:
        list[TermOverview]
    """
    return course_site_svc.get_user_course_sites(subject)


@api.get("/{course_site_id}", tags=["My Courses"])
def get_course_site(
    course_site_id: int,
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> UpdatedCourseSite:
    """
    Gets the current office hour event overviews for a given class.

    Returns:
        list[OfficeHoursOverview]
    """
    return course_site_svc.get(subject, course_site_id)


@api.get("/{course_site_id}/roster", tags=["My Courses"])
def get_course_site_roster(
    course_site_id: int,
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> Paginated[CourseMemberOverview]:
    """
    Get the roster overview for a course.

    Returns:
        CourseRosterOverview
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return course_site_svc.get_course_site_roster(
        subject, course_site_id, pagination_params
    )


@api.get("/{course_site_id}/oh-events/current", tags=["My Courses"])
def get_current_oh_events(
    course_site_id: int,
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> list[OfficeHoursOverview]:
    """
    Gets the current office hour event overviews for a given class.

    Returns:
        list[OfficeHoursOverview]
    """
    return course_site_svc.get_current_office_hour_events(subject, course_site_id)


@api.get("/{course_site_id}/oh-events/future", tags=["My Courses"])
def get_future_oh_events(
    course_site_id: int,
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> Paginated[OfficeHoursOverview]:
    """
    Gets the future office hour event overviews for a given class.

    Returns:
        Paginated[OfficeHoursOverview]
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return course_site_svc.get_future_office_hour_events(
        subject, course_site_id, pagination_params
    )


@api.get("/{course_site_id}/oh-events/history", tags=["My Courses"])
def get_past_oh_events(
    course_site_id: int,
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> Paginated[OfficeHoursOverview]:
    """
    Gets the past office hour event overviews for a given class.

    Returns:
        Paginated[OfficeHoursOverview]
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return course_site_svc.get_past_office_hour_events(
        subject, course_site_id, pagination_params
    )


@api.post("/new", tags=["My Courses"])
def create_course_site(
    course_site: NewCourseSite,
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> CourseSite:
    """
    Adds a new course site to the database

    Returns:
        CourseSiteDetails: Course created
    """
    return course_site_svc.create(subject, course_site)


@api.put("", tags=["My Courses"])
def update_course_site(
    course_site: UpdatedCourseSite,
    subject: User = Depends(registered_user),
    course_site_svc: CourseSiteService = Depends(),
) -> CourseSite:
    """
    Updates a course site to the database

    Returns:
        CourseSite: Course updated
    """
    return course_site_svc.update(subject, course_site)


@api.get("/{course_site_id}/statistics", tags=["My Courses"])
def get_ticket_statistics(
    course_site_id: int,
    student_ids: str = "",
    staff_ids: str = "",
    range_start: str = "",
    range_end: str = "",
    subject: User = Depends(registered_user),
    oh_statistics_svc: OfficeHoursStatisticsService = Depends(),
) -> OfficeHoursTicketStatistics:
    """
    Gets the ticket statistics for a given class.

    Returns:
        OfficeHoursTicketStatistics
    """

    ticket_statistics_params = TicketPaginationParams(
        student_ids=json.loads(student_ids) if len(student_ids) > 0 else [],
        staff_ids=json.loads(staff_ids) if len(staff_ids) > 0 else [],
        range_start=range_start,
        range_end=range_end,
    )

    return oh_statistics_svc.get_statistics(
        subject, course_site_id, ticket_statistics_params
    )


@api.get("/{course_site_id}/statistics/ticket-history", tags=["My Courses"])
def get_paginated_ticket_history(
    course_site_id: int,
    page: int = 0,
    page_size: int = 10,
    student_ids: str = "",
    staff_ids: str = "",
    range_start: str = "",
    range_end: str = "",
    subject: User = Depends(registered_user),
    oh_statistics_svc: OfficeHoursStatisticsService = Depends(),
) -> Paginated[OfficeHourTicketOverview]:
    """
    Gets the past office hour event overviews for a given class.

    Returns:
        Paginated[OfficeHoursOverview]
    """

    ticket_pagination_params = TicketPaginationParams(
        page=page,
        page_size=page_size,
        student_ids=json.loads(student_ids) if len(student_ids) > 0 else [],
        staff_ids=json.loads(staff_ids) if len(staff_ids) > 0 else [],
        range_start=range_start,
        range_end=range_end,
    )

    return oh_statistics_svc.get_paginated_tickets(
        subject, course_site_id, ticket_pagination_params
    )
