from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Paginated, PaginationParams
from ..entities import UserEntity
from .permission import PermissionService


class UserService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    def get(self, pid: int) -> User | None:
        query = select(UserEntity).where(UserEntity.pid == pid)
        user_entity: UserEntity = self._session.scalar(query)
        if user_entity is None:
            return None
        else:
            model = user_entity.to_model()
            model.permissions = self._permission.get_permissions(model)
            return model

    def search(self, subject: User, query: str) -> list[User]:
        statement = select(UserEntity)
        criteria = or_(
            UserEntity.first_name.ilike(f'%{query}%'),
            UserEntity.last_name.ilike(f'%{query}%'),
            UserEntity.onyen.ilike(f'%{query}%'),
            UserEntity.email.ilike(f'%{query}%'),
        )
        statement = statement.where(criteria).limit(10)
        entities = self._session.execute(statement).scalars()
        return [entity.to_model() for entity in entities]

    def list(self, subject: User, pagination_params: PaginationParams) -> Paginated[User]:
        self._permission.enforce(subject, 'user.list', 'user/')

        statement = select(UserEntity)
        length_statement = select(func.count()).select_from(UserEntity)
        if pagination_params.filter != '':
            query = pagination_params.filter
            criteria = or_(
                UserEntity.first_name.ilike(f'%{query}%'),
                UserEntity.last_name.ilike(f'%{query}%'),
                UserEntity.onyen.ilike(f'%{query}%'),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != '':
            statement = statement.order_by(
                getattr(UserEntity, pagination_params.order_by))

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(items=[entity.to_model() for entity in entities], length=length, params=pagination_params)

    def save(self, user: User) -> User | None:
        if user.id:
            entity = self._session.get(UserEntity, user.id)
            entity.update(user)
        else:
            entity = UserEntity.from_model(user)
            self._session.add(entity)
        self._session.commit()
        return entity.to_model()
