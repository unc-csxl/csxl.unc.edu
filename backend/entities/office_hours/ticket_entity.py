"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets."""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...models.office_hours.ticket_state import TicketState
from ...models.office_hours.ticket_type import TicketType
from ...models.office_hours.ticket import OfficeHoursTicket, NewOfficeHoursTicket
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...models.academics.my_courses import OfficeHourTicketOverview
from .user_created_tickets_table import user_created_tickets_table


from ..entity_base import EntityBase
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = [
    "Ajay Gandecha",
    "Madelyn Andrews",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursTicket` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours__ticket"

    # Unique id for OfficeHoursTicket
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Description of ticket, concatenated from user-entered info
    description: Mapped[str] = mapped_column(String, nullable=False)
    # Type of OH ticket
    type: Mapped[TicketType] = mapped_column(SQLAlchemyEnum(TicketType), nullable=False)
    # State of OH ticket
    state: Mapped[TicketState] = mapped_column(
        SQLAlchemyEnum(TicketState), default=TicketState.QUEUED, nullable=False
    )
    # Time ticket was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    # Time ticket was called by a TA
    called_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    # Time ticket was closed by a TA
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    # Flag for if UTA has concerns about student
    have_concerns: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Notes from TA
    caller_notes: Mapped[str] = mapped_column(String, default="", nullable=False)

    # One-to-many relationship to event that the ticket was created in
    office_hours_id: Mapped[int] = mapped_column(
        ForeignKey("office_hours.id"), nullable=False
    )
    office_hours: Mapped["OfficeHoursEntity"] = relationship(back_populates="tickets")

    # One-to-many relationship of OfficeHoursTicket to section member(s)
    creators: Mapped[list["SectionMemberEntity"]] = relationship(
        secondary=user_created_tickets_table
    )

    # One-to-one relationship of OfficeHoursTicket to UTA that has called it; optional field
    caller_id: Mapped[int | None] = mapped_column(
        ForeignKey("academics__user_section.id"), nullable=True
    )
    caller: Mapped["SectionMemberEntity"] = relationship(
        back_populates="called_oh_tickets"
    )

    @classmethod
    def from_new_model(cls, model: NewOfficeHoursTicket) -> Self:
        """
        Class method that converts an `NewOfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (NewOfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            description=model.description,
            type=model.type,
            office_hours_id=model.office_hours_id,
        )

    @classmethod
    def from_model(cls, model: OfficeHoursTicket) -> Self:
        """
        Class method that converts an `OfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (OfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            id=model.id,
            description=model.description,
            type=model.type,
            state=model.state,
            created_at=model.created_at,
            called_at=model.called_at,
            closed_at=model.closed_at,
            have_concerns=model.have_concerns,
            caller_notes=model.caller_notes,
            office_hours_id=model.office_hours_id,
            caller_id=model.caller_id,
        )

    def to_model(self) -> OfficeHoursTicket:
        """
        Converts a `OfficeHoursTicketEntity` object into a `OfficeHoursTicket` model object

        Returns:
            OfficeHoursTicket: `OfficeHoursTicket` object from the entity
        """
        return OfficeHoursTicket(
            id=self.id,
            description=self.description,
            type=self.type,
            state=self.state,
            created_at=self.created_at,
            called_at=self.called_at,
            closed_at=self.closed_at,
            have_concerns=self.have_concerns,
            caller_notes=self.caller_notes,
            office_hours_id=self.office_hours_id,
            caller_id=self.caller_id,
        )

    def to_overview_model(self) -> OfficeHourTicketOverview:
        return OfficeHourTicketOverview(
            id=self.id,
            created_at=self.created_at,
            called_at=self.called_at,
            closed_at=self.closed_at,
            state=self.state.to_string(),
            type=self.type.to_string(),
            description=self.description,
            creators=[creator.user.to_public_model() for creator in self.creators],
            caller=(self.caller.user.to_public_model() if self.caller else None),
        )

    def to_details_model(self) -> OfficeHoursTicketDetails:
        """
        Converts a `OfficeHoursTicketEntity` object into a `OfficeHoursTicketDetails` model object

        Returns:
            OfficeHoursTicketDetails: `OfficeHoursTicketDetails` object from the entity
        """
        return OfficeHoursTicketDetails(
            id=self.id,
            description=self.description,
            type=self.type,
            state=self.state,
            created_at=self.created_at,
            called_at=self.called_at,
            closed_at=self.closed_at,
            have_concerns=self.have_concerns,
            caller_notes=self.caller_notes,
            office_hours_id=self.office_hours_id,
            caller_id=self.caller_id,
            office_hours=self.office_hours,
            creators=[creator.to_flat_model() for creator in self.creators],
            caller=(self.caller.to_flat_model() if self.caller is not None else None),
        )
