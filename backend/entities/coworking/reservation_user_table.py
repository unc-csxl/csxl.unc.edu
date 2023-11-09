"""Join table between Reservation and Seat entities."""

from sqlalchemy import Table, Column, ForeignKey
from ..entity_base import EntityBase

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

reservation_user_table = Table(
    "coworking__reservation_user",
    EntityBase.metadata,
    Column("reservation_id", ForeignKey("coworking__reservation.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)
