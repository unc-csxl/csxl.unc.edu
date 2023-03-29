"""Definition of SQLAlchemy table-backed object mapping entity for RegistrationEntity."""

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from .entity_base import EntityBase
from typing import Self
from backend.models.registration import Registration

class RegistrationEntity(EntityBase):
  """Serves as the database model schema defining the shape of the `Registrations` table."""
  
  __tablename__ = "registrations"

  # Unique ID for a registration
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  # User ID associated with registration
  user_id: Mapped[int] = mapped_column(Integer)
  # Event ID associated with registration
  event_id: Mapped[int] = mapped_column(Integer)
  # Status of Registration (0 = Registered, 1 = Registered + Attended)
  status: Mapped[int] = mapped_column(Integer)

  @classmethod
  def from_model(cls, model: Registration) -> Self:
    """
    Class method that converts a `Registration` object into a `RegistrationEntity`
    
    Parameters:
        model: a valid Registration model to convert into an entity
    
    Returns:
        RegistrationEntity: a valid entity created from a Registration model
    """
    return cls(id=model.id, user_id=model.user_id, event_id=model.event_id, status=model.status)

  def to_model(self) -> Registration:
    """
    Class method that converts a `RegistrationEntity` into a `Registration` object
    
    Returns:
        Registration: a valid `Registration` model from the entity
        
    """
    return Registration(id=self.id, user_id=self.user_id, event_id=self.event_id, status=self.status)