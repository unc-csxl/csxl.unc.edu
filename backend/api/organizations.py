"""Organization API

Organization routes are used to create, retrieve, and update Organizations."""

from fastapi import APIRouter, Depends

from ..services import OrganizationService
from ..models.organization import Organization
from ..models.organization_details import OrganizationDetails
from ..api.authentication import registered_user
from ..models.user import User

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/organizations")
openapi_tags = {
    "name": "Organizations",
    "description": "Create, update, delete, and retrieve CS Organizations.",
}


@api.get("", response_model=list[Organization], tags=["Organizations"])
def get_organizations(
    organization_service: OrganizationService = Depends(),
) -> list[Organization]:
    """
    Get all organizations

    Parameters:
        organization_service: a valid OrganizationService

    Returns:
        list[Organization]: All `Organization`s in the `Organization` database table
    """

    # Return all organizations
    return organization_service.all()


@api.post("", response_model=Organization, tags=["Organizations"])
def new_organization(
    organization: Organization,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> Organization:
    """
    Create organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        Organization: Created organization

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    return organization_service.create(subject, organization)


@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def get_organization_from_slug(
    slug: str, organization_service: OrganizationService = Depends()
) -> OrganizationDetails:
    """
    Get organization with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        Organization: Organization with matching slug

    Raises:
        HTTPException 404 if get_from_slug() raises an Exception
    """

    return organization_service.get_from_slug(slug)


@api.put(
    "",
    responses={404: {"model": None}},
    response_model=Organization,
    tags=["Organizations"],
)
def update_organization(
    organization: Organization,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> Organization:
    """
    Update organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        Organization: Updated organization

    Raises:
        HTTPException 404 if update() raises an Exception
    """

    return organization_service.update(subject, organization)


@api.delete("/{slug}", response_model=None, tags=["Organizations"])
def delete_organization(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
):
    """
    Delete organization based on slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    organization_service.delete(subject, slug)
