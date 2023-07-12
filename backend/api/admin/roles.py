"""Roles are used to grant permissions to users via role-based access control.

This API is for administrative purposes only."""

from fastapi import APIRouter, Depends, HTTPException
from ...services import RoleService, UserPermissionError
from ...models import User, Role, RoleDetails, Permission
from ..authentication import registered_user


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = {"name": "(Admin) Roles", "description": "Roles are used to grant permissions to users."}

api = APIRouter(prefix="/api/admin/roles")


@api.get("", tags=["(Admin) Roles"])
def list_roles(
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends(),
) -> list[Role]:
    """List all roles in the system for administrators."""
    try:
        return role_service.list(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.get("/{id}", tags=["(Admin) Roles"])
def role_details(
    id: int,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends(),
) -> RoleDetails:
    """Get details about a specific role in the system for administrators."""
    try:
        return role_service.details(subject, id)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.post('/{id}/permission', tags=["(Admin) Roles"])
def grant_permission_to_role(
    id: int,
    permission: Permission,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends()
) -> RoleDetails:
    """Grant a permission to a role."""
    try:
        return role_service.grant_permission(subject, id, permission)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.delete("/{id}/permission/{permissionId}", tags=["(Admin) Roles"])
def revoke_permission_from_role(
    id: int,
    permissionId: int,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends()
) -> bool:
    """Revoke a permission from a role."""
    try:
        return role_service.revoke_permission(subject, id, permissionId)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.post('/{id}/member', tags=["(Admin) Roles"])
def add_member_to_role(
    id: int,
    member: User,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends()
) -> RoleDetails:
    """Add a member to a role."""
    try:
        return role_service.add_member(subject, id, member)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.delete("/{id}/member/{userId}", tags=["(Admin) Roles"])
def remove_member_from_role(
    id: int,
    userId: int,
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends()
) -> bool:
    """Remove a member from a role."""
    try:
        return role_service.remove_member(subject, id, userId)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
