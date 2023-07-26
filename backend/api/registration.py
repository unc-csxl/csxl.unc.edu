"""Registration API

Registration routes are used to create, retrieve, and update Registrations to Events."""

from fastapi import APIRouter, Depends, HTTPException
from backend.api.authentication import registered_user
from backend.models.registration import RegistrationDetail, Registration
from backend.models.user import User
from backend.services.registration import RegistrationService

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

api = APIRouter(prefix="/api/registrations")

@api.get("", response_model=list[RegistrationDetail], tags=['Registration'])
def get_registrations(registrations_service: RegistrationService = Depends()) -> list[RegistrationDetail]:
  """
  Get all registrations for all events

  Parameters:
    registration_service: a valid RegistrationService

  Returns:
    list[Role]: All `RegistrationDetail`s in the `Registrations` database table
  """

  # Return all registrations
  return registrations_service.all()

@api.post("", response_model=RegistrationDetail, tags=['Registration'])
def create_registration(registration: Registration, subject: User = Depends(registered_user), registrations_service: RegistrationService = Depends()) -> RegistrationDetail:
  """
  Create a registration by a user for an Event

  Parameters:
    registration: a valid RegistrationDetail model
    subject: a valid User model representing the currently logged in User
    registration_service: a valid RegistrationService
    
  Returns:
    RegistrationDetail object for the user

  Raises:
    HTTPException 422 if create() raises an Exception
  """

  try:
    # Try to create and return registration for user
    return registrations_service.create(subject, registration)
  except Exception as e:
    # Raise 422 exception if create fails (request body shaped incorrectly / not authorized)
    raise HTTPException(status_code=422, detail=str(e))

@api.get("/user/{user_id}/{status}", response_model=list[RegistrationDetail], tags=['Registration'])
def get_registrations_by_user(user_id: int, status: int, registrations_service: RegistrationService = Depends()) -> list[RegistrationDetail]:
  """
  Get all RegistrationDetail objects associated with a User based on attendance status

  Parameters:
    user_id: an int representing a unique identifier for a user
    status: an int representing if the user has registered for (0) or attended (1) an event
    registration_service: a valid RegistrationService

  Returns:
    list of RegistrationDetail objects for all events the user has registered for or attended

  Raises:
    HTTPException 404 if get_by_user() raises an Exception
  """

  try:
    # Try to get and return registrations for the user 
    return registrations_service.get_by_user(user_id, status)
  except Exception as e:
    # Raise 404 exception if get fails (no registrations for user)
    raise HTTPException(status_code=404, detail=str(e))

@api.get("/event/{event_id}/{status}", response_model=list[RegistrationDetail], tags=['Registration'])
def get_registrations_by_event(event_id: int, status: int, registrations_service: RegistrationService = Depends()) -> list[RegistrationDetail]:
  """
  Get all registrations associated with an Event based on attendance status

  Parameters:
    event_id: an int representing a unique identifier for an event
    status: an int representing if the user has registered for (0) or attended (1) an event
    registration_service: a valid RegistrationService

  Returns:
    list of Users who are registered for or attended the event

  Raises:
    HTTPException 404 if get_by_event() raises an Exception
  """
  
  try:
    # Try to get and return registrations for the event
    return registrations_service.get_by_event(event_id, status)
  except Exception as e:
    # Raise 404 exception if get fails (no registrations for event)
    raise HTTPException(status_code=404, detail=str(e))

@api.put("", response_model=RegistrationDetail, tags=['Registration'])
def mark_attended(registration: RegistrationDetail, subject: User = Depends(registered_user), registrations_service: RegistrationService = Depends()) -> RegistrationDetail:
  """
  Update a User's attendance status for an Event

  Parameters:
    registration: a valid RegistrationDetail model
    subject: a valid User model representing the currently logged in User
    registration_service: a valid RegistrationService

  Returns:
    updated RegistrationDetail object

  Raises:
    HTTPException 404 if update_status() raises an Exception.
  """

  try:
    # Try to update and return registration
    return registrations_service.update_status(subject, registration)
  except Exception as e:
    # Raise 404 exception if update fails (registration not found / not authorized)
    raise HTTPException(status_code=404, detail=str(e))

@api.delete("/registration/{reg_id}", response_model=None, tags=['Registration'])
def delete_registration(reg_id: int, subject: User = Depends(registered_user), registrations_service: RegistrationService = Depends()) -> None:
  """
  Delete RegistrationDetail for EventDetail by Registration ID

  Parameters:
    reg_id: an int that represents a Registration ID
    subject: a valid User model representing the currently logged in User
    registration_service: a valid RegistrationService

  Raises:
    HTTPException 404 if delete_registration() raises an Exception.
  """

  try:
    # Try to delete registration
    registrations_service.delete_registration(subject, reg_id)
  except Exception as e:
    # Raise 404 exception if delete fails (registration does not exist / not authorized)
    raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{event_id}", response_model=None, tags=['Registration'])
def clear_event_registrations(event_id: int, subject: User = Depends(registered_user), registrations_service: RegistrationService = Depends()) -> None:
  """
  Clear all registrations for an event

  Parameters:
    event_id: an int representing a unique identifier for an event
    subject: a valid User model representing the currently logged in User
    registration_service: a valid RegistrationService

  Raises:
    HTTPException 404 if clear_registrations() raises an Exception
  """

  try:
    # Try to clear registrations
    registrations_service.clear_registrations(subject, event_id)
  except Exception as e:
    # Raise 404 exception if clear fails (no registrations exist / not authorized)
    raise HTTPException(status_code=404, detail=str(e))

