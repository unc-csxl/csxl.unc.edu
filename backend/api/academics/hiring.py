"""Hiring API

Hiring routes are used for hiring based on TA Applications."""

from fastapi import APIRouter, Depends

from ...services.academics import HiringService

from ...models.academics.hiring.application_review import HiringStatus

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
