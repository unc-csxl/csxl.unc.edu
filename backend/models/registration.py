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