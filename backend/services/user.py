"""User Service.

The User Service provides access to the User model and its associated database operations.
"""

from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, UserDetails, Paginated, PaginationParams
from ..entities import UserEntity
from .permission import PermissionService

__authors__ = ['Kris Jordan']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'


class UserService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        """Initialize the User Service."""
        self._session = session
        self._permission = permission

    def get(self, pid: int) -> UserDetails | None:
        """Get a User by PID.

        Args:
            pid: The PID of the user.

        Returns:
            UserDetails | None: The user or None if not found.
        """
        query = select(UserEntity).where(UserEntity.pid == pid)
        user_entity: UserEntity | None = self._session.scalar(query)
        if user_entity is None:
            return None
        else:
            user = user_entity.to_model()
            user_fields = user.model_dump()
            user_fields['permissions'] = self._permission.get_permissions(user)
            user_details = UserDetails(**user_fields)
            return user_details

    def search(self, _subject: User, query: str) -> list[User]:
        """Search for users by their name, onyen, email.

        Args:
            subject: The user performing the action.
            query: The search query.

        Returns:
            list[User]: The list of users matching the query.
        """
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
        """List Users.

        The subject must have the 'user.list' permission on the 'user/' resource.

        Args:
            subject: The user performing the action.
            pagination_params: The pagination parameters.

        Returns:
            Paginated[User]: The paginated list of users.

        Raises:
            PermissionException: If the subject does not have the required permission."""
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

    def create(self, subject: User, user: User) -> User:
        """Create a User.

        If the subject is not the user, the subject must have the `user.create` permission.

        Args:
            subject: The user performing the action.
            user: The user to create.

        Returns:
            The created User.

        Raises:
            PermissionError: If the subject does not have permission to create the user."""
        if subject != user:
            self._permission.enforce(subject, 'user.create', 'user/')
        entity = UserEntity.from_model(user)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def update(self, subject: User, user: User) -> User:
        """Update a User.

        If the subject is not the user, the subject must have the `user.update` permission.

        Args:
            subject: The user performing the action.
            user: The user to update.

        Returns:
            The updated User.

        Raises:
            PermissionError: If the subject does not have permission to update the user."""
        if subject != user:
            self._permission.enforce(subject, 'user.update', f'user/{user.id}')
        entity = self._session.get(UserEntity, user.id)
        entity.update(user)
        self._session.commit()
        return entity.to_model()
