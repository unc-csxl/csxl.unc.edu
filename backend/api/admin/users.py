"""Health check routes are used by the production system to monitor whether the system is live and running."""

from fastapi import APIRouter, Depends, HTTPException
from ...services import UserService, UserPermissionError
from ...models import User, Paginated, PaginationParams
from ..authentication import registered_user


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = {"name": "User Admin API", "description": ""}

api = APIRouter(prefix="/api/admin/users")


@api.get("", tags=["List Users"])
def list_users(
    subject: User = Depends(registered_user),
    user_service: UserService = Depends(),
    page: int = 0,
    page_size: int = 10,
    order_by: str = "first_name",
    filter: str = ""
) -> Paginated[User]:
    try:
        pagination_params = PaginationParams(
            page=page, page_size=page_size, order_by=order_by, filter=filter)
        return user_service.list(subject, pagination_params)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
