"""Health check routes are used by the production system to monitor whether the system is live and running."""

from fastapi import APIRouter, Depends, HTTPException
from ...services import RoleService, UserPermissionError
from ...models import User, PaginationParams, Role
from ..authentication import registered_user


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = {"name": "Role Admin API", "description": ""}

api = APIRouter(prefix="/api/admin/roles")


@api.get("", tags=["Roles"])
def list_users(
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends(),
) -> list[Role]:
    try:
        return role_service.list(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
