"""Organizations API

Organizations routes are used to create, retrieve, and update Organizations."""

from fastapi import APIRouter, Depends, HTTPException
from ..services import OrganizationService
from ..models.organization import Organization
from backend.api.authentication import registered_user
from backend.models.user import User

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

api = APIRouter(prefix="/api/organizations")

@api.get("", response_model=list[Organization], tags=['Organization'])
def get_organizations(organization_service: OrganizationService = Depends()) -> list[Organization]:
    """
    Get all organizations

    Parameters:
        organization_service: a valid OrganizationService

    Returns:
        list[Organization]: All `Organizations`s in the `Organization` database table
    """

    # Return all organizations
    return organization_service.all()

@api.post("", response_model=Organization, tags=['Organization'])
def new_organization(organization: Organization, subject: User = Depends(registered_user), organization_service: OrganizationService = Depends()) -> Organization:
    """
    Create organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        OrganizationDetail: Created organization

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    try:
        # Try to create and return new organization
        return organization_service.create(subject, organization)
    except Exception as e:
        # Raise 422 exception if creation fails (request body is shaped incorrectly / not authorized)
        raise HTTPException(status_code=422, detail=str(e))

@api.get("/{id}", responses={404: {"model": None}}, response_model=Organization, tags=['Organization'])
def get_organization_from_id(id: int, organization_service: OrganizationService = Depends()) -> Organization:
    """
    Get organization with matching id

    Parameters:
        id: an int representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        OrganizationDetail: OrganizationDetail with matching id

    Raises:
        HTTPException 404 if get_from_id() raises an Exception
    """
    
    # Try to get organization with matching id
    try: 
        # Return organization
        return organization_service.get_from_id(id)
    except Exception as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/name/{name}", responses={404: {"model": None}}, response_model=Organization, tags=['Organization'])
def get_organization_from_name(name: str, organization_service: OrganizationService = Depends()) -> Organization:
    """
    Get organization with matching name

    Parameters:
        name: a str representing the name of the organization
        organization_service: an OrganizationService

    Returns:
        OrganizationDetail: OrganizationDetail with matching name

    Raises:
        HTTPException 404 if get_from_name() raises an Exception
    """
    
    try: 
        # Try to get and return organization with matching name
        return organization_service.get_from_name(name)
    except Exception as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))

@api.put("", responses={404: {"model": None}}, response_model=Organization, tags=['Organization'])
def update_organization(organization: Organization, subject: User = Depends(registered_user), organization_service: OrganizationService = Depends()) -> Organization:
    """
    Update organization

    Parameters:
        organization: a valid OrganizationDetail model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        OrganizationDetail: Updated organization

    Raises HTTPException 404 if update() raises an Exception
    """
    try: 
        # Return updated organization
        return organization_service.update(subject, organization)
    except Exception as e:
        # Raise 404 exception if update fails (organization does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", response_model=None, tags=['Organization'])
def delete_organization(id: int, subject: User = Depends(registered_user), organization_service = Depends(OrganizationService)):
    """
    Delete organization based on id

    Parameters:
        id: an int representing a unique identifier for an Organization
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    try:
        # Try to delete organization
        organization_service.delete(subject, id)
    except Exception as e:
        # Raise 404 exception if delete fails (organization does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))