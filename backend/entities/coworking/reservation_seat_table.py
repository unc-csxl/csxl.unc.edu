"""Join table between Reservation and Seat entities."""

from sqlalchemy import Table, Column, ForeignKey
from ..entity_base import EntityBase

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

reservation_seat_table = Table(
    "coworking__reservation_seat",
    EntityBase.metadata,
    Column("reservation_id", ForeignKey("coworking__reservation.id"), primary_key=True),
    Column("seat_id", ForeignKey("coworking__seat.id"), primary_key=True),
)
