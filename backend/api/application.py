"""Application API

Application routes are used to create, retrieve, and update Applications."""

from fastapi import APIRouter, Depends

from typing import List

from backend.models.application_details import (
    UTAApplicationDetails,
    NewUTAApplicationDetails,
)
from backend.services.application import ApplicationService

from ..api.authentication import registered_user
from ..models.user import User

__authors__ = ["Ben Goulet, Abdulaziz Al-Shayef"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


openapi_tags = {
    "name": "Applications",
    "description": "Create, update, delete, and retrieve TA Applications.",
}

api = APIRouter(prefix="/api/applications/ta")


@api.get("", response_model=list[NewUTAApplicationDetails], tags=["Applications"])
def get_applications(
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> list[UTAApplicationDetails]:
    """
    Get all applications

    Parameters:
        application_service: a valid ApplicationService

    Returns:
        list[Application]: All `Application`s in the `Application` database table
    """

    # Return all applications
    return application_service.list(user)


@api.get("/user", response_model=NewUTAApplicationDetails | None, tags=["Applications"])
def get_applications_user(
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> NewUTAApplicationDetails | None:
    """
    Get all applications

    Parameters:
        application_service: a valid ApplicationService

    Returns:
        list[Application]: All `Application`s in the `Application` database table
    """

    return application_service.get_application(user)


@api.post("", response_model=NewUTAApplicationDetails, tags=["Applications"])
def new_undergrad_application(
    application: NewUTAApplicationDetails,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> NewUTAApplicationDetails:
    """
    Create application

    Parameters:
        application: a valid New_UTA model
        application_service: a valid ApplicationService

    Returns:
        Application: Created application

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    return application_service.create_uta_application(user, application)


@api.put("/update", response_model=NewUTAApplicationDetails, tags=["Applications"])
def update_undergrad_application(
    application: NewUTAApplicationDetails,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> NewUTAApplicationDetails:
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

    return application_service.update_uta_application(user, application)


@api.delete("/delete", response_model=None, tags={"Applications"})
def delete_application(
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

    return application_service.delete_application(user)
