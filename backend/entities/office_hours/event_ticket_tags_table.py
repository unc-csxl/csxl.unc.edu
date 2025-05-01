"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets."""

from sqlalchemy import Column, ForeignKey, Table
from ..entity_base import EntityBase


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"

# Association table between OfficeHoursTicket and OfficeHoursTicketTag
event_ticket_tags_table = Table(
    "office_hours__event_ticket_tags",
    EntityBase.metadata,
    Column("ticket_id", ForeignKey("office_hours__ticket.id"), primary_key=True),
    Column("ticket_tag_id", ForeignKey("office_hours__ticket_tag.id", ondelete="CASCADE"), primary_key=True),
)
