"""Entity for Operating Hours Recurrence.""" ""

from sqlalchemy import Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.coworking.operating_hours import (
    OperatingHoursRecurrence,
)
from ..entity_base import EntityBase
from ...models.coworking import OperatingHours
from datetime import datetime
from typing import Self

__authors__ = ["David Foss"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OperatingHoursRecurrenceEntity(EntityBase):
    """Entity for Operating Hours Recurrence."""

    __tablename__ = "coworking__operating_hours_recurrence"
    __table_args__ = (
        Index("coworking__operating_hours_recurrence_idx", "end_date", unique=False),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, index=True)

    recurs_on: Mapped[int] = mapped_column(Integer)

    def to_model(self) -> OperatingHoursRecurrence:
        """Converts the entity to a model.

        Returns:
            OperatingHoursRecurrence: The model representation of the entity."""
        return OperatingHoursRecurrence(
            id=self.id, end_date=self.end_date, recurs_on=self.recurs_on
        )

    @classmethod
    def from_model(cls, model: OperatingHoursRecurrence) -> Self:
        """Create an OperatingHoursRecurrenceEntity from a OperatingHoursRecurrence model.

        Args:
            model (OperatingHoursRecurrence): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            end_date=model.end_date,
            recurs_on=model.recurs_on,
        )
