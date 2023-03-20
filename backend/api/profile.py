from fastapi import APIRouter, Depends
from .authentication import authenticated_pid
from ..services import UserService
from ..models import User, NewUser, ProfileForm

api = APIRouter(prefix="/api/profile")

PID = 0
ONYEN = 1

@api.get("", response_model=User | NewUser, tags=['profile'])
def read_profile(pid_onyen: tuple[int, str] = Depends(authenticated_pid), user_svc: UserService = Depends()):
    pid, onyen = pid_onyen
    user = user_svc.get(pid)
    if user:
        return user
    else:
        return NewUser(pid=pid, onyen=onyen)


@api.put("", response_model=User, tags=['profile'])
def update_profile(
    profile: ProfileForm,
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    user_svc: UserService = Depends()
):
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
    else:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.pronouns = profile.pronouns
        user.onyen = onyen
    user_svc.save(user)
    return user
