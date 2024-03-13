"""Application API

Application routes are used to create, retrieve, and update Applications."""

from fastapi import APIRouter, Depends

from backend.models.application import Application, New_UTA
from backend.models.application_details import New_UTADetails
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


@api.post("", response_model=New_UTA, tags=["Applications"])
def new_undergrad_application(
    application: New_UTA,
    application_service: ApplicationService = Depends(),
) -> New_UTA:
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
