"""Entity for Permissions in the database."""""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from .user_entity import UserEntity
from .role_entity import RoleEntity
from ..models import Permission

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class PermissionEntity(EntityBase):
    """Entity for Permissions in the database."""
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action: Mapped[str] = mapped_column(String)
    resource: Mapped[str] = mapped_column(String)

    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=True)
    role: Mapped[RoleEntity] = relationship(back_populates='permissions')

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    user: Mapped[UserEntity] = relationship(back_populates='permissions')

    @classmethod
    def from_model(cls, model: Permission) -> Self:
        """Create a PermissionEntity from a Permission model.
        
        Args:
            model (Permission): The model to create the entity from.
            
        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            action=model.action,
            resource=model.resource
        )

    def to_model(self) -> Permission:
        """Create a Permission model from a PermissionEntity.
        
        Returns:
            Permission: A Permission model for API usage."""
        return Permission(
            id=self.id,
            action=self.action,
            resource=self.resource
        )
