"""Definition of SQLAlchemy table-backed object mapping entity for Roles."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from .user_role_table import user_role_table
from ..models import Role, RoleDetails

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RoleEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Role` table"""

    # Name for the role table in the PostgreSQL database
    __tablename__ = "role"

    # Unique ID for the role entry
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Name of the role
    name: Mapped[str] = mapped_column(String, unique=True)

    # All of the users with the given role.
    # NOTE: This field establishes a many-to-many relationship between the roles and users table.
    #       and uses the "user_role" table as the join table.
    users: Mapped[list["UserEntity"]] = relationship(
        secondary=user_role_table, back_populates="roles"
    )

    # All of the permissions with the given role.
    # NOTE: This field establishes a one-to-many relationship between the permissions and roles table.
    permissions: Mapped[list["PermissionEntity"]] = relationship(back_populates="role")

    @classmethod
    def from_model(cls, model: Role) -> Self:
        """
        Create a RoleEntity from a Role model.

        Args:
            model (Role): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """
        return cls(id=model.id, name=model.name)

    def to_model(self) -> Role:
        """
        Create a Role model from a RoleEntity.

        Returns:
            Role: A Role model for API usage.
        """
        return Role(id=self.id, name=self.name)

    def to_details_model(self) -> RoleDetails:
        """
        Create a RoleDetails model from a RoleEntity, with permissions and members included.

        Returns:
            RoleDetails: A RoleDetails model for API usage.
        """
        return RoleDetails(
            id=self.id,
            name=self.name,
            permissions=[permission.to_model() for permission in self.permissions],
            users=[user.to_model() for user in self.users],
        )
