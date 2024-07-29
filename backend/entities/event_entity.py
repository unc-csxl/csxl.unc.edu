"""Definition of SQLAlchemy table-backed object mapping entity for Events."""

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.event import EventOverview
from .entity_base import EntityBase
from typing import Self
from ..models.event import EventOverview, EventDraft
from ..models.registration_type import RegistrationType
from ..models.user import User

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
    start: Mapped[datetime] = mapped_column(DateTime)
    # Time of the event
    end: Mapped[datetime] = mapped_column(DateTime)
    # Location of the event
    location: Mapped[str] = mapped_column(String)
    # Description of the event
    description: Mapped[str] = mapped_column(String)
    # Whether the event is public or not
    public: Mapped[bool] = mapped_column(Boolean)
    # Maximim number of people who can register for the event
    registration_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # URL for the image for an event.
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    # Organization hosting the event
    # NOTE: This defines a one-to-many relationship between the organization and events tables.
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")

    # Registrations for the event
    # NOTE: This is part of a many-to-many relationship between events and users, via the event registration table.
    registrations: Mapped[list["EventRegistrationEntity"]] = relationship(
        back_populates="event", cascade="all,delete"
    )

    @classmethod
    def from_draft_model(cls, model: EventDraft, organization_id: int) -> Self:
        """
        Class method that converts an `DraftEvent` model into a `EventEntity`

        Parameters:
            - model (DraftEvent): Model to convert into an entity
        Returns:
            EventEntity: Entity created from model
        """
        return cls(
            name=model.name,
            start=model.start,
            end=model.end,
            location=model.location,
            description=model.description,
            public=False,  # TODO: Implement public and private events.
            registration_limit=model.registration_limit,
            organization_id=organization_id,
            image_url=model.image_url,
        )

    def to_overview_model(self, subject: User | None = None) -> EventOverview:
        """Creates an overview model from an event."""
        attendees = [
            registration.to_flat_model()
            for registration in self.registrations
            if registration.registration_type == RegistrationType.ATTENDEE
        ]

        user_registration = (
            [
                registration
                for registration in self.registrations
                if registration.user_id == subject.id
            ][0]
            if subject is not None
            and len(
                [
                    registration
                    for registration in self.registrations
                    if registration.user_id == subject.id
                ]
            )
            > 0
            else None
        )

        # Hide organizer info for unauthenticated users
        organizer_registrations = [
            registration
            for registration in self.registrations
            if registration.registration_type == RegistrationType.ORGANIZER
        ]

        organizers = [
            registration.user.to_public_model()
            for registration in organizer_registrations
        ]

        return EventOverview(
            id=self.id,
            name=self.name,
            start=self.start,
            end=self.end,
            location=self.location,
            description=self.description,
            public=self.public,
            registration_limit=self.registration_limit,
            number_registered=len(attendees),
            organization_slug=self.organization.slug,
            organization_icon=self.organization.logo,
            organization_name=self.organization.shorthand,
            organization_id=self.organization.id,
            organizers=organizers,
            user_registration_type=(
                user_registration.registration_type if user_registration else None
            ),
            image_url=self.image_url,
        )
