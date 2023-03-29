from fastapi import APIRouter, Depends, HTTPException
from ..services import UserService
from ..models import User
from .authentication import registered_user

api = APIRouter(prefix="/api/user")


@api.get("", response_model=list[User], tags=['User'])
def search(q: str, subject: User = Depends(registered_user), user_svc: UserService = Depends()):
		return user_svc.search(subject, q)

@api.get("/all", tags=['User'])
def get_users(user_service: UserService = Depends()) -> list[User]:
		"""
		Get all users

		Returns:
				list[User]: All `User`s in the `User` database table
		"""

		# Return all roles
		return user_service.getAll()

@api.post("", tags=['User'])
def new_user(user: User, user_service: UserService = Depends()) -> User:
		"""
		Create or update user

		Returns:
				User: Latest iteration of the created or updated user after changes made
		"""

		# Try to create / update user
		try:
				# Return created / updated user
				return user_service.save(user)
		except Exception as e:
				# Raise 422 exception if creation fails
				# - This would occur if the request body is shaped incorrectly
				raise HTTPException(status_code=422, detail=str(e))

@api.get("/{pid}", responses={404: {"model": None}}, tags=['User'])
def get_user(pid: int, user_service: UserService = Depends()) -> User:
    """
    Get user with matching pid

    Returns:
        User: User with matching pid
    """
    
    # Try to get user with matching pid
    try: 
        # Return user
        return user_service.get(pid)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{pid}", tags=['User'])
def delete_user(pid: int, user_service = Depends(UserService)):
    """
    Delete user based on pid
    """

    # Try to delete user
    try:
        # Return deleted role
        return user_service.delete(pid)
    except Exception as e:
        # Raise 404 exception if search fails
        # - This would occur if there is no response or if item to delete does not exist
        raise HTTPException(status_code=404, detail=str(e))