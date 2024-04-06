"""Application API

Application routes are used to create, retrieve, and update Applications."""

from fastapi import APIRouter, Depends

from typing import List

from backend.models.application import Application, New_UTA
from backend.models.application_details import New_UTADetails, UserApplication
from backend.services.application import ApplicationService

from ..api.authentication import registered_user
from ..models.user import User

__authors__ = ["Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


openapi_tags = {
    "name": "Applications",
    "description": "Create, update, delete, and retrieve TA Applications.",
}

api = APIRouter(prefix="/api/applications")


@api.get("", response_model=list[New_UTADetails], tags=["Applications"])
def get_applications(
    application_service: ApplicationService = Depends(),
) -> list[New_UTADetails]:
    """
    Get all applications

    Parameters:
        application_service: a valid ApplicationService

    Returns:
        list[Application]: All `Application`s in the `Application` database table
    """

    # Return all applications
    return application_service.list()


@api.get("/user", response_model=UserApplication, tags=["Applications"])
def get_applications_user(
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> UserApplication:
    """
    Get all applications

    Parameters:
        application_service: a valid ApplicationService

    Returns:
        list[Application]: All `Application`s in the `Application` database table
    """

    return application_service.get_application(user)


@api.post("", response_model=New_UTADetails, tags=["Applications"])
def new_undergrad_application(
    application: New_UTADetails,
    application_service: ApplicationService = Depends(),
) -> New_UTADetails:
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

    return application_service.create_undergrad(application)


@api.post("/update", response_model=New_UTADetails, tags=["Applications"])
def update_undergrad_application(
    application: New_UTADetails,
    user: User = Depends(registered_user),
    application_service: ApplicationService = Depends(),
) -> New_UTADetails:
    """
    Update application

    Parameters:
        application: a valid New_UTA model
        user: The suer updating their model
        application_service: a valid ApplicationService

    Returns:
        Application: Created application

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    return application_service.update_undergrad(user, application)
