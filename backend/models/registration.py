"""RegistrationDetail is the data object for a User's registration to an event."""

from pydantic import BaseModel
from .event import Event
from .user import User

class Registration(BaseModel):
  """
  Model to represent `RegistrationDetail` connections between users and organizations
    
  This model is based on the `RegistrationEntity` model, which defines the shape
  of the `Registrations` database in the PostgreSQL database
  """
  id: int | None = None
  user_id: int
  event_id: int
  status: int

class RegistrationDetail(Registration):
  """
  Model to represent `RegistrationDetail` connections between users and organizations
    
  This model is based on the `RegistrationEntity` model, which defines the shape
  of the `Registrations` database in the PostgreSQL database
  """
  event: Event
  user: User