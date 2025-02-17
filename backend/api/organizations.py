"""Organization API

Organization routes are used to create, retrieve, and update Organizations."""

from fastapi import APIRouter, Depends, Body

from ..services import OrganizationService, RoleService
from ..models.organization import Organization
from ..models.organization_membership import OrganizationMembership
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
    role_service: RoleService = Depends(),
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

    new_organization = organization_service.create(subject, organization)
    # Create a new role for the organization newly created
    role_service.create(subject, new_organization.slug)
    return new_organization


@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def get_organization_by_slug(
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
        HTTPException 404 if get_by_slug() raises an Exception
    """

    return organization_service.get_by_slug(slug)


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


@api.post(
    "/{slug}/roster",
    responses={404: {"model": None}},
    response_model=OrganizationMembership,
    tags=["Organizations"],
)
def add_membership_to_organization(
    slug: str,
    membership: OrganizationMembership = Body(...),
    organization_service: OrganizationService = Depends(),
    subject: User = Depends(registered_user),
) -> OrganizationMembership:
    """
    Add member

    Parameters:
        user_id: new member id, passed in from frontend
        organization_service: a valid OrganizationService
        subject: a valid User model representing the currently logged in User

    Returns:
        OrganizationMember: Created organization member

    Raises:
        HTTPException 404 if add_member() raises an Exception
    """
    new_member = organization_service.add_membership(subject, slug, membership)
    return new_member


@api.get(
    "/{slug}/roster",
    responses={404: {"model": None}},
    response_model=list[OrganizationMembership],
    tags=["Organizations"],
)
def get_roster_by_slug(
    slug: str,
    organization_service: OrganizationService = Depends(),
    subject: User = Depends(registered_user),
) -> list[OrganizationMembership]:
    """
    Get organization roster with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService
        // add user?

    Returns:
        list[OrganizationMember]: List of OrganizationMember of Organization with matching slug

    Raises:
        HTTPException 404 if get_roster() raises an Exception
    """
    return organization_service.get_roster(subject, slug)


@api.put(
    "/{slug}/roster",
    response_model=OrganizationMembership,
    tags=["Organizations"],
)
def update_membership(
    slug: str,
    membership: OrganizationMembership = Body(...),
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> OrganizationMembership:
    """
    Update membership role

    Parameters:
        membership_id: a membership id of the user and corresponding organization
        new_role: a valid role from the organization role enumeration to assign to a new User
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService
    """
    return organization_service.update_membership(subject, slug, membership)


@api.delete(
    "/{slug}/roster/{membership_id}", response_model=None, tags=["Organizations"]
)
def delete_membership(
    slug: str,
    membership_id: int,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
):
    """
    Delete user based on membership_id

    Parameters:
        slug: a string representing a unique identifier for an Organization
        membership_id: a unique membership id
        organization_service: a valid OrganizationService
        subject: a valid User model representing the currently logged in User
    """
    organization_service.remove_membership(subject, slug, membership_id)
