"""RegistrationDetail is the data object for a User's registration to an event."""

from pydantic import BaseModel

class RegistrationDetail(BaseModel):
  """
  Model to represent `RegistrationDetail` connections between users and organizations
    
  This model is based on the `RegistrationEntity` model, which defines the shape
  of the `Registrations` database in the PostgreSQL database
  """
  id: int | None = None
  user_id: int
  event_id: int
  status: int
  event: 'Event'
  user: 'UserSummary'

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


from backend.models.event import Event;
from backend.models.user import UserSummary;
RegistrationDetail.update_forward_refs()


