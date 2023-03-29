from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from backend.models.event import Event

from datetime import datetime

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
    # ID of the organization hosting the event
    org_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    # Organization hosting the event
        # Generated from a relationship with the "organization table"
        # Back-populates the `events` field of `OrganizationEntity`
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")

    @classmethod
    def from_model(cls, model: Event) -> Self:
        """
        Class method that converts a `Event` object into a `EventEntity`
        
        Parameters:
            - model (Event): Model to convert into an entity
        Returns:
            EventEntity: Entity created from model
        """
        return cls(id=model.id, name=model.name, time=model.time, location=model.location, description=model.description, public=model.public, org_id=model.org_id)

    def to_model(self) -> Event:
        """
        Converts a `EventEntity` object into a `Event`
        
        Returns:
            Event: `Event` object from the entity
        """
        return Event(id=self.id, name=self.name, time=self.time, location=self.location, description=self.description, public=self.public, org_id=self.org_id)