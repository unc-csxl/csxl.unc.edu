"""Hiring API

Hiring routes are used for hiring based on TA Applications."""

from fastapi import APIRouter, Depends

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
) -> HiringAssignmentOverview:
    """
    Creates a new level
    """
    return hiring_service.create_hiring_level(subject, level)


@api.put("/level", tags=["Hiring"])
def update_hiring_level(
    level: HiringLevel,
    subject: User = Depends(registered_user),
    hiring_service: HiringService = Depends(),
) -> HiringAssignmentOverview:
    """
    Updates a level
    """
    return hiring_service.update_hiring_level(subject, level)
