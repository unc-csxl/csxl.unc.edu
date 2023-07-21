"""RegistrationDetail is the data object for a User's registration to an event."""

from pydantic import BaseModel

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
  event: 'Event'
  user: 'UserSummary'
  
from backend.models.event import Event;
from backend.models.user import UserSummary;
RegistrationDetail.update_forward_refs()


