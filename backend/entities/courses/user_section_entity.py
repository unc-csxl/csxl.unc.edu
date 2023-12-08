"""Definition of SQLAlchemy table-backed object mapping entity for the user - section association table."""

from enum import Enum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class CourseSectionMembershipType(Enum):
    STUDENT = 0
    UTA = 1
    GTA = 2
    INSTRUCTOR = 3


class UserSectionEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `UserSection` table

    This table is the association / join table to establish the many-to-many relationship
    between the `user` and `section` tables.

    To establish this relationship, this entity contains two primary key fields for each related
    table.
    """

    # Name for the user section table in the PostgreSQL database
    __tablename__ = "courses__user_section"

    # User Section properties (columns in the database table)

    # User for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    # Section for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    section_id: Mapped[int] = mapped_column(
        ForeignKey("courses__section.id"), primary_key=True
    )

    # Type of relationship
    member_type: Mapped[CourseSectionMembershipType] = mapped_column(
        SQLAlchemyEnum(CourseSectionMembershipType)
    )
