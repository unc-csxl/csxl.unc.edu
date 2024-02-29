"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets."""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.office_hours.ticket_state import TicketState
from backend.models.office_hours.ticket_type import TicketType
from .user_created_tickets_table import user_created_tickets_table


from ..entity_base import EntityBase
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketEntity(EntityBase):
    # TODO: write description
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
        SQLAlchemyEnum(TicketState), nullable=False
    )
    # Time ticket was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    # Time ticket was closed by a TA; nullable if ticket gets canceled
    closed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    # Flag for if UTA has concerns about student
    have_concerns: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Notes from TA
    caller_notes: Mapped[str] = mapped_column(String, default="", nullable=False)

    # One-to-one relationship to event that the ticket was created in
    event_id: Mapped[int] = mapped_column(
        ForeignKey("office_hours__event.id"), nullable=False
    )
    event: Mapped["OfficeHoursEventEntity"] = relationship(back_populates="tickets")

    # One-to-many relationship of OfficeHoursTicket to section member(s)
    creators: Mapped[list["SectionMemberEntity"]] = relationship(
        secondary=user_created_tickets_table
    )

    # One-to-one relationship of OfficeHoursTicket to UTA that has called it; optional field
    caller_id: Mapped[int | None] = mapped_column(
        ForeignKey("academics__user_section.id"), nullable=True
    )
    caller: Mapped["SectionMemberEntity"] = relationship(
        back_populates="called_tickets"
    )
