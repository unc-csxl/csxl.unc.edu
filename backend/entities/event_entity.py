"""Definition of SQLAlchemy table-backed object mapping entity for Events."""

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.event_details import EventDetails
from .entity_base import EntityBase
from typing import Self
from ..models.event import Event
from datetime import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Event` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "event"

    # Event properties (columns in the database table)

    # Unique ID for the event
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the event
    name: Mapped[str] = mapped_column(String)
    # Time of the event
    time: Mapped[datetime] = mapped_column(DateTime)
    # End time of the event
    end_time: Mapped[datetime] = mapped_column(DateTime)
    # Location of the event
    location: Mapped[str] = mapped_column(String)
    # Description of the event
    description: Mapped[str] = mapped_column(String)
    # Whether the event is public or not
    public: Mapped[bool] = mapped_column(Boolean)

    # Organization hosting the event
    # NOTE: This defines a one-to-many relationship between the organization and events tables.
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")

    @classmethod
    def from_model(cls, model: Event) -> Self:
        """
        Class method that converts an `Event` model into a `EventEntity`

        Parameters:
            - model (Event): Model to convert into an entity
        Returns:
            EventEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
            time=model.time,
            end_time=model.end_time,
            location=model.location,
            description=model.description,
            public=model.public,
            organization_id=model.organization_id,
        )

    def to_model(self) -> Event:
        """
        Converts a `EventEntity` object into a `Event` model object

        Returns:
            Event: `Event` object from the entity
        """
        return Event(
            id=self.id,
            name=self.name,
            time=self.time,
            end_time=self.end_time,
            location=self.location,
            description=self.description,
            public=self.public,
            organization_id=self.organization_id,
        )

    @classmethod
    def from_details_model(cls, model: EventDetails):
        """
        Class method that converts an `EventDetails` model into a `EventEntity`

        Parameters:
            - model (EventDetails): Model to convert into an entity
        Returns:
            EventEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
            time=model.time,
            end_time=model.end_time,
            location=model.location,
            description=model.description,
            public=model.public,
            organization_id=model.organization_id,
        )

    def to_details_model(self) -> EventDetails:
        """Create a EventDetails model from an EventEntity, with permissions and members included.

        Returns:
            EventDetails: An EventDetails model for API usage.
        """
        return EventDetails(
            id=self.id,
            name=self.name,
            time=self.time,
            end_time=self.end_time,
            location=self.location,
            description=self.description,
            public=self.public,
            organization_id=self.organization_id,
            organization=self.organization.to_model(),
        )
