"""Definition of SQLAlchemy table-backed object mapping entity for the room - section association table."""

from typing import Self
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.room_assignment_type import RoomAssignmentType

from ...models.roster_role import RosterRole
from ...models.courses.section_member import SectionMember

from ..entity_base import EntityBase

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionRoomEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `SectionRoom` table

    This table is the association / join table to establish the many-to-many relationship
    between the `room` and `section` tables.

    To establish this relationship, this entity contains two primary key fields for each related
    table.
    """

    # Name for the section room table in the PostgreSQL database
    __tablename__ = "courses__section_room"

    # Properties (columns in the database table)

    # Section for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    section_id: Mapped[int] = mapped_column(
        ForeignKey("courses__section.id"), primary_key=True
    )
    section: Mapped["SectionEntity"] = relationship(back_populates="rooms")

    # Room for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), primary_key=True)
    room: Mapped["RoomEntity"] = relationship(back_populates="course_sections")

    # Type of relationship
    assignment_type: Mapped[RoomAssignmentType] = mapped_column(
        SQLAlchemyEnum(RoomAssignmentType)
    )
