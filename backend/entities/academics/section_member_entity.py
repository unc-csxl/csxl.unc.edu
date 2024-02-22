"""Definition of SQLAlchemy table-backed object mapping entity for the user - section association table."""

from typing import Self
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.office_hours import user_created_tickets_table

from ...models.roster_role import RosterRole
from ...models.academics.section_member import SectionMember

from ..entity_base import EntityBase

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionMemberEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `UserSection` table

    This table is the association / join table to establish the many-to-many relationship
    between the `user` and `section` tables.

    To establish this relationship, this entity contains two primary key fields for each related
    table.
    """

    # Name for the user section table in the PostgreSQL database
    __tablename__ = "academics__user_section"

    # User Section properties (columns in the database table)

    # Section for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    section_id: Mapped[int] = mapped_column(
        ForeignKey("academics__section.id"), primary_key=True
    )
    section: Mapped["SectionEntity"] = relationship(back_populates="members")

    # User for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["UserEntity"] = relationship(back_populates="sections")

    # Type of relationship
    member_role: Mapped[RosterRole] = mapped_column(SQLAlchemyEnum(RosterRole))

    # Tickets that have been created by the user
    created_tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(secondary=user_created_tickets_table)

    # Tickets that have been called by the user
    called_tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(back_populates="caller", cascade="all, delete")

    def to_flat_model(self) -> SectionMember:
        """
        Converts a `SectionEntity` object into a `SectionMember` model object

        Returns:
            SectionMember: `SectionMember` object from the entity
        """
        return SectionMember(
            id=self.user.id,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            pronouns=self.user.pronouns,
            member_role=self.member_role,
        )
