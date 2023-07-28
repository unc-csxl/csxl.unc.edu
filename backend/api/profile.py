"""Profile API

This API is used to retrieve and update a user's profile."""

from fastapi import APIRouter, Depends
from .authentication import authenticated_pid
from ..services import UserService
from ..models import UserDetails, User, UnregisteredUser, ProfileForm

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/profile")
openapi_tags = {
    "name": "Profile",
    "description": "Update and retrieve your CSXL profile as an authenticated user.",
}


@api.get("", response_model=UserDetails | UnregisteredUser, tags=["Profile"])
def read_profile(
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    user_svc: UserService = Depends(),
):
    """Retrieve a user's profile. If the user does not exist, return a NewUser.

    To handle new users, we rely only on the authenticated_pid dependency rather than
    registered_user.
    """
    pid, onyen = pid_onyen
    user = user_svc.get_details(pid)
    if user:
        return user
    else:
        return UnregisteredUser(pid=pid, onyen=onyen)


@api.put("", response_model=User, tags=["Profile"])
def update_profile(
    profile: ProfileForm,
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    user_svc: UserService = Depends(),
):
    """Update a user's profile. If the user does not exist, create a new user.

    Since the user is authenticated, we can trust the pid and onyen. However,
    since the user may not be registered, we depend on authenticated_pid rather
    than registered_user.

    ProfileForm is used here, rather than User, for similar registration-specific
    purposes. Importantly, ProfileForm doesn't contain an ID field.
    """
    pid, onyen = pid_onyen
    user = user_svc.get(pid)
    if user is None:
        user = User(
            pid=pid,
            onyen=onyen,
            first_name=profile.first_name,
            last_name=profile.last_name,
            email=profile.email,
            pronouns=profile.pronouns,
        )
        user = user_svc.create(user, user)
    else:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.pronouns = profile.pronouns
        user.onyen = onyen
        user = user_svc.update(user, user)
    return user
