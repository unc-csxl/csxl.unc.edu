from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from models import User
from typing import Self
from .entity_base import EntityBase

class PermissionEntity(EntityBase):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action: Mapped[str] = mapped_column(String)
    resource: Mapped[str] = mapped_column(String)