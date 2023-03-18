from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User
from ..entities import UserEntity

class AccessControlService:

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session 

    def has_permission_to(self, subject: User, action: str, resource: str) -> bool:
        return False