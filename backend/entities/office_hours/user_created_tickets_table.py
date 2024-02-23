"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets."""

from sqlalchemy import Column, ForeignKey, Table
from ..entity_base import EntityBase


__authors__ = ["Madelyn Andrews"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

user_created_tickets_table = Table(
    "office_hours__user_created_ticket",
    EntityBase.metadata,
    Column("ticket_id", ForeignKey("office_hours__ticket.id"), primary_key=True),
    Column(
        "user_section_id",
        ForeignKey("academics__user_section.pid_section_id"),
        primary_key=True,
    ),
)
