import re
from fastapi import Depends
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Permission, Role, RoleDetails
from ..entities import UserEntity, PermissionEntity, RoleEntity


class UserPermissionError(Exception):
    def __init__(self, action: str, resource: str):
        super().__init__(
            f'Not authorized to perform `{action}` on `{resource}`')


class PermissionService:

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def get_permissions(self, subject: User) -> list[Permission]:
        user_permissions = self._get_user_permissions(subject)
        roles_permissions = self._get_user_roles_permissions(subject)
        permissions = user_permissions + roles_permissions
        return [permission.to_model() for permission in permissions]

    def grant(self, grantor: User, grantee: User | Role | RoleDetails, permission: Permission) -> bool:
        # To grant a permission, two things must be true:
        # 1. Grantor must have `permission.grant` action permission
        # 2. Grantor must have permission to carry out the permission in question
        self.enforce(grantor, 'permission.grant', permission.action)
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
            raise ValueError('grantee must be User or Role')

        self._session.add(permission_entity)
        self._session.commit()
        return True

    def revoke(self, revoker: User, permission: Permission) -> bool:
        if permission.id is None:
            return False

        permission_entity = self._session.get(PermissionEntity, permission.id)
        if permission_entity is None:
            return False

        self.enforce(revoker, 'permission.revoke', f'permission/{permission_entity.id}')
        self.enforce(revoker, permission_entity.action, permission_entity.resource)

        self._session.delete(permission_entity)
        self._session.commit()
        return True

    def enforce(self, subject: User, action: str, resource: str) -> None:
        if self.check(subject, action, resource) is False:
            raise UserPermissionError(action, resource)

    def check(self, subject: User, action: str, resource: str) -> bool:
        # Check user permissions
        user_perms = self._get_user_permissions(subject)
        if self._has_permission(user_perms, action, resource):
            return True

        # Check role permissions
        role_permissions = self._get_user_roles_permissions(subject)
        return self._has_permission(role_permissions, action, resource)

    def _get_user_permissions(self, subject: User) -> list[PermissionEntity]:
        user_query = select(PermissionEntity).where(
            PermissionEntity.user_id == subject.id)
        user_perms = [p for p in self._session.execute(user_query).scalars()]
        return user_perms

    def _get_user_roles_permissions(self, subject: User) -> list[PermissionEntity]:
        user_entity = self._session.get(UserEntity, subject.id)
        if user_entity == None:
            return []
        role_ids = [role.id for role in user_entity.roles]
        if len(role_ids) == 0:
            return []
        role_query = select(PermissionEntity).where(
            PermissionEntity.role_id.in_(role_ids))
        return [p for p in self._session.execute(role_query).scalars()]

    def _has_permission(self, permissions: list[PermissionEntity], action: str, resource: str) -> bool:
        for permission in permissions:
            if self._check_permission(permission, action, resource):
                return True
        return False

    def _check_permission(self, permission: PermissionEntity, action: str, resource: str) -> bool:
        action_re = self._expand_pattern(permission.action)
        if action_re.fullmatch(action) is not None:
            resource_re = self._expand_pattern(permission.resource)
            return resource_re.fullmatch(resource) is not None
        else:
            return False

    @lru_cache()
    def _expand_pattern(self, pattern: str) -> re.Pattern:
        search = pattern.replace('*', '.*')
        return re.compile(f'^{search}$')
