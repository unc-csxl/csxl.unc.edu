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


@api.get("/{onyen}", tags=["Users"])
def get_by_onyen(
    onyen: str,
    subject: User = Depends(registered_user),
    user_svc: UserService = Depends(),
):
    """Search for one user by their onyen"""
    return user_svc.get_by_onyen(subject, onyen)
    

# Do we want this in the user api file or in my_courses?
# Is it unsafe if I put the pid in the url?
@api.get("/{pid}", tags=["Users"])
def get_user_by_pid(
    pid: int,
    subject: User = Depends(registered_user),
    user_svc: UserService = Depends(),
) -> User:
    return user_svc.get_by_pid(subject, pid)
