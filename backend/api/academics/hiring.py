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
from ...models.academics.hiring.conflict_check import ConflictCheck

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


@api.get("/admin/course/{course_site_id}", tags=["Hiring"])
def get_hiring_admin_course_overview(
    course_site_id: int,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringAdminCourseOverview:
    """
    Returns the state of hiring to the admin.
    """
    return hiring_service.get_hiring_admin_course_overview(subject, course_site_id)


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


@api.post("/create_sites", tags=["Hiring"])
def create_missing_course_sites_for_term(
    term_id: str,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> bool:
    """
    Creates missing course sites for the term
    """
    return hiring_service.create_missing_course_sites_for_term(subject, term_id)


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
    page_size: int = 100,
    order_by: str = "",
    filter: str = "",
    flagged: HiringAssignmentFlagFilter = HiringAssignmentFlagFilter.ALL,
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
        subject, term_id, flagged, pagination_params
    )


@api.get("/summary/{term_id}/csv", tags=["Hiring"])
def get_hiring_summary_csv(
    term_id: str,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> StreamingResponse:
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
    wr = csv.DictWriter(stream, delimiter=",", fieldnames=list(data[0].__dict__.keys()))
    wr.writeheader()
    wr.writerows([d.__dict__ for d in data])
    # Create HTTP response of type `text/csv`
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    # Return the response
    return response


@api.get("/{course_site_id}/csv", tags=["Hiring"])
def get_applicants_for_site_csv(
    course_site_id: int,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> StreamingResponse:
    """
    Returns the state of hiring as a summary.
    """
    # Get the data
    data = hiring_service.get_course_site_hiring_status_csv(subject, course_site_id)
    # Create IO Stream
    stream = io.StringIO()
    # Create dictionary writer to convert objects to CSV rows
    # Note: __dict__ converts the Pydantic model into a dictionary of key-value
    # pairs, enabling access of the object's keys.
    wr = csv.DictWriter(stream, delimiter=",", fieldnames=list(data[0].__dict__.keys()))
    wr.writeheader()
    wr.writerows([d.__dict__ for d in data])
    # Create HTTP response of type `text/csv`
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    # Return the response
    return response


@api.get("/summary/{term_id}/phd_applicants", tags=["Hiring"])
def get_phd_applicants_csv(
    term_id: str,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> StreamingResponse:
    """
    Returns the state of hiring as a summary.
    """
    data = hiring_service.get_phd_applicants(subject, term_id)
    # Create IO Stream
    stream = io.StringIO()
    # Create dictionary writer to convert objects to CSV rows
    # Note: __dict__ converts the Pydantic model into a dictionary of key-value
    # pairs, enabling access of the object's keys.
    keys = [
        "id",
        "last_name",
        "first_name",
        "pid",
        "onyen",
        "email",
        "advisor",
        "program_pursued",
        "intro_video_url",
        "student_preferences",
        "instructor_preferences",
    ]
    wr = csv.DictWriter(stream, delimiter=",", fieldnames=keys)
    wr.writeheader()
    rows = []
    for d in data:
        rows.append(
            {
                "id": d.id,
                "last_name": d.applicant.last_name,
                "first_name": d.applicant.first_name,
                "pid": d.applicant.pid,
                "onyen": d.applicant.onyen,
                "email": d.applicant.email,
                "advisor": d.advisor,
                "program_pursued": d.program_pursued,
                "intro_video_url": d.intro_video_url,
                "student_preferences": ", ".join(d.student_preferences),
                "instructor_preferences": ", ".join(d.instructor_preferences),
            }
        )
    wr.writerows(rows)
    # Create HTTP response of type `text/csv`
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = (
        f"attachment; filename=phd_applicants_{term_id}.csv"
    )
    # Return the response
    return response


@api.get("/assignments/{course_site_id}", tags=["Hiring"])
def get_hiring_assignments_for_course_site(
    course_site_id: int,
    page: int = 0,
    page_size: int = 25,
    order_by: str = "",
    filter: str = "",
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> Paginated[HiringAssignmentOverview]:
    """Retrieves the committed and final hiring assignments for a course site."""
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return hiring_service.get_hiring_assignments_for_course_site(
        subject, course_site_id, pagination_params
    )


@api.get("/assignments/{course_site_id}/csv", tags=["Hiring"])
def get_assignments_csv(
    course_site_id: int,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> StreamingResponse:
    """
    Returns the state of hiring as a summary.
    """
    data = hiring_service.get_assignment_summary_for_instructors_csv(
        subject, course_site_id
    )
    # Create IO Stream
    stream = io.StringIO()
    # Create dictionary writer to convert objects to CSV rows
    # Note: __dict__ converts the Pydantic model into a dictionary of key-value
    # pairs, enabling access of the object's keys.
    keys = ["first_name", "last_name", "onyen", "pid", "email", "level_title"]

    wr = csv.DictWriter(stream, delimiter=",", fieldnames=keys)
    wr.writeheader()
    rows = []
    for d in data:
        rows.append(
            {
                "first_name": d.first_name,
                "last_name": d.last_name,
                "pid": d.pid,
                "onyen": d.onyen,
                "email": d.email,
                "level_title": d.level_title,
            }
        )
    wr.writerows(rows)
    # Create HTTP response of type `text/csv`
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = (
        f"attachment; filename=hiring_assignments.csv"
    )
    # Return the response
    return response


@api.get("/conflict_check/{application_id}", tags=["Hiring"])
def conflict_check(
    application_id: int,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> ConflictCheck:
    return hiring_service.conflict_check(subject, application_id)


# New: applicants export for a term (streaming)
@api.get("/admin/{term_id}/csv", tags=["Hiring"])
def get_applicants_for_term_csv(
    term_id: str,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> StreamingResponse:
    """Stream a CSV of all applicants for a term."""
    fieldnames = [
        "type",
        "assignments",
        "first_name",
        "last_name",
        "pid",
        "email",
        "pronouns",
        "program_pursued",
        "comp_227",
        "intro_video_url",
        "prior_experience",
        "advisor",
        "preferred_sections",
        "instructor_selections",
    ]

    def row_iter():
        # header
        header_buf = io.StringIO()
        header_writer = csv.DictWriter(header_buf, delimiter=",", fieldnames=fieldnames)
        header_writer.writeheader()
        yield header_buf.getvalue()
        # rows
        for row in hiring_service.iter_applicants_for_term_csv(subject, term_id):
            buf = io.StringIO()
            writer = csv.DictWriter(buf, delimiter=",", fieldnames=fieldnames)
            writer.writerow(row)
            yield buf.getvalue()

    response = StreamingResponse(row_iter(), media_type="text/csv")
    response.headers["Content-Disposition"] = (
        f"attachment; filename=applicants_{term_id}.csv"
    )
    return response
