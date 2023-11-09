"""
Permission Service grants, revokes, tests, and enforces permissions for users and roles in the system.

This Service is more of an internal service that other services take dependency on. It is not directly
exposed via the API.
"""

import re
from fastapi import Depends
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Permission, Role, RoleDetails
from ..entities import UserEntity, PermissionEntity, RoleEntity
from ..services.exceptions import UserPermissionException

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class PermissionService:
    """PermissionService grants, revokes, tests, and enforces permissions for users and roles in the system."""

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        """Initialize a new PermissionService instance.

        Args:
            session (Session): The SQLAlchemy session to use for database operations."""
        self._session = session

    def get_permissions(self, subject: User) -> list[Permission]:
        """Get the permissions for a user.

        Args:
            subject (User): The user to get permissions for.

        Returns:
            list[Permission]: The permissions for the user."""
        user_permissions = self._get_user_permissions(subject)
        roles_permissions = self._get_user_roles_permissions(subject)
        permissions = user_permissions + roles_permissions
        return [permission.to_model() for permission in permissions]

    def grant(
        self, grantor: User, grantee: User | Role | RoleDetails, permission: Permission
    ) -> bool:
        """Grant a permission to a user or role.

        To grant a permission, two things must be true:

        1. Grantor must have `permission.grant` action permission on the action being granted
        2. Grantor must have permission to carry out the permission being granted

        Args:
            grantor (User): The user granting the permission.
            grantee (User | Role | RoleDetails): The user or role to grant the permission to.
            permission (Permission): The permission to grant.

        Returns:
            bool: True if the permission was granted, False otherwise.

        Raises:
            ValueError: If the grantee is not a User or Role.
            UserPermissionException: If the grantor does not have permission to grant the permission.
        """
        self.enforce(grantor, "permission.grant", permission.action)
        self.enforce(grantor, permission.action, permission.resource)

        # Grant Permission
        permission_entity = PermissionEntity.from_model(permission)
        if type(grantee) is User:
            user_entity = self._session.get(UserEntity, grantee.id)
            permission_entity.user = user_entity
        elif type(grantee) is Role or type(grantee) is RoleDetails:
            role_entity = self._session.get(RoleEntity, grantee.id)
            permission_entity.role = role_entity
        else:
            raise ValueError("grantee must be User or Role")

        self._session.add(permission_entity)
        self._session.commit()
        return True

    def revoke(self, revoker: User, permission: Permission) -> bool:
        """Revoke a permission from a user or role.

        Args:
            revoker (User): The user revoking the permission.
            permission (Permission): The permission to revoke (must have its id attribute assigned).

        Returns:
            bool: True if the permission was revoked, False otherwise.

        Raises:
            UserPermissionException: If the revoker does not have permission to revoke the permission.
        """
        if permission.id is None:
            return False

        permission_entity = self._session.get(PermissionEntity, permission.id)
        if permission_entity is None:
            return False

        self.enforce(revoker, "permission.revoke", f"permission/{permission_entity.id}")
        self.enforce(revoker, permission_entity.action, permission_entity.resource)

        self._session.delete(permission_entity)
        self._session.commit()
        return True

    def enforce(self, subject: User, action: str, resource: str) -> None:
        """Enforce a permission for a user.

        Args:
            subject (User): The user to enforce the permission for.
            action (str): The action to enforce the subject has permission to perform.
            resource (str): The resource to enforce the subject has permission to carry out the action on.

        Returns:
            None

        Raises:
            UserPermissionException: If the subject does not have permission to carry out the action on the resource.
        """
        if self.check(subject, action, resource) is False:
            raise UserPermissionException(action, resource)

    def check(self, subject: User, action: str, resource: str) -> bool:
        """Check if a user has permission to carry out an action on a resource.

        Args:
            subject (User): The user to check permissions for.

        Returns:
            bool: True if the user has permission to carry out the action on the resource, False otherwise.
        """
        # Check user permissions
        user_perms = self._get_user_permissions(subject)
        if self._has_permission(user_perms, action, resource):
            return True

        # Check role permissions
        role_permissions = self._get_user_roles_permissions(subject)
        return self._has_permission(role_permissions, action, resource)

    def _get_user_permissions(self, subject: User) -> list[PermissionEntity]:
        """Get the permissions for a user.

        Args:
            subject (User): The user to get permissions for.

        Returns:
            list[PermissionEntity]: The permissions for the user."""
        user_query = select(PermissionEntity).where(
            PermissionEntity.user_id == subject.id
        )
        user_perms = [p for p in self._session.execute(user_query).scalars()]
        return user_perms

    def _get_user_roles_permissions(self, subject: User) -> list[PermissionEntity]:
        """Get the permissions for a user's roles.

        Args:
            subject (User): The user to get permissions for.

        Returns:
            list[PermissionEntity]: The permissions for the user's roles."""
        user_entity = self._session.get(UserEntity, subject.id)
        if user_entity == None:
            return []
        role_ids = [role.id for role in user_entity.roles]
        if len(role_ids) == 0:
            return []
        role_query = select(PermissionEntity).where(
            PermissionEntity.role_id.in_(role_ids)
        )
        return [p for p in self._session.execute(role_query).scalars()]

    def _has_permission(
        self, permissions: list[PermissionEntity], action: str, resource: str
    ) -> bool:
        """Check if a user has permission to carry out an action on a resource in a list of permissions.

        Args:
            permissions (list[PermissionEntity]): The permissions to check.
            action (str): The action in question.
            resource (str): The resource in question.

        Returns:
            bool: True if the user has permission to carry out the action on the resource, False otherwise.
        """
        for permission in permissions:
            if self._check_permission(permission, action, resource):
                return True
        return False

    def _check_permission(
        self, permission: PermissionEntity, action: str, resource: str
    ) -> bool:
        """Check if a user has permission to carry out an action on a resource.

        Args:
            permission (PermissionEntity): The permission to check.
            action (str): The action in question.
            resource (str): The resource in question.

        Returns:
            bool: True if the user has permission to carry out the action on the resource, False otherwise.
        """
        action_re = self._expand_pattern(permission.action)
        if action_re.fullmatch(action) is not None:
            resource_re = self._expand_pattern(permission.resource)
            return resource_re.fullmatch(resource) is not None
        else:
            return False

    @lru_cache()
    def _expand_pattern(self, pattern: str) -> re.Pattern:
        """Expand a permission pattern into a regular expression.

        This function is memoized to avoid recompiling the same regular expression multiple times.

        Args:
            pattern (str): The pattern to expand.

        Returns:
            re.Pattern: The compiled regular expression."""
        search = pattern.replace("*", ".*")
        return re.compile(f"^{search}$")
