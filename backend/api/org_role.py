"""OrgRole API

OrgRole routes are used to create, retrieve, and update roles in Organizations."""

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from backend.models.org_role import OrgRole, OrgRoleDetail
from backend.services.org_role import OrgRoleService
from backend.api.authentication import registered_user
from backend.models.user import User

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

api = APIRouter(prefix="/api/orgroles")

@api.get("", tags=['Org Role'])
def get_roles(role_service: OrgRoleService = Depends()) -> list[OrgRoleDetail]:
    """
    Get all roles

    Parameters:
        role_service: a valid OrgRoleService

    Returns:
        list[OrgRoleDetail]: All `OrgRoleDetail`s in the `OrgRole` database table
    """

    # Return all roles
    return role_service.all()

@api.post("", tags=['Org Role'])
def new_role(role: OrgRole, subject: User = Depends(registered_user), role_service: OrgRoleService = Depends()) -> OrgRoleDetail:
    """
    Create or update role

    Parameters:
        role: a valid OrgRole model
        subject: a valid User model representing the currently logged in User
        role_service: a valid OrgRoleService

    Returns:
        OrgRoleDetail: latest iteration of the created or updated role after changes made

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    try:
        # Try to create/update and return role
        return role_service.create(subject, role)
    except Exception as e:
        # Raise 422 exception if creation fails (request body is shaped incorrectly / not authorized)
        raise HTTPException(status_code=422, detail=str(e))

@api.get("/user/{user_id}", responses={404: {"model": None}}, tags=['Org Role'])
def get_role_from_userid(user_id: int, role_service: OrgRoleService = Depends()) -> list[OrgRoleDetail]:
    """
    Get all roles with matching user_id

    Parameters:
        user_id: an int representing a unique identifier for a user
        role_service: a valid OrgRoleService

    Returns:
        list[Role]: All roles with matching user_id

    Raises:
        HTTPException 404 if get_from_userid() raises an Exception
    """

    try: 
        # Try to get and return all roles associated with the user_id
        return role_service.get_from_userid(user_id)
    except Exception as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/org/{org_id}", responses={404: {"model": None}}, tags=['Org Role'])
def get_role_from_orgid(org_id: int, role_service: OrgRoleService = Depends()) -> list[OrgRoleDetail]:
    """
    Get all roles with matching org_id

    Parameters:
        org_id: an int representing 
        role_service: a valid OrgRoleService

    Returns:
        list[OrgRoleDetail]: All roles with matching org_id

    Raises:
        HTTPException 404 if get_from_orgid() raises an Exception
    """

    try: 
        # Try to get and return all roles with matching org_id
        return role_service.get_from_orgid(org_id)
    except Exception as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['Org Role'])
def delete_role(id: int, subject: User = Depends(registered_user), role_service = Depends(OrgRoleService)):
    """
    Delete role based on id

    Parameters:
        id: an int representing a unique identifier for an orgnaization
        subject: a valid User model representing the currently logged in User
        role_service: a valid OrgRoleService

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    try:
        # Try to delete role
        role_service.delete(subject, id)
    except Exception as e:
        # Raise 404 exception if search fails (no response / item to delete does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))