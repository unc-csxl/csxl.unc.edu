"""Service for database-backed standing room reservation blocks."""

from datetime import date, datetime, time, timedelta

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ...database import db_session
from ...entities import RoomEntity
from ...entities.coworking import ReservationEntity, RoomReservationBlockEntity
from ...models import User
from ...models.coworking import (
    NewRoomReservationBlock,
    ReservationState,
    RoomReservationBlock,
    RoomReservationBlockOccurrence,
    TimeRange,
)
from ..exceptions import ResourceNotFoundException
from ..permission import PermissionService
from .exceptions import RoomReservationBlockConflictException


class RoomReservationBlockService:
    """Manage recurring policy blocks for reservable rooms."""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        self._session = session
        self._permission_svc = permission_svc

    def get_by_id(self, id: int) -> RoomReservationBlock:
        entity = self._session.get(RoomReservationBlockEntity, id)
        if entity is None:
            raise ResourceNotFoundException(
                f"Room reservation block with id {id} does not exist."
            )
        return entity.to_model()

    def get(self, subject: User, id: int) -> RoomReservationBlock:
        block = self.get_by_id(id)
        self._permission_svc.enforce(
            subject, "coworking.room_reservation_blocks.read", f"room/{block.room_id}"
        )
        return block

    def list_rules(
        self,
        subject: User,
        room_id: str | None = None,
        include_disabled: bool = False,
    ) -> list[RoomReservationBlock]:
        resource = f"room/{room_id}" if room_id is not None else "room/*"
        self._permission_svc.enforce(
            subject, "coworking.room_reservation_blocks.read", resource
        )

        query = select(RoomReservationBlockEntity)
        if room_id is not None:
            query = query.where(RoomReservationBlockEntity.room_id == room_id)
        if not include_disabled:
            query = query.where(RoomReservationBlockEntity.enabled.is_(True))
        query = query.order_by(
            RoomReservationBlockEntity.room_id,
            RoomReservationBlockEntity.weekday,
            RoomReservationBlockEntity.start_time,
        )
        return [entity.to_model() for entity in self._session.scalars(query).all()]

    def schedule(
        self, value: date | datetime, room_id: str | None = None
    ) -> list[RoomReservationBlockOccurrence]:
        """Expand enabled rules that apply on one local calendar date."""
        target_date = value.date() if isinstance(value, datetime) else value
        query = select(RoomReservationBlockEntity).where(
            RoomReservationBlockEntity.enabled.is_(True),
            RoomReservationBlockEntity.weekday == target_date.weekday(),
            RoomReservationBlockEntity.starts_on <= target_date,
            or_(
                RoomReservationBlockEntity.ends_on.is_(None),
                RoomReservationBlockEntity.ends_on >= target_date,
            ),
        )
        if room_id is not None:
            query = query.where(RoomReservationBlockEntity.room_id == room_id)
        query = query.order_by(
            RoomReservationBlockEntity.room_id,
            RoomReservationBlockEntity.start_time,
        )

        return [
            RoomReservationBlockOccurrence(
                id=entity.id,
                room_id=entity.room_id,
                label=entity.label,
                start=datetime.combine(target_date, entity.start_time),
                end=datetime.combine(target_date, entity.end_time),
            )
            for entity in self._session.scalars(query).all()
        ]

    def find_overlaps(
        self, room_id: str, bounds: TimeRange
    ) -> list[RoomReservationBlockOccurrence]:
        """Return enabled occurrences overlapping an absolute time range."""
        overlaps = []
        target_date = bounds.start.date()
        while target_date <= bounds.end.date():
            for occurrence in self.schedule(target_date, room_id):
                if occurrence.start < bounds.end and occurrence.end > bounds.start:
                    overlaps.append(occurrence)
            target_date += timedelta(days=1)
        return overlaps

    def create(
        self, subject: User, block: NewRoomReservationBlock
    ) -> RoomReservationBlock:
        self._permission_svc.enforce(
            subject, "coworking.room_reservation_blocks.create", f"room/{block.room_id}"
        )
        self._lock_reservable_room(block.room_id)
        self._validate_conflicts(block)

        entity = RoomReservationBlockEntity.from_new_model(block)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def update(
        self, subject: User, id: int, block: NewRoomReservationBlock
    ) -> RoomReservationBlock:
        entity = self._session.get(RoomReservationBlockEntity, id)
        if entity is None:
            raise ResourceNotFoundException(
                f"Room reservation block with id {id} does not exist."
            )

        self._permission_svc.enforce(
            subject,
            "coworking.room_reservation_blocks.update",
            f"room/{entity.room_id}",
        )
        if block.room_id != entity.room_id:
            self._permission_svc.enforce(
                subject,
                "coworking.room_reservation_blocks.update",
                f"room/{block.room_id}",
            )

        self._lock_reservable_room(block.room_id)
        self._validate_conflicts(block, exclude_id=id)

        entity.room_id = block.room_id
        entity.label = block.label
        entity.weekday = block.weekday.value
        entity.start_time = block.start_time
        entity.end_time = block.end_time
        entity.starts_on = block.starts_on
        entity.ends_on = block.ends_on
        entity.enabled = block.enabled
        self._session.commit()
        return entity.to_model()

    def delete(self, subject: User, id: int) -> None:
        entity = self._session.get(RoomReservationBlockEntity, id)
        if entity is None:
            raise ResourceNotFoundException(
                f"Room reservation block with id {id} does not exist."
            )
        self._permission_svc.enforce(
            subject,
            "coworking.room_reservation_blocks.delete",
            f"room/{entity.room_id}",
        )
        self._session.delete(entity)
        self._session.commit()

    def lock_reservable_room(self, room_id: str) -> RoomEntity:
        """Serialize bookings and policy changes for a room."""
        return self._lock_reservable_room(room_id)

    def _lock_reservable_room(self, room_id: str) -> RoomEntity:
        room = self._session.scalar(
            select(RoomEntity)
            .where(RoomEntity.id == room_id, RoomEntity.reservable.is_(True))
            .with_for_update()
        )
        if room is None:
            raise ResourceNotFoundException(
                f"Reservable room with id {room_id} does not exist."
            )
        return room

    def _validate_conflicts(
        self, block: NewRoomReservationBlock, exclude_id: int | None = None
    ) -> None:
        if not block.enabled:
            return

        query = select(RoomReservationBlockEntity).where(
            RoomReservationBlockEntity.enabled.is_(True),
            RoomReservationBlockEntity.room_id == block.room_id,
            RoomReservationBlockEntity.weekday == block.weekday.value,
            RoomReservationBlockEntity.start_time < block.end_time,
            RoomReservationBlockEntity.end_time > block.start_time,
            or_(
                RoomReservationBlockEntity.ends_on.is_(None),
                RoomReservationBlockEntity.ends_on >= block.starts_on,
            ),
        )
        if block.ends_on is not None:
            query = query.where(RoomReservationBlockEntity.starts_on <= block.ends_on)
        if exclude_id is not None:
            query = query.where(RoomReservationBlockEntity.id != exclude_id)

        conflicting_block = self._session.scalars(query).first()
        if conflicting_block is not None:
            raise RoomReservationBlockConflictException(
                f'Conflicts with "{conflicting_block.label}" in {block.room_id}.'
            )

        conflicting_reservation = self._active_reservation_conflict(block)
        if conflicting_reservation is not None:
            raise RoomReservationBlockConflictException(
                f"Conflicts with reservation {conflicting_reservation.id} "
                f"in {block.room_id}."
            )

    def _active_reservation_conflict(
        self, block: NewRoomReservationBlock
    ) -> ReservationEntity | None:
        first_day = datetime.combine(block.starts_on, time.min)
        query = select(ReservationEntity).where(
            ReservationEntity.room_id == block.room_id,
            ReservationEntity.state.in_(
                [
                    ReservationState.DRAFT,
                    ReservationState.CONFIRMED,
                    ReservationState.CHECKED_IN,
                ]
            ),
            ReservationEntity.end > first_day,
        )
        if block.ends_on is not None:
            query = query.where(
                ReservationEntity.start
                < datetime.combine(block.ends_on + timedelta(days=1), time.min)
            )

        for reservation in self._session.scalars(query).all():
            target_date = max(reservation.start.date(), block.starts_on)
            final_date = reservation.end.date()
            if block.ends_on is not None:
                final_date = min(final_date, block.ends_on)
            while target_date <= final_date:
                if target_date.weekday() == block.weekday.value:
                    occurrence_start = datetime.combine(target_date, block.start_time)
                    occurrence_end = datetime.combine(target_date, block.end_time)
                    if (
                        reservation.start < occurrence_end
                        and reservation.end > occurrence_start
                    ):
                        return reservation
                target_date += timedelta(days=1)
        return None
