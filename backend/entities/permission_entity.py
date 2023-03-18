from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from .user_entity import UserEntity
from .role_entity import RoleEntity
from models import Permission
from typing import Self


class PermissionEntity(EntityBase):
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
        return cls(
            id=model.id,
            action=model.action,
            resource=model.resource,
            user_id=model.user.id if model.user else None,
            role_id=model.role.id if model.role else None
        )

    def to_model(self) -> Permission:
        return Permission(
            id=self.id,
            action=self.action,
            resource=self.resource,
            role=self.role.to_model() if self.role else None,
            user=self.user.to_model() if self.user else None
        )
