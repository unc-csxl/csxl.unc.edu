from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from backend.entities.entity_base import EntityBase

from backend.models.org_role import OrgRoleDetail, OrgRole

from datetime import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OrgRoleEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Role` table"""

    __tablename__ = "org_role"

    # Unique ID for the role
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # User ID for the role
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    # OrganizationDetail ID for the role
    org_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), primary_key=True)
    # Type of membership (0 = Member, 1 = Executive, 2 = Manager)
    membership_type: Mapped[int] = mapped_column(Integer)
    # Time of the event
    timestamp: Mapped[datetime] = mapped_column(DateTime)

    # Bi-Directional Relationship Fields
    user: Mapped["UserEntity"] = relationship(
        back_populates="organization_associations"
    )
    organization: Mapped["OrganizationEntity"] = relationship(
        back_populates="user_associations"
    )

    @classmethod
    def from_model(cls, model: OrgRoleDetail) -> Self:
        """
        Class method that converts a `Role` object into a `RoleEntity`

        Parameters:
            - model (Role): Model to convert into an entity

        Returns:
            RoleEntity: Entity created from model
        """
        return cls(
            id=model.id,
            user_id=model.user_id,
            org_id=model.org_id,
            membership_type=model.membership_type,
            timestamp=model.timestamp,
        )

    def to_model(self) -> OrgRoleDetail:
        """
        Converts a `OrgRoleEntity` object into a `OrgRoleDetail`

        Returns:
            OrgRoleDetail: `OrgRoleDetail` object from the entity
        """
        return OrgRoleDetail(
            id=self.id,
            user_id=self.user_id,
            org_id=self.org_id,
            membership_type=self.membership_type,
            timestamp=self.timestamp,
            organization=self.organization.to_summary(),
            user=self.user.to_summary(),
        )

    def to_summary(self) -> OrgRole:
        """
        Converts a `OrgRoleEntity` object into a `OrgRole`

        Returns:
            OrgRole: `OrgRole` object from the entity
        """
        return OrgRole(
            id=self.id,
            user_id=self.user_id,
            org_id=self.org_id,
            membership_type=self.membership_type,
            timestamp=self.timestamp,
        )


from backend.entities.user_entity import UserEntity
from backend.entities.organization_entity import OrganizationEntity
