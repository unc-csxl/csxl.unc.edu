"""Registration is the data object for a User's registration to an event."""

from pydantic import BaseModel

class Registration(BaseModel):
  """
  Model to represent `Registration` connections between users and organizations
    
  This model is based on the `RegistrationEntity` model, which defines the shape
  of the `Registrations` database in the PostgreSQL database
  """
  id: int | None = None
  user_id: int
  event_id: int
  status: int
  event: 'EventSummary'
  user: 'UserSummary'

class RegistrationSummary(BaseModel):
  """
  Model to represent `Registration` connections between users and organizations
    
  This model is based on the `RegistrationEntity` model, which defines the shape
  of the `Registrations` database in the PostgreSQL database
  """
  id: int | None = None
  user_id: int
  event_id: int
  status: int


from backend.models.event import EventSummary;
from backend.models.user import UserSummary;
Registration.update_forward_refs()


