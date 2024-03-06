"""Definition of SQLAlchemy table-backed object mapping entity for Applications."""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.application import Application

__authors__ = ["Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Application` table"""

    # Name for the applications table in the PostgreSQL database
    __tablename__ = "application"

    # Application properties (columns in the database table)

    # Unique ID for the application
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Courses LA'd for, reference to section_meber

    @classmethod
    def from_model(cls, model: Application) -> Self:
        """
        Class method that converts an `Application` model into a `ApplicationEntity`

        Parameters:
            - model (Application): Model to convert into an entity
        Returns:
            ApplicationEntity: Entity created from model
        """
        return cls(id=model.id)

    def to_model(self) -> Application:
        """
        Converts an `ApplicationEntity` object into an `Application` model object

        Returns:
            Application: `Application` object from the entity
        """
        return Application(id=self.id, video=self.video)
