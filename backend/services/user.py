from fastapi import Depends
from database import db_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from entities import UserEntity

class UserService:

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def get(self, pid: int) -> User | None:
        query = select(UserEntity).where(UserEntity.pid == pid)
        user_entity: UserEntity = self._session.scalar(query)
        return user_entity.to_model() if user_entity else None

    def save(self, user: User) -> User | None:

        if user.id:
            entity = self._session.get(UserEntity, user.id)
            entity.update(user)
        else:
            entity = UserEntity.from_model(user)
            self._session.add(entity)
        self._session.commit()
        return entity.to_model()