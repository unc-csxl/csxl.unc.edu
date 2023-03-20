"""Health check routes are used by the production system to monitor whether the system is live and running."""

from fastapi import APIRouter, Depends, HTTPException
from ...services import RoleService, UserPermissionError
from ...models import User, Role, RoleDetails
from ..authentication import registered_user


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = {"name": "Role Admin API", "description": ""}

api = APIRouter(prefix="/api/admin/roles")


@api.get("", tags=["Roles"])
def list_roles(
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends(),
) -> list[Role]:
    try:
        return role_service.list(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))


@api.get("/{id}", tags=["Roles"])
def role_details(
    id: int,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends(),
) -> RoleDetails:
    try:
        return role_service.details(subject, id)
    except UserPermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))


@api.delete("/{id}/permission/{permissionId}", tags=["Roles"])
def revoke_permission(
    id: int,
    permissionId: int,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends()
) -> bool:
    try:
        return role_service.revoke(subject, id, permissionId)
    except UserPermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))