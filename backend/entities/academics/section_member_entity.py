"""Definition of SQLAlchemy table-backed object mapping entity for the user - section association table."""

from typing import Self
from sqlalchemy import ForeignKey, Integer, Index
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..office_hours import user_created_tickets_table
from ...models.academics.section_member_details import SectionMemberDetails

from ...models.roster_role import RosterRole
from ...models.academics.section_member import SectionMember, SectionMemberDraft

from ..entity_base import EntityBase

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Madelyn Andrews",
    "Bailey DeSouza",
    "Meghan Sun",
]
__copyright__ = "Copyright 2024"
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

    # Add indexes to the database for fast, common lookup queries
    __table_args__ = (
        Index(
            "ix_academics__user_section__by_user",
            "user_id",
            "section_id",
            unique=True,
        ),
        Index(
            "ix_academics__user_section__by_section",
            "section_id",
            "user_id",
            unique=True,
        ),
    )

    # User Section properties (columns in the database table)

    # Unique ID for a user's membership in an academic section
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Section for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    section_id: Mapped[int] = mapped_column(ForeignKey("academics__section.id"))
    section: Mapped["SectionEntity"] = relationship(back_populates="members")

    # User for the current relation
    # NOTE: This is ultimately a join table for a many-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="sections")

    # Type of User Role in Academic Section
    member_role: Mapped[RosterRole] = mapped_column(SQLAlchemyEnum(RosterRole))

    # Tickets that have been created by the user
    created_oh_tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(
        secondary=user_created_tickets_table
    )

    # Tickets that have been called by the user
    called_oh_tickets: Mapped[list["OfficeHoursTicketEntity"]] = relationship(
        back_populates="caller", cascade="all, delete"
    )

    def to_flat_model(self) -> SectionMember:
        """
        Converts a `SectionEntity` object into a `SectionMember` model object

        Returns:
            SectionMember: `SectionMember` object from the entity
        """
        return SectionMember(
            id=self.id,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            pronouns=self.user.pronouns,
            member_role=self.member_role,
        )

    @classmethod
    def from_draft_model(cls, model: SectionMemberDraft) -> Self:
        # Draft Model Usually Will Not Have ID - Auto Generated.
        # ID will not be None ONLY For Testing Purpose
        return cls(
            id=model.id,  # If model's id is None, set entity's id to None too
            section_id=model.section_id,
            user_id=model.user_id,
            member_role=model.member_role,
        )

    @classmethod
    def from_model(cls, model: SectionMember) -> Self:
        """
        Class method that converts an `SectionMember` model into a `SectionMemberEntity`

        Parameters:
            - model (SectionMember): Model to convert into an entity
        Returns:
            SectionMemberEntity: Entity created from model
        """
        return cls(
            id=model.id,
            first_name=model.user.first_name,
            last_name=model.user.last_name,
            pronouns=model.user.pronouns,
            member_role=model.member_role,
        )

    def to_details_model(self) -> SectionMemberDetails:
        """
        Converts a `SectionMemberEntity` object into a `SectionMemberDetails` model object

        Returns:
            SectionMemberDetails: `SectionMemberDetails` object from the entity
        """
        return SectionMemberDetails(
            id=self.id,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            pronouns=self.user.pronouns,
            member_role=self.member_role,
            user=self.user.to_model(),
            section=self.section.to_model(),
            created_oh_tickets=[
                ticket.to_model() for ticket in self.created_oh_tickets
            ],
            called_oh_tickets=[ticket.to_model() for ticket in self.called_oh_tickets],
        )
