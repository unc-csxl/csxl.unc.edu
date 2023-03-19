import re
from fastapi import Depends
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Permission
from ..entities import UserEntity, PermissionEntity


class PermissionService:

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def grant(self, grantor: User, permission: Permission) -> bool:
        # To grant a permission, two things must be true:
        # 1. Grantor must have `permission.grant` action permission
        # 2. Grantor must have permission to carry out the permission in question
        if not self.check(grantor, 'permission.grant', permission.action):
            return False
        elif not self.check(grantor, permission.action, permission.resource):
            return False

        # Grant Permission
        permission_entity = PermissionEntity.from_model(permission)
        self._session.add(permission_entity)
        self._session.commit()
        return True

    def revoke(self, revoker: User, permission: Permission) -> bool:
        if permission.id is None:
            return False

        permission_entity = self._session.get(PermissionEntity, permission.id)
        if permission_entity is None:
            return False
        elif not self.check(revoker, 'permission.revoke', f'permission/{permission_entity.id}'):
            return False
        elif not self.check(revoker, permission_entity.action, permission_entity.resource):
            return False

        self._session.delete(permission_entity)
        self._session.commit()
        return True

    def check(self, subject: User, action: str, resource: str) -> bool:
        # Check user permissions
        user_query = select(PermissionEntity).where(
            PermissionEntity.user_id == subject.id)
        user_perms = [p for p in self._session.execute(user_query).scalars()]
        if self._has_permission(user_perms, action, resource):
            return True

        # Check role permissions
        user_entity = self._session.get(UserEntity, subject.id)
        if user_entity == None:
            return False

        role_ids = [role.id for role in user_entity.roles]
        role_query = select(PermissionEntity).where(
            PermissionEntity.role_id.in_(role_ids))
        role_permissions = [
            permission for permission in self._session.execute(role_query).scalars()]
        return self._has_permission(role_permissions, action, resource)

    def _has_permission(self, permissions: list[Permission], action: str, resource: str) -> bool:
        for permission in permissions:
            if self._check_permission(permission, action, resource):
                return True
        return False

    def _check_permission(self, permission: Permission, action: str, resource: str) -> bool:
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
