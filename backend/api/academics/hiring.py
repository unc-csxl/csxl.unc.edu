"""Hiring API

Hiring routes are used for hiring based on TA Applications."""

from fastapi import APIRouter, Depends
import io
import csv
from fastapi.responses import StreamingResponse

from backend.models.pagination import Paginated, PaginationParams

from ...services.academics import HiringService

from ...models.academics.hiring.application_review import HiringStatus
from ...models.academics.hiring.hiring_assignment import *
from ...models.academics.hiring.hiring_level import *

from ...api.authentication import registered_user
from ...models.user import User

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/hiring")

openapi_tags = {
    "name": "Hiring",
    "description": "View and update the hiring status for a course site.",
}


@api.get("/admin/{term_id}", tags=["Hiring"])
def get_hiring_admin_overview(
    term_id: str,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringAdminOverview:
    """
    Returns the state of hiring to the admin.
    """
    return hiring_service.get_hiring_admin_overview(subject, term_id)


@api.post("/assignment", tags=["Hiring"])
def create_hiring_assignment(
    assignment: HiringAssignmentDraft,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringAssignmentOverview:
    """
    Creates a new assignment
    """
    return hiring_service.create_hiring_assignment(subject, assignment)


@api.put("/assignment", tags=["Hiring"])
def update_hiring_assignment(
    assignment: HiringAssignmentDraft,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringAssignmentOverview:
    """
    Updates an assignment
    """
    return hiring_service.update_hiring_assignment(subject, assignment)


@api.delete("/assignment/{assignment_id}", tags=["Hiring"])
def delete_hiring_assignment(
    assignment_id: int,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringAssignmentOverview:
    """
    Deletes an assignment
    """
    return hiring_service.delete_hiring_assignment(subject, assignment_id)


@api.get("/level", tags=["Hiring"])
def get_hiring_levels(
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> list[HiringLevel]:
    """
    Get all hiring levels
    """
    return hiring_service.get_hiring_levels(subject)


@api.post("/level", tags=["Hiring"])
def create_hiring_level(
    level: HiringLevel,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringLevel:
    """
    Creates a new level
    """
    return hiring_service.create_hiring_level(subject, level)


@api.put("/level", tags=["Hiring"])
def update_hiring_level(
    level: HiringLevel,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringLevel:
    """
    Updates a level
    """
    return hiring_service.update_hiring_level(subject, level)


@api.get("/{course_site_id}", tags=["Hiring"])
def get_status(
    course_site_id: int,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringStatus:
    """
    Retrieves the hiring status for TA Applications.
    """
    return hiring_service.get_status(subject, course_site_id)


@api.put("/{course_site_id}", tags=["Hiring"])
def update_status(
    course_site_id: int,
    hiring_status: HiringStatus,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringStatus:
    """
    Updates the hiring status for TA Applications.
    """
    return hiring_service.update_status(subject, course_site_id, hiring_status)


@api.get("/summary/{term_id}", tags=["Hiring"])
def get_hiring_summary_overview(
    term_id: str,
    page: int = 0,
    page_size: int = 25,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> Paginated[HiringAssignmentSummaryOverview]:
    """
    Returns the state of hiring as a summary.
    """
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return hiring_service.get_hiring_summary_overview(
        subject, term_id, pagination_params
    )


@api.get("/summary/{term_id}/csv", tags=["Hiring"])
def get_hiring_summary_csv(
    term_id: str,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> Paginated[HiringAssignmentSummaryOverview]:
    """
    Returns the state of hiring as a summary.
    """
    # Get the data
    data = hiring_service.get_hiring_summary_for_csv(subject, term_id)
    # Create IO Stream
    stream = io.StringIO()
    # Create dictionary writer to convert objects to CSV rows
    # Note: __dict__ converts the Pydantic model into a dictionary of key-value
    # pairs, enabling access of the object's keys.
    wr = csv.DictWriter(
        stream, delimiter="\t", fieldnames=list(data[0].__dict__.keys())
    )
    wr.writeheader()
    wr.writerows([d.__dict__ for d in data])
    # Create HTTP response of type `text/csv`
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    # Return the response
    return response
