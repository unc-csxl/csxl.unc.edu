"""Definition of SQLAlchemy table-backed object mapping entity for Event Registrations."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.event_entity import EventEntity
from backend.entities.user_entity import UserEntity

from ..models import RegistrationType
from ..models.public_user import PublicUser
from .entity_base import EntityBase
from typing import Self
from ..models.event_registration import EventRegistration, NewEventRegistration
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EventRegistrationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `EventRegistration` table

    This table is the association / join table to establish the many-to-many relationship
    between the `user` and `event` tables. This allows many users to register for one event, and
    users be registered for many events.

    To establish this relationship, this entity contains two primary key fields for each related
    table.
    """

    # Name for the events table in the PostgreSQL database
    __tablename__ = "event_registration"

    # Event for the current event registration
    # NOTE: This is ultimately a join table for a many-to-many relationship
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    event: Mapped["EventEntity"] = relationship(back_populates="registrations")

    # User for the current event registration
    # NOTE: This is ultimately a join table for a many-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["UserEntity"] = relationship()

    # Type of relationship
    registration_type: Mapped[RegistrationType] = mapped_column(
        SQLAlchemyEnum(RegistrationType)
    )

    @classmethod
    def from_model(cls, model: EventRegistration) -> Self:
        """
        Class method that converts an `EventRegistration` model into a `EventRegistrationEntity`

        Parameters:
            - model (EventRegistration): Model to convert into an entity
        Returns:
            EventRegistrationEntity: Entity created from model
        """
        return cls(
            event_id=model.event_id,
            user_id=model.user_id,
            event=EventEntity.from_model(model.event),
            user=UserEntity.from_model(model.user),
            registration_type=model.registration_type,
        )

    @classmethod
    def from_new_model(cls, model: NewEventRegistration) -> Self:
        """
        Class method that converts an `NewEventRegistration` model into a `EventRegistrationEntity`

        Parameters:
            - model (NewEventRegistration): Model to convert into an entity
        Returns:
            EventRegistrationEntity: Entity created from model
        """
        return cls(
            event_id=model.event_id,
            user_id=model.user_id,
            registration_type=model.registration_type,
        )

    def to_model(self) -> EventRegistration:
        """
        Converts an `EventRegistrationEntity` into an `EventRegistration` model object
        to store registration information.

        Returns:
            EventRegistration: `EventRegistration` object from the entity
        """
        return EventRegistration(
            event_id=self.event_id,
            event=self.event.to_model(),
            user_id=self.user_id,
            user=self.user.to_model(),
            registration_type=self.registration_type,
        )

    def to_flat_model(self) -> PublicUser:
        """
        Converts an `EventRegistrationEntity` into an `PublicUser` model object
        to store public user information.

        Returns:
            PublicUser: `PublicUser` object from the entity
        """
        return PublicUser(
            id=self.user_id,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            pronouns=self.user.pronouns,
            email=self.user.email,
            github_avatar=self.user.github_avatar,
        )
