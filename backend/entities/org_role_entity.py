"""Definitions of SQLAlchemy table-backed object mappings called entities."""


from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Self
from backend.entities.entity_base import EntityBase

from backend.models.org_role import OrgRole

class OrgRoleEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Role` table"""

    __tablename__ = "org_role"

    # Unique ID for the role
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # User ID for the role
    user_id: Mapped[int] = mapped_column(Integer)
    # Organization ID for the role
    org_id: Mapped[int] = mapped_column(Integer)
    # Type of membership (0 = Member, 1 = Executive, 2 = Manager)
    membership_type: Mapped[int] = mapped_column(Integer)

    @classmethod
    def from_model(cls, model: OrgRole) -> Self:
        """
        Class method that converts a `Role` object into a `RoleEntity`
        
        Parameters:
            - model (Role): Model to convert into an entity

        Returns:
            RoleEntity: Entity created from model
        """
        return cls(id=model.id, user_id=model.user_id, org_id=model.org_id, membership_type=model.membership_type)

    def to_model(self) -> OrgRole:
        """
        Converts a `RoleEntity` object into a `Role`
        
        Returns:
            Role: `Role` object from the entity
        """
        return OrgRole(id=self.id, user_id=self.user_id, org_id=self.org_id, membership_type=self.membership_type)
