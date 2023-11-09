"""User administration API."""

from fastapi import APIRouter, Depends, HTTPException
from ...services import UserService, UserPermissionException
from ...models import User, Paginated, PaginationParams
from ..authentication import registered_user


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = {
    "name": "(Admin) Users",
    "description": "User administration end points.",
}

api = APIRouter(prefix="/api/admin/users")


@api.get("", tags=["(Admin) Users"])
def list_users(
    subject: User = Depends(registered_user),
    user_service: UserService = Depends(),
    page: int = 0,
    page_size: int = 10,
    order_by: str = "first_name",
    filter: str = "",
) -> Paginated[User]:
    """List users via standard backend pagination query parameters."""
    try:
        pagination_params = PaginationParams(
            page=page, page_size=page_size, order_by=order_by, filter=filter
        )
        return user_service.list(subject, pagination_params)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
