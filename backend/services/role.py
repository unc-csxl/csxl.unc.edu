from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Role, RoleDetails, Permission
from ..entities import RoleEntity, PermissionEntity, UserEntity
from .permission import PermissionService, UserPermissionError


class RoleService:

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    def list(self, subject: User) -> list[Role]:
        self._permission.enforce(subject, 'role.list', 'role/')
        stmt = select(RoleEntity).order_by(RoleEntity.name)
        role_entities = self._session.execute(stmt).scalars()
        return [role_entity.to_model() for role_entity in role_entities]

    def details(self, subject: User, id: int) -> RoleDetails:
        self._permission.enforce(subject, 'role.details', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        return role.to_details_model()

    def grant(self, subject: User, id: int, permission: Permission):
        self._permission.enforce(subject, 'role.grant_permission', f'role/{id}')
        role = self.details(subject, id)
        self._permission.grant(subject, role, permission)
        return self.details(subject, id)

    def revoke(self, subject: User, id: int, permissionId: int):
        self._permission.enforce(subject, 'role.revoke_permission', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        permission = self._session.get(PermissionEntity, permissionId)
        assert role is permission.role
        self._session.delete(permission)
        self._session.commit()
        return True

    def add(self, subject: User, id: int, member: User):
        self._permission.enforce(subject, 'role.add_member', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        user = self._session.get(UserEntity, member.id)
        if user:
            role.users.append(user)
            self._session.commit()
        return self.details(subject, id)

    def remove(self, subject: User, id: int, userId: int):
        self._permission.enforce(subject, 'role.remove_member', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        user = self._session.get(UserEntity, userId)
        role.users.remove(user)
        self._session.commit()
        return True