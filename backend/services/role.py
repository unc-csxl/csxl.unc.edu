"""
Role Service is primarily for the administration of roles and their members and permissions.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Role, RoleDetails, Permission
from ..entities import RoleEntity, PermissionEntity, UserEntity
from .permission import PermissionService

class RoleService:
    """RoleService is the access layer to the role data model, its members, and permissions."""

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        """Initialize a new RoleService instance.

        Both arguments are optional and will be typically be injected.

        Args:
            session (Session, optional): The SQLAlchemy session to use.
            permission (PermissionService, optional): The PermissionService contains the logic for User and Role permission granting and checking.
        """
        self._session = session
        self._permission = permission

    def list(self, subject: User) -> list[Role]:
        """List all roles in the system for administrators.

        Args:
            subject (User): The user making the request.

        Returns:
            list[Role]: A list of all roles in the system."""
        self._permission.enforce(subject, 'role.list', 'role/')
        stmt = select(RoleEntity).order_by(RoleEntity.name)
        role_entities = self._session.execute(stmt).scalars()
        return [role_entity.to_model() for role_entity in role_entities]

    def create(self, subject: User, name: str) -> Role:
        """Create a new role in the system.
        
        Args:
            subject (User): The user making the request.
            name (str): The name of the new role.
            
        Returns:
            Role: the newly created role with an ID"""
        self._permission.enforce(subject, 'role.create', 'role/')
        role_entity = RoleEntity(name=name)
        self._session.add(role_entity)
        self._session.commit()
        return role_entity.to_model()

    def details(self, subject: User, id: int) -> RoleDetails:
        """Get details about a specific role in the system for administrators.

        Args:
            subject (User): The user making the request.
            id (int): The id of the Role to retrieve details about.

        Returns:
            RoleDetails: The details of the role."""
        self._permission.enforce(subject, 'role.details', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        return role.to_details_model()

    def grant_permission(self, subject: User, id: int, permission: Permission) -> RoleDetails:
        """Grant a permission to a role.

        Args:
            subject (User): The user making the request.
            id (int): The id of the Role to grant the permission to.

        Returns:
            RoleDetails: The details of the role."""
        self._permission.enforce(subject, 'role.grant_permission', f'role/{id}')
        role = self.details(subject, id)
        self._permission.grant(subject, role, permission)
        return self.details(subject, id)

    def revoke_permission(self, subject: User, id: int, permissionId: int) -> bool:
        """Revoke a permission from a role.

        Args:
            subject (User): The user making the request.
            id (int): The id of the Role to revoke the permission from.
            permissionId (int): The id of the Permission to revoke.

        Returns:
            bool: True if the permission was revoked."""
        self._permission.enforce(subject, 'role.revoke_permission', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        permission = self._session.get(PermissionEntity, permissionId)
        assert role is permission.role
        self._permission.revoke(subject, permission)
        return True

    def add_member(self, subject: User, id: int, member: User) -> RoleDetails:
        """Add a member to a role.

        Args:
            subject (User): The user making the request.
            id (int): The id of the Role to add the member to.
            member (User): The user to add to the role.

        Returns:
            RoleDetails: The details of the role."""
        self._permission.enforce(subject, 'role.add_member', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        user = self._session.get(UserEntity, member.id)
        if user:
            role.users.append(user)
            self._session.commit()
        return self.details(subject, id)

    def is_member(self, subject: User, id: int, userId: int) -> bool:
        """Check if a user is a member of a role.

        Args:
            subject (User): The user making the request.
            id (int): The id of the Role to check.
            userId (int): The id of the User to check.

        Returns:
            bool: True if the user is a member of the role."""
        self._permission.enforce(subject, 'role.details', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        user = self._session.get(UserEntity, userId)
        return user in role.users

    def remove_member(self, subject: User, id: int, userId: int):
        """Remove a member from a role.

        Args:
            subject (User): The user making the request.
            id (int): The id of the Role to remove the member from.
            userId (int): The id of the User to remove from the role.

        Returns:
            bool: True if the user was removed from the role."""
        self._permission.enforce(subject, 'role.remove_member', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        user = self._session.get(UserEntity, userId)
        role.users.remove(user)
        self._session.commit()
        return True
