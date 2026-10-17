"""Service that manages operating hours of the XL."""

from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ...database import db_session
from ...entities.coworking import OperatingHoursEntity
from ...models import User
from ...models.coworking import OperatingHours, TimeRange
from ..exceptions import ResourceNotFoundException
from ..permission import PermissionService
from .exceptions import (
    OperatingHoursCannotDeleteException,
    OperatingHoursCannotOverlapException,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OperatingHoursService:
    """OperatingHoursService is the access layer to the operating hours data model."""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes a new OperatingHoursService.

        Args:
            session (Session, optional): The database session to use, typically injected by FastAPI.
            permission_svc (PermissionService, optional): The backend permission service, injected by FastAPI.
        """
        self._session = session
        self._permission_svc = permission_svc

    def get_by_id(self, id: int) -> OperatingHours:
        """Lookup an Operating Hours object by its id.

        Args:
            id (int): The id of the Operating Hours object to lookup.

        Returns:
            OperatingHours

        Raises:
            ResourceNotFoundException"""
        entity = self._session.get(OperatingHoursEntity, id)
        if entity is None:
            raise ResourceNotFoundException()
        return entity.to_model()

    def schedule(self, time_range: TimeRange) -> list[OperatingHours]:
        """Returns all operating hours of the XL for a given date range.

        Args:
            time_range (TimeRange): The date range to check for matching OperatingHours.

        Returns:
            list[OperatingHours]: All operating hours the XL within the given time_range, including overlaps.
        """
        entities = (
            self._session.query(OperatingHoursEntity)
            .filter(
                OperatingHoursEntity.start <= time_range.end,
                OperatingHoursEntity.end >= time_range.start,
            )
            .order_by(OperatingHoursEntity.start)
            .all()
        )
        return [entity.to_model() for entity in entities]

    def create(self, subject: User, time_range: TimeRange) -> OperatingHours:
        """Create new, open Operating Hours for XL coworking.

        Args:
            subject (User): The user creating the Operating Hours entry.
            time_range (TimeRange): The time which the XL is open for.

        Returns:
            OperatingHours: The persisted object.
        """
        self._permission_svc.enforce(
            subject, "coworking.operating_hours.create", "coworking/operating_hours"
        )

        time_range = TimeRange.model_validate(time_range.model_dump())
        self._lock_schedule()
        self._check_conflicts(time_range)

        entity = OperatingHoursEntity(start=time_range.start, end=time_range.end)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def update(self, subject: User, id: int, time_range: TimeRange) -> OperatingHours:
        """Replace a record's times while retaining its ID and checking other hours.

        Raises permission, not-found, validation, or overlap errors without
        changing the stored interval. An unchanged update is valid.
        """
        self._permission_svc.enforce(
            subject,
            "coworking.operating_hours.update",
            f"coworking/operating_hours/{id}",
        )
        time_range = TimeRange.model_validate(time_range.model_dump())
        self._lock_schedule()
        entity = self._get_for_update(id)
        self._check_conflicts(time_range, exclude_id=id)
        entity.start = time_range.start
        entity.end = time_range.end
        self._session.commit()
        return entity.to_model()

    def _lock_schedule(self) -> None:
        """Serialize schedule mutations until commit/rollback, without blocking readers.

        Lock the table before checking conflicts, including when no hours exist.
        Locking just the edited row cannot prevent concurrent overlapping inserts.
        Every create, update, and delete takes this lock before reading the schedule.
        """
        self._session.execute(
            text("LOCK TABLE coworking__operating_hours IN SHARE ROW EXCLUSIVE MODE")
        )

    def _check_conflicts(self, time_range: TimeRange, exclude_id: int | None = None):
        """Keep the existing inclusive endpoint policy for both create and update."""
        query = self._session.query(OperatingHoursEntity).filter(
            OperatingHoursEntity.start <= time_range.end,
            OperatingHoursEntity.end >= time_range.start,
        )
        if exclude_id is not None:
            query = query.filter(OperatingHoursEntity.id != exclude_id)
        if query.first() is not None:
            self._session.rollback()
            raise OperatingHoursCannotOverlapException(
                "These times conflict with other operating hours."
            )

    def _get_for_update(self, id: int) -> OperatingHoursEntity:
        """Refresh and lock the row before updating or checking deletion eligibility."""
        entity = (
            self._session.query(OperatingHoursEntity)
            .filter(OperatingHoursEntity.id == id)
            .populate_existing()
            .with_for_update()
            .one_or_none()
        )
        if entity is None:
            self._session.rollback()
            raise ResourceNotFoundException(f"Operating hours {id} do not exist.")
        return entity

    def delete(self, subject: User, operating_hours: OperatingHours) -> None:
        """Delete Operating Hours entry from the database.

        Args:
            subject (User): The user deleting the Operating Hours entry.
            operating_hours (OperatingHours): The entry to delete.

        Returns:
            None
        """
        self._permission_svc.enforce(
            subject,
            "coworking.operating_hours.delete",
            f"coworking/operating_hours/{operating_hours.id}",
        )

        if operating_hours.id is None:
            raise ResourceNotFoundException("Operating hours have no persisted ID.")
        self._lock_schedule()
        operating_hours_entity = self._get_for_update(operating_hours.id)
        now = datetime.now(ZoneInfo("America/New_York")).replace(tzinfo=None)
        if operating_hours_entity.start <= now:
            self._session.rollback()
            raise OperatingHoursCannotDeleteException(
                "Only future operating hours can be deleted. Refresh the schedule."
            )
        self._session.delete(operating_hours_entity)
        self._session.commit()
