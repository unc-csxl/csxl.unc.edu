from fastapi import APIRouter, Depends, HTTPException
from ..services import OrganizationService, UserService
from ..models.organization import Organization
from ..models.organization_detail import OrganizationDetail
from backend.api.authentication import registered_user
from backend.models.user import User

api = APIRouter(prefix="/api/organizations")

@api.get("", response_model=list[OrganizationDetail], tags=['OrganizationDetail'])
def get_organizations(organization_service: OrganizationService = Depends()) -> list[OrganizationDetail]:
    """
    Get all organizations

    Returns:
        list[OrganizationDetail]: All `Organizations`s in the `Organization` database table
    """

    # Return all organizations
    return organization_service.all()

@api.post("", response_model=OrganizationDetail, tags=['OrganizationDetail'])
def new_organization(organization: Organization, subject: User = Depends(registered_user), organization_service: OrganizationService = Depends()) -> OrganizationDetail:
    """
    Create organization

    Returns:
        OrganizationDetail: Created organization
    """

    # Try to create organization
    try:
        # Return created organization
        return organization_service.create(subject, organization)
    except Exception as e:
        # Raise 422 exception if creation fails
        # - This would occur if the request body is shaped incorrectly
        raise HTTPException(status_code=422, detail=str(e))

@api.get("/{id}", responses={404: {"model": None}}, response_model=OrganizationDetail, tags=['OrganizationDetail'])
def get_organization_from_id(id: int, organization_service: OrganizationService = Depends()) -> OrganizationDetail:
    """
    Get organization with matching id

    Returns:
        OrganizationDetail: OrganizationDetail with matching id
    """
    
    # Try to get organization with matching id
    try: 
        # Return organization
        return organization_service.get_from_id(id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/name/{name}", responses={404: {"model": None}}, response_model=OrganizationDetail, tags=['OrganizationDetail'])
def get_organization_from_name(name: str, organization_service: OrganizationService = Depends()) -> OrganizationDetail:
    """
    Get organization with matching name

    Returns:
        OrganizationDetail: OrganizationDetail with matching name
    """
    
    # Try to get organization with matching name
    try: 
        # Return organization
        return organization_service.get_from_name(name)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.put("", responses={404: {"model": None}}, response_model=OrganizationDetail, tags=['OrganizationDetail'])
def update_organization(organization: OrganizationDetail, subject: User = Depends(registered_user), organization_service: OrganizationService = Depends()) -> OrganizationDetail:
    """
    Update organization

    Returns:
        OrganizationDetail: Updated organization
    """
    try: 
        # Return updated organization
        return organization_service.update(subject, organization)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", response_model=None, tags=['OrganizationDetail'])
def delete_organization(id: int, subject: User = Depends(registered_user), organization_service = Depends(OrganizationService)):
    """
    Delete organization based on id
    """

    # Try to delete organization
    try:
        # Return deleted organization
        return organization_service.delete(subject, id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))