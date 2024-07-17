"""Application API

Application routes are used to create, retrieve, and update Applications."""

from fastapi import APIRouter, Depends

from typing import List

from backend.models.application import Application
from backend.services.application import ApplicationService

from ..api.authentication import registered_user
from ..models.user import User
from ..models.academics import CatalogSectionIdentity

__authors__ = ["Ajay Gandecha", "Ben Goulet", "Abdulaziz Al-Shayef"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


openapi_tags = {
    "name": "Applications",
    "description": "Create, update, delete, and retrieve TA Applications.",
}

api = APIRouter(prefix="/api/applications/ta")


@api.get("/user/:term_id", tags=["Applications"])
def get_application(
    term_id: str,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> Application | None:
    """Get a user's application"""

    return application_service.get_application(term_id, user)


@api.post("", tags=["Applications"])
def create_application(
    application: Application,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> Application:
    """Creates an application"""
    return application_service.create(user, application)


@api.put("", tags=["Applications"])
def update_undergrad_application(
    application: Application,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> Application:
    """
    Update application

    Parameters:
        application: a valid New_UTA model
        user: The user updating their application
        application_service: a valid ApplicationService

    Returns:
        Application: Created application

    Raises:
        ResourceNotFound if application doesn't exist
    """

    return application_service.update(user, application)


@api.delete("", response_model=None, tags={"Applications"})
def delete_application(
    application: Application,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
):
    """
    Delete Application

    Parameters:
        user: The user deleteing their application

    Returns:
        None

    Raises:
        ResourceNotFound if application doesn't exist
    """

    return application_service.delete(application.id, user)


@api.get(
    "/eligible-sections",
    response_model=list[CatalogSectionIdentity],
    tags=["Applications"],
)
def get_eligible_sections(
    application_service: ApplicationService = Depends(),
) -> list[CatalogSectionIdentity]:
    """
    Get sections that an applicant can apply to.

    Returns:
        list[CatalogSectionIdentity]: All sections.
    """

    # Return all applications
    return application_service.eligible_sections()
