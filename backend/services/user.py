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
    
    def getAll(self) -> list[User]:
        """
        Retrieves all users from the table

        Returns:
            list[User]: List of all `Users`
        """
        # Select all entries in `User` table
        query = select(UserEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def list(self, subject: User, pagination_params: PaginationParams) -> Paginated[User]:
        """
        Retrieves users in a paginated format that match a query

        Parameters:
            pagination_params (pagination_params): Contains pagination details including query and page size
        Returns:
            Paginated[User]: Object that contains matching users in a paginated format
        """
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
        """
        Creates a user based on the input object and adds it to the table.
        If the user's ID is unique to the table, a new entry is added.
        If the user's ID already exists in the table, the existing entry is updated.

        Parameters:
            user (User): User to add to table
        Returns:
            User: Object added to table
        """
        if user.id:
            entity = self._session.get(UserEntity, user.id)
            entity.update(user)
        else:
            entity = UserEntity.from_model(user)
            self._session.add(entity)
        self._session.commit()
        return entity.to_model()
    
    
    def delete(self, pid: int) -> None:
        """
        Delete the user based on the provided PID.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            pid (int): Unique user PID
        """

        # Find user to delete
        user=self._session.query(UserEntity).filter(UserEntity.pid == pid).first()

        # Ensure object exists
        if user:
            # Delete object and commit
            self._session.delete(user)
            self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No user found with PID: {pid}")
