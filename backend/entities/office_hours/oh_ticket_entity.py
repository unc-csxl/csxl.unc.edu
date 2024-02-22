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

__authors__ = ["Madelyn Andrews"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OfficeHoursTicketEntity(EntityBase):
    #TODO: write description
    """Serves as the database model schema defining the shape of the `OfficeHoursTicket` table


    """

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours__ticket"

    #TODO: add comments
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[TicketType] = mapped_column(SQLAlchemyEnum(TicketType), nullable=False)
    state: Mapped[TicketState] = mapped_column(SQLAlchemyEnum(TicketState), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    have_concerns: Mapped[bool] = mapped_column(Boolean, nullable=True)
    caller_notes: Mapped[str] = mapped_column(String, nullable=True)

    # OH Event that the ticket was created under
    event_id: Mapped[int] = mapped_column(ForeignKey("office_hours__event.id"), nullable=False)
    event: Mapped["OfficeHoursEventEntity"] = relationship(back_populates="tickets")

    # User(s) that have created the ticket entity
    creators: Mapped[list["SectionMemberEntity"]] = relationship(secondary=user_created_tickets_table)

    # UTA that has called the tickets
    caller_id: Mapped[int] = mapped_column(ForeignKey("academics__user_section.user_id"), nullable=True)
    caller: Mapped["SectionMemberEntity"] = relationship(back_populates="called_tickets")
