"""Definition of SQLAlchemy table-backed object mapping entity for Organization Members."""

from sqlalchemy import Integer, Boolean, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.organization_membership import (
    OrganizationMembership,
    OrganizationMembershipRegistration,
    OrganizationPermissionLevel,
    OrganizationMembershipStatus,
)


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

    # Membership title, default value of "Member"
    title: Mapped[str] = mapped_column(String, default="Member")

    # Level of administrative privileges in organization
    permission_level: Mapped["OrganizationPermissionLevel"] = mapped_column(
        SQLAlchemyEnum(OrganizationPermissionLevel),
        default=OrganizationPermissionLevel.MEMBER,
    )

    # Membership status
    status: Mapped["OrganizationMembershipStatus"] = mapped_column(
        SQLAlchemyEnum(OrganizationMembershipStatus)
    )

    # Membership term, default value of the current academic term
    # NOTE: This defines a one-to-many relationship between the term and organization membership tables.
    term_id: Mapped[str] = mapped_column(ForeignKey("academics__term.id"))
    term: Mapped["TermEntity"] = relationship(back_populates="organization_memberships")

    @classmethod
    def from_model(
        cls, model: OrganizationMembership | OrganizationMembershipRegistration
    ) -> Self:
        """Create an OrganizationMembershipEntity from an OrganizationMembership model or Registration model."""
        if isinstance(model, OrganizationMembership):
            return cls(
                id=model.id,
                user_id=model.user.id,
                organization_id=model.organization_id,
                title=model.title,
                permission_level=model.permission_level,
                status=model.status,
                term_id=model.term.id,
            )
        else:
            return cls(
                id=model.id,
                user_id=model.user_id,
                organization_id=model.organization_id,
                title=model.title,
                permission_level=model.permission_level,
                status=model.status,
                term_id=model.term_id,
            )

    def to_model(self) -> OrganizationMembership:
        """Create an OrganizationMembership model from an OrganizationMembershipEntity."""
        return OrganizationMembership(
            id=self.id,
            user=self.user.to_public_model(),
            organization_id=self.organization_id,
            organization_name=self.organization.name,
            organization_slug=self.organization.slug,
            title=self.title,
            permission_level=self.permission_level,
            status=self.status,
            term=self.term.to_model(),
        )
