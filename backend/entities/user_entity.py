"""User accounts for all registered users in the application."""


from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from .user_role_entity import user_role_table
from ..models import User


__authors__ = ['Kris Jordan']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'


class UserEntity(EntityBase):
    """Entity for Users in the database."""

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    onyen: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    email: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False, default=''
    )
    first_name: Mapped[str] = mapped_column(
        String(64), nullable=False, default='')
    last_name: Mapped[str] = mapped_column(
        String(64), nullable=False, default='')
    pronouns: Mapped[str] = mapped_column(
        String(32), nullable=False, default='')
    github: Mapped[str] = mapped_column(
        String(32), nullable=False, default='')
    github_id: Mapped[int] = mapped_column(
        Integer, nullable=True)
    github_avatar: Mapped[str] = mapped_column(
        String(), nullable=True)

    roles: Mapped[list['RoleEntity']] = relationship(
        secondary=user_role_table, back_populates='users')
    permissions: Mapped['PermissionEntity'] = relationship(
        back_populates='user')

    @classmethod
    def from_model(cls, model: User) -> Self:
        """Create a UserEntity from a User model.
        
        Args:
            model (User): The model to create the entity from.
            
        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            pid=model.pid,
            onyen=model.onyen,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            pronouns=model.pronouns,
            github=model.github,
            github_id=model.github_id,
            github_avatar=model.github_avatar,
        )

    def to_model(self) -> User:
        """Create a User model from a UserEntity.
        
        Returns:
            User: A User model for API usage."""
        return User(
            id=self.id,
            pid=self.pid,
            onyen=self.onyen,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            github=self.github,
            github_id=self.github_id,
            github_avatar=self.github_avatar,
            pronouns=self.pronouns,
        )

    def update(self, model: User) -> None:
        """Update a UserEntity from a User model.
        
        Args:
            model (User): The model to update the entity from.
            
        Returns:
            None"""
        self.email = model.email
        self.first_name = model.first_name
        self.last_name = model.last_name
        self.pronouns = model.pronouns
        self.github = model.github
        self.github_id = model.github_id
        self.github_avatar = model.github_avatar
