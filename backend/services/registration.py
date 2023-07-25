"""Definition of the RegistrationService used to update the RegistrationEntity."""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.services.event import EventService
from backend.services.org_role import OrgRoleService
from backend.services.permission import UserPermissionError
from ..database import db_session
from backend.models.registration import RegistrationDetail, Registration
from backend.entities.registration_entity import RegistrationEntity

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class RegistrationService:

  _session: Session

  def __init__(self, session: Session = Depends(db_session), org_roles: OrgRoleService = Depends(), events: EventService = Depends()):
    """Initializes the `RoleService` session"""
    self._session = session
    self._org_roles = org_roles
    self._events = events

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
  
  def check_permissions(self, subject: User, registration: RegistrationDetail, action: str, resource: str):
    # Check that user has permission to modify registrations for the organization
    org_roles = [org_role for org_role in self._org_roles.get_from_userid(subject.id) if
        org_role.org_id == registration.event.org_id and org_role.membership_type > 0]
      
    # If no role is found, raise an exception
    if (len(org_roles) <= 0):
        raise UserPermissionError('registration.update', f'registrations')

  def create(self, subject: User, registration: Registration) -> RegistrationDetail:
    """
    register a User for an EventDetail.

    Parameters:
      registration: a valid RegistrationDetail model.

    Returns:
      The RegistrationDetail object.

    Raises:
      ValueError if registration does not exist.
    """      

    # If user is not creating a registration for themself
    if (subject.id != registration.user_id):
      # Raise error
      raise UserPermissionError('registration.create', f'registrations')
    
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
    
  def update_status(self, subject: User, registration: RegistrationDetail) -> RegistrationDetail:
    """
    Update a RegistrationDetail's status to attended (1).

    Parameters:
      registration: a valid RegistrationDetail model.

    Returns:
      list of Registrations

    Raises:
      ValueError if there is no RegistrationDetail for the specified User and EventDetail.
    """
    # Check that user has permission to modify organization registrations
    self.check_permissions(subject, registration, 'registration.update', f'registrations')

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
      
  def delete_registration(self, subject: User, reg_id: int) -> None:
    """
    Delete a User's registration for an EventDetail.

    Parameters:
      reg_id: an integer that represents a RegistrationDetail ID

    Raises:
      ValueError if there is no RegistrationDetail for the specified User and EventDetail.
    """

    # Query the Registrations table for a registration associated with the specified id
    registration = self._session.query(RegistrationEntity).filter(RegistrationEntity.id == reg_id).one_or_none()

    # If a registration was found
    if registration:
      # If user is not trying to delete their own reg
      if (subject.id != registration.user_id):
          # Check that user has permission to modify organization registrations
          self.check_permissions(subject, registration, 'registration.delete', f'registrations/{reg_id}')

      # Delete Registration
      self._session.delete(registration)
      self._session.commit()
    else:
      raise ValueError(f"The user with the ID {subject.id} is not registered for the requested event.")
    
  def clear_registrations(self, subject: User, event_id: int):
    """
    Clear all registrations for an EventDetail.

    Parameters:
      event_id: an Integer representing a unique identifier for an event.

    Raises:
      ValueError if an event with the specified ID does not exist.
    """
    # Query the Registrations table for all events matching the event_id.
    registrations = self._session.query(RegistrationEntity).filter(RegistrationEntity.event_id == event_id).all()
      
    # If registrations were found
    if len(registrations) > 0:
      # Check that user has permission to clear registrations for organization
      self.check_permissions(subject, registrations[0], 'registration.delete', f'registrations/{event_id}')

      # Delete each registration
      for registration in registrations:
        self._session.delete(registration)
        self._session.commit()
    else:
      raise ValueError(f"There are no registrations associated with the event of ID {event_id}.") 
