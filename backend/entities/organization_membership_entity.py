"""Definition of SQLAlchemy table-backed object mapping entity for Organization Members."""

from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models import OrganizationMembership


class OrganizationMembershipEntity(EntityBase):

    __tablename__ = "organization_membership"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # The member's user information
    # NOTE: This defines a one-to-many relationship between the user and organization membership tables.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["UserEntity"] = relationship(back_populates="memberships")

    # Organization that the member is a part of
    # NOTE: This defines a one-to-many relationship between the organization and organization membership tables.
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), primary_key=True
    )
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="members")

    title: Mapped[str] = mapped_column(String)

    # Organization administrative privileges
    is_admin: Mapped[bool] = mapped_column(Boolean)

    # An optional membership term
    # NOTE: This defines a one-to-one relationship between the term and organization membership tables.
    term_id: Mapped[str | None] = mapped_column(
        ForeignKey("academics__term.id"), nullable=True
    )
    term: Mapped["TermEntity"] = relationship(back_populates="organization_memberships")

    @classmethod
    def from_model(cls, model: OrganizationMembership) -> Self:
        """Create an OrganizationMembershipEntity from an OrganizationMember model."""
        return cls(
            id=model.id,
            user_id=model.user.id,
            organization_id=model.organization_id,
            title=model.title,
            is_admin=model.is_admin,
            term_id=model.term.id if model.term else None,
        )

    def to_model(self) -> OrganizationMembership:
        """Create an OrganizationMember model from an OrganizationMembershipEntity."""
        return OrganizationMembership(
            id=self.id,
            user=self.user.to_model(),
            organization_id=self.organization_id,
            organization_name=self.organization.name,
            organization_slug=self.organization.slug,
            title=self.title,
            is_admin=self.is_admin,
            term=self.term.to_model() if self.term else None,
        )
