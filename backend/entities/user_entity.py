"""Definition of SQLAlchemy table-backed object mapping entity for Users."""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self

from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.models.academics.section_member import SectionMember
from .entity_base import EntityBase
from .user_role_table import user_role_table
from ..models import User, PublicUser

__authors__ = ["Kris Jordan", "Matt Vu"]
__copyright__ = "Copyright 2023 - 2024"
__license__ = "MIT"


class UserEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `User` table"""

    # Name for the user table in the PostgreSQL database
    __tablename__ = "user"

    # Unique ID for the user entry
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # PID of the user (should be unique per user)
    pid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    # ONYEN of the user
    onyen: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    # Email of the user
    email: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False, default=""
    )
    # First name of the user
    first_name: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    # Last name of the user
    last_name: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    # Pronouns of the user
    pronouns: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    # GitHub username of the user
    github: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    # GitHub ID of the user
    github_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # GitHub Avatar permalink for the user
    github_avatar: Mapped[str | None] = mapped_column(String(), nullable=True)
    # Checks whether or not the user has accepted community agreement
    accepted_community_agreement: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    # Bio of the user
    bio: Mapped[str | None] = mapped_column(String(), nullable=True)

    # All of the roles for the given user.
    # NOTE: This field establishes a many-to-many relationship between the users and roles table.
    #       and uses the "user_role" table as the join table.
    roles: Mapped[list["RoleEntity"]] = relationship(
        secondary=user_role_table, back_populates="users"
    )

    # The permissions for the given user.
    # NOTE: This field establishes a one-to-many relationship between the permission and users table.
    permissions: Mapped["PermissionEntity"] = relationship(back_populates="user")

    # Section relations that the user is a part of.
    sections: Mapped[list["SectionMemberEntity"]] = relationship(
        back_populates="user"
    )  ### This handles previous sections

    # The applications for the  user.
    applications: Mapped[list["ApplicationEntity"]] = relationship(
        back_populates="user"
    )

    @classmethod
    def from_model(cls, model: User) -> Self:
        """
        Create a UserEntity from a User model.

        Args:
            model (User): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """
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
            accepted_community_agreement=model.accepted_community_agreement,
            bio=model.bio,
        )

    def to_model(self) -> User:
        """
        Create a User model from a UserEntity.

        Returns:
            User: A User model for API usage.
        """
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
            accepted_community_agreement=self.accepted_community_agreement,
            bio=self.bio,
        )

    def update(self, model: User) -> None:
        """
        Update a UserEntity from a User model.

        Args:
            model (User): The model to update the entity from.

        Returns:
            None
        """
        self.email = model.email
        self.first_name = model.first_name
        self.last_name = model.last_name
        self.pronouns = model.pronouns
        self.github = model.github
        self.github_id = model.github_id or None
        self.github_avatar = model.github_avatar or ""
        self.accepted_community_agreement = model.accepted_community_agreement
        self.bio = model.bio

    def to_public_model(self) -> PublicUser:
        return PublicUser(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            pronouns=self.pronouns,
            email=self.email,
            github_avatar=self.github_avatar,
            bio=self.bio,
        )
