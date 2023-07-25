"""Definition of SQLAlchemy table-backed object mapping entity for RegistrationEntity."""

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from backend.models.registration import RegistrationDetail, Registration

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class RegistrationEntity(EntityBase):
  """Serves as the database model schema defining the shape of the `Registrations` table."""
  
  __tablename__ = "registrations"

  # Unique ID for a registration
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  # User ID associated with registration
  user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
  # EventDetail ID associated with registration
  event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
  # Status of RegistrationDetail (0 = Registered, 1 = Registered + Attended)
  status: Mapped[int] = mapped_column(Integer)

  # Bi-Directional Relationship Fields
  event: Mapped['EventEntity'] = relationship(back_populates="user_associations")
  user: Mapped['UserEntity'] = relationship(back_populates="event_associations")

  @classmethod
  def from_model(cls, model: RegistrationDetail) -> Self:
    """
    Class method that converts a `RegistrationDetail` object into a `RegistrationEntity`
    
    Parameters:
        model: a valid RegistrationDetail model to convert into an entity
    
    Returns:
        RegistrationEntity: a valid entity created from a RegistrationDetail model
    """
    return cls(id=model.id, user_id=model.user_id, event_id=model.event_id, status=model.status)

  def to_model(self) -> RegistrationDetail:
    """
    Class method that converts a `RegistrationEntity` into a `RegistrationDetail` object
    
    Returns:
        RegistrationDetail: a valid `RegistrationDetail` model from the entity
        
    """
    return RegistrationDetail(
      id=self.id, 
      user_id=self.user_id, 
      event_id=self.event_id, 
      status=self.status, 
      event=self.event.to_summary(), 
      user=self.user.to_summary()
    )

  def to_summary(self) -> Registration:
    """
    Converts a `OrgRoleEntity` object into a `OrgRole`
    
    Returns:
        OrgRole: `OrgRole` object from the entity
    """
    return Registration(
      id=self.id, 
      user_id=self.user_id, 
      event_id=self.event_id, 
      status=self.status
    )
  
from backend.entities.event_entity import EventEntity
from backend.entities.user_entity import UserEntity