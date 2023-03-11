"""User accounts for all registered users in the application."""


from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from models import User
from typing import Self
from .entity_base import EntityBase


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UserEntity(EntityBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pid: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    onyen: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    email: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False, default=""
    )
    first_name: Mapped[str] = mapped_column(
        String(64), nullable=False, default="")
    last_name: Mapped[str] = mapped_column(
        String(64), nullable=False, default="")
    pronouns: Mapped[str] = mapped_column(
        String(32), nullable=False, default="")

    @classmethod
    def from_model(cls, model: User) -> Self:
        return cls(
            id=model.id,
            pid=model.pid,
            onyen=model.onyen,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            pronouns=model.pronouns,
        )

    def to_model(self) -> User:
        return User(
            id=self.id,
            pid=self.pid,
            onyen=self.onyen,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            pronouns=self.pronouns,
        )

    def update(self, model: User) -> None:
        self.email = model.email
        self.first_name = model.first_name
        self.last_name = model.last_name
        self.pronouns = model.pronouns
