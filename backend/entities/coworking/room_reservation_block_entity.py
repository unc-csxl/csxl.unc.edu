"""Database entity for standing room reservation blocks."""

from datetime import date, datetime, time
from typing import Self, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...models.coworking import NewRoomReservationBlock, RoomReservationBlock
from ..entity_base import EntityBase

if TYPE_CHECKING:
    from ..room_entity import RoomEntity


class RoomReservationBlockEntity(EntityBase):
    """A weekly policy rule that makes a room unavailable."""

    __tablename__ = "coworking__room_reservation_block"
    __table_args__ = (
        CheckConstraint(
            "weekday BETWEEN 0 AND 6",
            name="coworking__room_reservation_block_weekday_check",
        ),
        CheckConstraint(
            "start_time < end_time",
            name="coworking__room_reservation_block_time_range_check",
        ),
        CheckConstraint(
            "ends_on IS NULL OR ends_on >= starts_on",
            name="coworking__room_reservation_block_date_range_check",
        ),
        CheckConstraint(
            "length(trim(label)) > 0",
            name="coworking__room_reservation_block_label_check",
        ),
        CheckConstraint(
            "EXTRACT(MINUTE FROM start_time) IN (0, 30) "
            "AND EXTRACT(SECOND FROM start_time) = 0 "
            "AND EXTRACT(MINUTE FROM end_time) IN (0, 30) "
            "AND EXTRACT(SECOND FROM end_time) = 0",
            name="coworking__room_reservation_block_half_hour_check",
        ),
        Index(
            "coworking__room_reservation_block_schedule_idx",
            "room_id",
            "weekday",
            "starts_on",
            "ends_on",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[str] = mapped_column(
        String, ForeignKey("room.id", ondelete="RESTRICT"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    weekday: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    room: Mapped["RoomEntity"] = relationship()

    @classmethod
    def from_new_model(cls, model: NewRoomReservationBlock) -> Self:
        """Build an unpersisted entity from a validated model."""
        return cls(
            room_id=model.room_id,
            label=model.label,
            weekday=model.weekday.value,
            start_time=model.start_time,
            end_time=model.end_time,
            starts_on=model.starts_on,
            ends_on=model.ends_on,
            enabled=model.enabled,
        )

    def to_model(self) -> RoomReservationBlock:
        """Convert a persisted entity to its API model."""
        return RoomReservationBlock(
            id=self.id,
            room_id=self.room_id,
            label=self.label,
            weekday=self.weekday,
            start_time=self.start_time,
            end_time=self.end_time,
            starts_on=self.starts_on,
            ends_on=self.ends_on,
            enabled=self.enabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
