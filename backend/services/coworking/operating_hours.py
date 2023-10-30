"""Service that manages operating hours of the XL."""

from fastapi import Depends
from sqlalchemy.orm import Session
from .exceptions import OperatingHoursCannotOverlapException
from ..permission import PermissionService
from ...models import User
from ...database import db_session
from ...models.coworking import OperatingHours, TimeRange
from ...entities.coworking import OperatingHoursEntity

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
            time_range (TimeRange): The time which the XL is open for.

        Returns:
            OperatingHours: The persisted object.
        """
        self._permission_svc.enforce(
            subject, "coworking.operating_hours.create", "coworking/operating_hours"
        )

        conflicts = self.schedule(time_range)
        if len(conflicts) > 0:
            raise OperatingHoursCannotOverlapException(
                f"Conflicts in the range of {str(time_range)}"
            )

        entity = OperatingHoursEntity(start=time_range.start, end=time_range.end)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()
