"""Definition of SQLAlchemy table-backed object mapping entity for EventEntity."""

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.event import Event
from datetime import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

class EventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Event` table"""

    __tablename__ = "event"

    # Unique ID for the event
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the event
    name: Mapped[str] = mapped_column(String)
    # Time of the event
    time: Mapped[datetime] = mapped_column(DateTime)
    # Location of the event
    location: Mapped[str] = mapped_column(String)
    # Description of the event
    description: Mapped[str] = mapped_column(String)
    # Whether the event is public or not
    public: Mapped[bool] = mapped_column(Boolean)
    # Organization hosting the event
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped['OrganizationEntity'] = relationship(back_populates="events")

    # TODO: Fields that establish relationships with events table
    # org_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    # # Organization hosting the event
    #     # Generated from a relationship with the "organization table"
    #     # Back-populates the `events` field of `OrganizationEntity`
    # organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")

    # # Bi-Directional Relationship Fields
    # users: Mapped[list["UserEntity"]] = relationship(secondary="registrations", back_populates="events")
    # user_associations: Mapped[list["RegistrationEntity"]] = relationship(back_populates="event",cascade="all,delete")

    @classmethod
    def from_model(cls, model: Event) -> Self:
        """
        Class method that converts a `Event` object into a `EventEntity`
        
        Parameters:
            - model (Event): Model to convert into an entity
        Returns:
            EventEntity: Entity created from model
        """
        return cls(id=model.id, name=model.name, time=model.time, location=model.location, description=model.description, public=model.public) #, org_id=model.org_id)

    def to_model(self) -> Event:
        """
        Converts a `EventEntity` object into a `Event`
        
        Returns:
            Event: `Event` object from the entity
        """
        return Event(id=self.id, 
                     name=self.name, 
                     time=self.time, 
                     location=self.location, 
                     description=self.description, 
                     public=self.public)
    
                     # TODO: fields that connect events to other entities
                     #org_id=self.org_id,
                     #organization=self.organization.to_summary(),
                     #users=[user.to_summary() for user in self.users],
                     #user_associations=[association.to_model() for association in self.user_associations])

# TODO: Imports to entities that have relationships with events
# from backend.entities.organization_entity import OrganizationEntity;
# from backend.entities.user_entity import UserEntity;
# from backend.entities.registration_entity import RegistrationEntity;