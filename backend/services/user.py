"""User Service.

The User Service provides access to the User model and its associated database operations.
"""

from fastapi import Depends
from sqlalchemy import select, or_, func, cast, String
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, UserDetails, Paginated, PaginationParams, PublicUser
from ..entities import UserEntity
from .exceptions import ResourceNotFoundException
from .permission import PermissionService

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UserService:
    _session: Session
    _permission: PermissionService

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
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
            user_fields["permissions"] = self._permission.get_permissions(user)
            user_details = UserDetails(**user_fields)
            return user_details

    def get_by_id(self, id: int) -> User:
        """Get a User by their id.

        Args:
            id: The ID of the user.

        Returns:
            User

        Raises:
            ResourceNotFoundException if the User ID is not found
        """
        user_entity = self._session.get(UserEntity, id)
        if user_entity is None:
            raise ResourceNotFoundException(f"User with {id} not found")

        return user_entity.to_model()

    def get_by_onyen(self, subject: User, onyen: str) -> PublicUser:
        """Get a User by their onyen.

        Args:
            onyen: The onyen of the user.

        Returns:
            PublicUser

        Raises:
            ResourceNotFoundException if the User ID is not found
        """
        user_query = select(UserEntity).where(UserEntity.onyen == onyen)
        user_entity = self._session.scalars(user_query).one_or_none()
        if user_entity is None:
            raise ResourceNotFoundException(f"User with {id} not found")

        return user_entity.to_public_model()

    def get_by_pid(self, subject: User, pid: str) -> PublicUser:
        """Get a User by their pid.

        Args:
            onyen: The pid of the user.

        Returns:
            PublicUser

        Raises:
            ResourceNotFoundException if the User ID is not found
        """
        user_query = select(UserEntity).where(UserEntity.pid == pid)
        user_entity = self._session.scalars(user_query).one_or_none()
        if user_entity is None:
            raise ResourceNotFoundException(f"User with {id} not found")

        return user_entity.to_public_model()

    def search(self, _subject: User, query: str) -> list[User]:
        """Search for users by their name, onyen, email.

        Args:
            subject: The user performing the action.
            query: The search query.

        Returns:
            list[User]: The list of users matching the query.
        """
        # First attempt: Query for users by name, onyen, or PID from start of string
        statement = (
            select(UserEntity)
            .where(
                or_(
                    func.concat(UserEntity.first_name, " ", UserEntity.last_name).ilike(
                        f"{query}%"
                    ),
                    UserEntity.last_name.ilike(f"{query}%"),
                    UserEntity.onyen.ilike(f"{query}%"),
                    cast(UserEntity.pid, String).ilike(f"{query}%"),
                )
            )
            .order_by(UserEntity.first_name, UserEntity.last_name)
            .limit(50)
        )
        entities = self._session.execute(statement).scalars().all()

        # Second attempt: match in the middle of strings and also search email
        if len(entities) == 0:
            statement = (
                select(UserEntity)
                .where(
                    or_(
                        func.concat(
                            UserEntity.first_name, " ", UserEntity.last_name
                        ).ilike(f"%{query}%"),
                        UserEntity.last_name.ilike(f"%{query}%"),
                        UserEntity.onyen.ilike(f"%{query}%"),
                        UserEntity.email.ilike(f"%{query}%"),
                        cast(UserEntity.pid, String).ilike(f"%{query}%"),
                    )
                )
                .order_by(UserEntity.first_name, UserEntity.last_name)
                .limit(50)
            )
            entities = self._session.execute(statement).scalars().all()

        return [entity.to_model() for entity in entities]

    def list(
        self, subject: User, pagination_params: PaginationParams
    ) -> Paginated[User]:
        """List Users.

        The subject must have the 'user.list' permission on the 'user/' resource.

        Args:
            subject: The user performing the action.
            pagination_params: The pagination parameters.

        Returns:
            Paginated[User]: The paginated list of users.

        Raises:
            PermissionException: If the subject does not have the required permission.
        """
        self._permission.enforce(subject, "user.list", "user/")

        statement = select(UserEntity)
        length_statement = select(func.count()).select_from(UserEntity)
        if pagination_params.filter != "":
            query = pagination_params.filter
            criteria = or_(
                UserEntity.first_name.ilike(f"%{query}%"),
                UserEntity.last_name.ilike(f"%{query}%"),
                UserEntity.onyen.ilike(f"%{query}%"),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != "":
            statement = statement.order_by(
                getattr(UserEntity, pagination_params.order_by)
            )

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(
            items=[entity.to_model() for entity in entities],
            length=length,
            params=pagination_params,
        )

    def create(self, subject: User, user: User) -> User:
        """Create a User.

        If the subject is not the user, the subject must have the `user.create` permission.

        Args:
            subject: The user performing the action.
            user: The user to create.

        Returns:
            The created User.

        Raises:
            PermissionError: If the subject does not have permission to create the user.
        """
        if subject != user:
            self._permission.enforce(subject, "user.create", "user/")
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
            PermissionError: If the subject does not have permission to update the user.
        """
        if subject != user:
            self._permission.enforce(subject, "user.update", f"user/{user.id}")
        entity = self._session.get(UserEntity, user.id)
        entity.update(user)
        self._session.commit()
        return entity.to_model()
