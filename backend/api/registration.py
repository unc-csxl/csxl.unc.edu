"""Registration routes are used to update the Registrations table"""

from fastapi import APIRouter, Depends, HTTPException
from backend.models.registration import Registration, RegistrationSummary
from backend.services.registration import RegistrationService

api = APIRouter(prefix="/api/registrations")

@api.get("", response_model=list[Registration], tags=['Registration'])
def get_registrations(registrations_service: RegistrationService = Depends()) -> list[Registration]:
  """
  Get all registrations for all events.

  Parameters:
    registration_service: a valid RegistrationService.

  Returns:
    list[Role]: All `Registration`s in the `Registrations` database table
  """
  return registrations_service.all()

@api.post("", response_model=Registration, tags=['Registration'])
def create_registration(registration: RegistrationSummary, registrations_service: RegistrationService = Depends()) -> Registration:
  """
  Create a registration by a user for an event.

  Parameters:
    registration: a valid Registration model.
    registration_service: a valid RegistrationService.

  Returns:
    The Registration object for the user.

  Raises:
    HTTPException 422 if create() raises an Exception.
  """
  try:
    return registrations_service.create(registration)
  except Exception as e:
    raise HTTPException(status_code=422, detail=str(e))

@api.get("/user/{user_id}/{status}", response_model=list[Registration], tags=['Registration'])
def get_registrations_by_user(user_id: int, status: int, registrations_service: RegistrationService = Depends()) -> list[Registration]:
  """
  Get all Registration objects associated with a User based on attendance status.

  Parameters:
    user_id: an Integer representing a unique identifier for a user.
    status: an Integer representing if the user has registered for (0) or attended (1) an event.
    registration_service: a valid RegistrationService.

  Returns:
    list of Events the user has registered for or attended.

  Raises:
    HTTPException 404 if get_by_user() raises an Exception.
  """
  try:
    return registrations_service.get_by_user(user_id, status)
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))

@api.get("/event/{event_id}/{status}", response_model=list[Registration], tags=['Registration'])
def get_registrations_by_event(event_id: int, status: int, registrations_service: RegistrationService = Depends()) -> list[Registration]:
  """
  Get all registrations associated with an Event based on attendance status.

  Parameters:
    event_id: an Integer representing a unique identifier for an event.
    status: an Integer representing if the user has registered for (0) or attended (1) an event.
    registration_service: a valid RegistrationService.

  Returns:
    list of Users who are registered for or attended the event.

  Raises:
    HTTPException 404 if get_by_event() raises an Exception.
  """
  try:
    return registrations_service.get_by_event(event_id, status)
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))

@api.put("", response_model=Registration, tags=['Registration'])
def mark_attended(registration: Registration, registrations_service: RegistrationService = Depends()) -> Registration:
  """
  Update a User's attendance status for an Event.

  Parameters:
    registration: a valid Registration model.
    registration_service: a valid RegistrationService.

  Returns:
    The updated Registration object

  Raises:
    HTTPException 404 if update_status() raises an Exception.
  """
  try:
    return registrations_service.update_status(registration)
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))

@api.delete("", response_model=None, tags=['Registration'])
def delete_registration(registration: Registration, registrations_service: RegistrationService = Depends()) -> None:
  """
  Delete Registration for Event based on the User and the Event.

  Parameters:
    registration: a valid Registration model.
    registration_service: a valid RegistrationService.

  Raises:
    HTTPException 404 if delete_registration() raises an Exception.
  """
  try:
    registrations_service.delete_registration(registration)
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{event_id}", response_model=None, tags=['Registration'])
def clear_event_registrations(event_id: int, registrations_service: RegistrationService = Depends()) -> None:
  """
  Clear all registrations for an event.

  Parameters:
    event_id: an Integer representing a unique identifier for an event.
    registration_service: a valid RegistrationService.

  Raises:
    HTTPException 404 if clear_registrations() raises an Exception.
  """

  try:
    registrations_service.clear_registrations(event_id)
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))

