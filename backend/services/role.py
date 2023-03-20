from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Role, RoleDetails
from ..entities import RoleEntity, PermissionEntity
from .permission import PermissionService


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

    def revoke(self, subject: User, id: int, permissionId: int):
        self._permission.enforce(subject, 'role.revoke', f'role/{id}')
        role = self._session.get(RoleEntity, id)
        permission = self._session.get(PermissionEntity, permissionId)
        assert role is permission.role
        self._session.delete(permission)
        self._session.commit()
        return True