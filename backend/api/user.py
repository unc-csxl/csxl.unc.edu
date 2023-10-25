"""User operations open to registered users such as searching for fellow user profiles."""

from fastapi import APIRouter, Depends
from ..services import UserService
from ..models import User
from .authentication import registered_user

api = APIRouter(prefix="/api/user")
openapi_tags = {
    "name": "Users",
    "description": "User profile search and related operations.",
}


@api.get("", response_model=list[User], tags=["Users"])
def search(
    q: str, subject: User = Depends(registered_user), user_svc: UserService = Depends()
):
    """Search for users based on a query string which matches against name, onyen, and email address."""
    return user_svc.search(subject, q)
