from fastapi import FastAPI, Depends, HTTPException, APIRouter
from backend.models.org_role import OrgRole
from backend.services.org_role import OrgRoleService

api = APIRouter(prefix="/api/orgroles")

@api.get("", tags=['Org Role'])
def get_roles(role_service: OrgRoleService = Depends()) -> list[OrgRole]:
    """
    Get all roles

    Returns:
        list[OrgRole]: All `OrgRole`s in the `OrgRole` database table
    """

    # Return all roles
    return role_service.all()

@api.post("", tags=['Org Role'])
def new_role(role: OrgRole, role_service: OrgRoleService = Depends()) -> OrgRole:
    """
    Create or update role

    Returns:
        OrgRole: Latest iteration of the created or updated role after changes made
    """

    # Try to create / update role
    try:
        # Return created / updated role
        return role_service.create(role)
    except Exception as e:
        # Raise 422 exception if creation fails
        # - This would occur if the request body is shaped incorrectly
        raise HTTPException(status_code=422, detail=str(e))

@api.get("/user/{user_id}", responses={404: {"model": None}}, tags=['Org Role'])
def get_role_from_userid(user_id: int, role_service: OrgRoleService = Depends()) -> list[OrgRole]:
    """
    Get all roles with matching user_id

    Returns:
        list[Role]: All roles with matching user_id
    """
    
    # Try to get all roles with matching user_id
    try: 
        # Return roles
        return role_service.get_from_userid(user_id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/org/{org_id}", responses={404: {"model": None}}, tags=['Org Role'])
def get_role_from_orgid(org_id: int, role_service: OrgRoleService = Depends()) -> list[OrgRole]:
    """
    Get all roles with matching org_id

    Returns:
        list[OrgRole]: All roles with matching org_id
    """

    # Try to get all roles with matching org_id
    try: 
        # Return roles
        return role_service.get_from_orgid(org_id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{id}", tags=['Org Role'])
def delete_role(id: int, role_service = Depends(OrgRoleService)):
    """
    Delete role based on id
    """

    # Try to delete role
    try:
        # Return deleted role
        return role_service.delete(id)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))

