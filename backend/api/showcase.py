"""423 Showcase API

API Route used to supply data for the 423 project showcase.

"""

from fastapi import APIRouter, Depends

from ..services import ShowcaseService
from ..api.authentication import registered_user
from ..models.user import User
from ..models.showcase_project import ShowcaseProject

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/showcase")
openapi_tags = {
    "name": "COMP 423 Showcase",
    "description": "Showcasing the amazing projects created by COMP 423 students!",
}


@api.get("", response_model=list[ShowcaseProject], tags=["COMP 423 Showcase"])
def get_projects(
    subject: User = Depends(registered_user),
    showcase_service: ShowcaseService = Depends(),
) -> list[ShowcaseProject]:
    """
    Get all COMP 423 projects.

    Parameters:
        showcase_service: a valid ShowcaseService

    Returns:
        list[ShowcaseProject]: All projects
    """
    # Return all organizations
    return showcase_service.all()
