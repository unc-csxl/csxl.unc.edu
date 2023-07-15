from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from backend.models.registration import RegistrationDetail, Registration
from backend.entities.registration_entity import RegistrationEntity

"""Definition of the RegistrationService used to update the RegistrationEntity."""

class RegistrationService:

  _session: Session

  def __init__(self, session: Session = Depends(db_session)):
      self._session = session

  def all(self) -> list[RegistrationDetail]:
    """
    Get a list of all Registrations.

    Returns:
      list of Registrations

    Raises:
      None
    """
    query = select(RegistrationEntity)
    entities = self._session.scalars(query).all()
    return [entity.to_model() for entity in entities]

  def create(self, registration: Registration) -> RegistrationDetail:
    """
    register a User for an EventDetail.

    Parameters:
      registration: a valid RegistrationDetail model.

    Returns:
      The RegistrationDetail object.

    Raises:
      ValueError if registration does not exist.
    """      
    # Attempt to get RegistrationEntity based on the IDs of the given user and event.
    entity = self._session.query(RegistrationEntity).filter(
      RegistrationEntity.user_id == registration.user_id,
      RegistrationEntity.event_id == registration.event_id).one_or_none()

    # Check if the registration already exists in the table.
    if entity:
      # If the registration exists, raise a value error with a description.
      raise ValueError(f"This user is already registered for the event.")
    else:
      # If the registration does not exist, create a new registration.
      registration_entity = RegistrationEntity.from_model(registration)
      self._session.add(registration_entity)
      self._session.commit()

      # Return the registration as a RegistrationDetail model.
      return registration_entity.to_model()
      
  def get_by_user(self, user_id: int, status: int) -> list[RegistrationDetail]:
    """
    Get all registrations associated with a user.

    Parameters:
      user_id: an Integer representing a unique identifier for a user.
      status: an Integer representing if the user has registered for (0) or attended (1) an event.

    Returns:
      list of Registrations
    """
    # Query the Registrations table for all entries with the specified user_id and status.
    entities = self._session.query(RegistrationEntity).filter(
        RegistrationEntity.user_id == user_id, RegistrationEntity.status == status).all()
    
    # Return the registrations as a list of RegistrationDetail models
    return [entity.to_model() for entity in entities]
          
  def get_by_event(self, event_id: int, status: int) -> list[RegistrationDetail]:
    """
    Get all registrations associated with an event.

    Parameters:
      event_id: an Integer representing a unique identifier for an event.
      status: an Integer representing if the user has registered for (0) or attended (1) an event.

    Returns:
      list of Registrations
    """
    # Query the Registrations table for all entries associated with the specified event_id and status.
    entities = self._session.query(RegistrationEntity).filter(
      RegistrationEntity.event_id == event_id, RegistrationEntity.status == status).all()
    
    # Return the registrations as a list of RegistrationDetail models.
    return [entity.to_model() for entity in entities]
    
  def update_status(self, registration: RegistrationDetail) -> RegistrationDetail:
    """
    Update a RegistrationDetail's status to attended (1).

    Parameters:
      registration: a valid RegistrationDetail model.

    Returns:
      list of Registrations

    Raises:
      ValueError if there is no RegistrationDetail for the specified User and EventDetail.
    """
    # Query the Registrations table for a registration associated with the specified user_id and event_id.
    entity = self._session.query(RegistrationEntity).filter(
      RegistrationEntity.user_id == registration.user_id, 
      RegistrationEntity.event_id == registration.event_id).one_or_none()
    
    # If a registration was found, update the entity status to 1 (= Attended).
    if entity:
      entity.status = 1
      self._session.commit()

      # Return the updated registration as a RegistrationDetail model.
      return entity.to_model()
    else:
      raise ValueError(f"The user with the ID {registration.user_id} is not registered for the event with the ID {registration.event_id}.")
      
  def delete_registration(self, reg_id: int) -> None:
    """
    Delete a User's registration for an EventDetail.

    Parameters:
      reg_id: an integer that represents a RegistrationDetail ID

    Raises:
      ValueError if there is no RegistrationDetail for the specified User and EventDetail.
    """
    # Query the Registrations table for a registration associated with the specified id
    entity = self._session.query(RegistrationEntity).filter(RegistrationEntity.id == reg_id).one_or_none()
      
    # If a registration was found, delete the registration.
    if entity:
      self._session.delete(entity)
      self._session.commit()
    else:
      raise ValueError(f"The user with the ID {entity.user_id} is not registered for the event with the ID {entity.event_id}.")
    
  def clear_registrations(self, event_id: int):
    """
    Clear all registrations for an EventDetail.

    Parameters:
      event_id: an Integer representing a unique identifier for an event.

    Raises:
      ValueError if an event with the specified ID does not exist.
    """
    # Query the Registrations table for all events matching the event_id.
    registrations = self._session.query(RegistrationEntity).filter(RegistrationEntity.event_id == event_id).all()
      
    # If registrations were found, delete each one.
    if len(registrations) > 0:
      for registration in registrations:
        self._session.delete(registration)
        self._session.commit()
    else:
      raise ValueError(f"There is no event with the ID {event_id}.") 
