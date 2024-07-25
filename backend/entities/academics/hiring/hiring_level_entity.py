"""Definition of SQLAlchemy table-backed object mapping entity for hiring levels."""

from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum

from ...entity_base import EntityBase
from ....models.academics.hiring.hiring_level import HiringLevelClassification

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringLevelEntity(EntityBase):
    """Serves as the database model schema defining the shape of the hiring level table"""

    # Name for the review table in the PostgreSQL database
    __tablename__ = "academics__hiring__level"

    # Properties (columns in the database table)

    # Unique ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Level title
    title: Mapped[str] = mapped_column(String)
    # Level salary
    salary: Mapped[float] = mapped_column(Float)
    # Load (decimal number that ranks salary compared to other levels)
    load: Mapped[float] = mapped_column(Float)
    # Classification (IOR, PhD, MS, UG)
    classification: Mapped[HiringLevelClassification] = mapped_column(
        SQLAlchemyEnum(HiringLevelClassification),
        nullable=False,
    )
    # Is active - Determines whether the hiring level is still used
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Assignments made with this level
    # NOTE: This defines a one-to-many relationship between the assignment and level tables.
    hiring_assignments: Mapped[list["HiringAssignmentEntity"]] = relationship(
        back_populates="hiring_level"
    )
