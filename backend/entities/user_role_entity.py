from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from models import User
from typing import Self
from .entity_base import EntityBase

class UserRole(EntityBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    onyen: Mapped[str] = mapped_column(String(32), unique=True, index=True)