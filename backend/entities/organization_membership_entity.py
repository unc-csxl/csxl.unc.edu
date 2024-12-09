"""Definition of SQLAlchemy table-backed object mapping entity for Organization Members."""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models import OrganizationMembership, OrganizationRole

# from ..models.organization_join_status import OrganizationJoinStatus


class OrganizationMembershipEntity(EntityBase):

    __tablename__ = "organization_membership"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # The member's user information
    # NOTE: This defines a one-to-many relationship between the user and organization_member tables.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["UserEntity"] = relationship(back_populates="memberships")

    # Organization that the member is a part of
    # NOTE: This defines a one-to-many relationship between the organization and organization_member tables.
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), primary_key=True
    )
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="members")

    organization_role: Mapped[OrganizationRole] = mapped_column(
        SQLAlchemyEnum(OrganizationRole)
    )

    @classmethod
    def from_model(cls, model: OrganizationMembership) -> Self:
        """Create an OrganizationMembershipEntity from an OrganizationMember model."""
        return cls(
            id=model.id,
            user_id=model.user.id,
            organization_id=model.organization_id,
            organization_role=model.organization_role,
        )

    def to_model(self) -> OrganizationMembership:
        """Create an OrganizationMember model from an OrganizationMembershipEntity."""
        return OrganizationMembership(
            id=self.id,
            user=self.user.to_model(),
            organization_id=self.organization.to_model().id,
            organization_slug=self.organization.to_model().slug,
            organization_role=self.organization_role,
        )
