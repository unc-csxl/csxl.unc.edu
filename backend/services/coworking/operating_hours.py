"""Service that manages operating hours of the XL."""

from datetime import datetime, time, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.models.coworking.operating_hours import OperatingHoursDraft
from .exceptions import OperatingHoursCannotOverlapException
from ..exceptions import ResourceNotFoundException
from ..permission import PermissionService
from ...models import User
from ...database import db_session
from ...models.coworking import OperatingHours, TimeRange
from ...entities.coworking import OperatingHoursEntity

__authors__ = ["Kris Jordan", "Tobenna Okoli"]
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

    def create(
        self, subject: User, operating_hours_draft: OperatingHoursDraft
    ) -> OperatingHours:
        """Create new, open Operating Hours for XL coworking.

        Args:
            subject (User): The user creating the Operating Hours entry.
            operating_Hours (OperatingHoursDraft): A draft of the operating hours to be created.

        Returns:
            OperatingHours: The persisted object.
        """
        self._permission_svc.enforce(
            subject, "coworking.operating_hours.create", "coworking/operating_hours"
        )

        if len(self.schedule(operating_hours_draft)) > 0:
            raise OperatingHoursCannotOverlapException(
                f"Conflicts in the range of {str(operating_hours_draft)}"
            )

        operating_hours = OperatingHoursEntity.from_draft(operating_hours_draft)
        self._session.add(operating_hours)

        recurrence = operating_hours.recurrence
        if operating_hours_draft.recurrence:

            operating_hours_to_create = []

            start_date = operating_hours_draft.start.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=operating_hours_draft.recurrence.end_date.tzinfo,
            )

            # Go through every day between the start date and end date(inclusive)
            # https://stackoverflow.com/a/24637447

            for day in [
                start_date + timedelta(days=x)
                for x in range(
                    1,
                    (operating_hours_draft.recurrence.end_date - start_date).days + 1,
                )
            ]:
                # If date is in recurrence, create a new operating hours object for that day
                if (1 << day.weekday()) & operating_hours_draft.recurrence.recurs_on:
                    start = datetime.combine(day, operating_hours_draft.start.time())
                    end = datetime.combine(day, operating_hours_draft.end.time())
                    operating_hours_to_create.append(
                        OperatingHoursDraft(start=start, end=end)
                    )

            for operating_hours in operating_hours_to_create:
                conflicts = self.schedule(operating_hours)
                if len(conflicts) > 0:
                    raise OperatingHoursCannotOverlapException(
                        f"Conflicts in the range of {str(operating_hours)}"
                    )

            entities = [
                OperatingHoursEntity.from_draft(operating_hours)
                for operating_hours in operating_hours_to_create
            ]

            for entity in entities:
                entity.recurrence = recurrence
                print(recurrence)
            self._session.add_all(entities)
        self._session.commit()

        # Return first operating hour
        # I believe this isn't used anywhere on the frontend yet
        # Might be worth switching to returning an array, however that might lead to weird behavior when not doing recurrence
        return entities[0].to_model()

    def update(
        self,
        subject: User,
        newest_operating_hours: OperatingHoursDraft,
    ) -> OperatingHours:
        """Update existing, open Operating Hours for XL coworking.

        Args:
            subject (User): The user updating the Operating Hours entry.
            newest_operating_hours (OperatingHours): object containing the id of the entity to update and the new operating hours.

        Returns:
            OperatingHours: The persisted object.
        """
        self._permission_svc.enforce(
            subject, "coworking.operating_hours.update", "coworking/operating_hours"
        )

        new_time_range = TimeRange(
            start=newest_operating_hours.start, end=newest_operating_hours.end
        )
        all_hours = self.schedule(new_time_range)

        conflicts = [
            opHours
            for opHours in all_hours
            if opHours.id
            != newest_operating_hours.id  # ignore the hours we are currently updating
        ]
        if len(conflicts) > 0:
            raise OperatingHoursCannotOverlapException(
                f"Conflicts in the range of {str(new_time_range)}"
            )

        # get the entity to update
        old_operating_hours_entity = self._session.get(
            OperatingHoursEntity, newest_operating_hours.id
        )

        # update it's start time
        old_operating_hours_entity.start = newest_operating_hours.start

        # update it's end time
        old_operating_hours_entity.end = newest_operating_hours.end

        self._session.commit()  # once edits have been made to the entity, session.commit() will update it in the db.
        return old_operating_hours_entity.to_model()

    def delete(
        self, subject: User, operating_hours: OperatingHours, cascade: bool
    ) -> None:
        """Delete Operating Hours entry from the database.

        Args:
            subject (User): The user deleting the Operating Hours entry.
            operating_hours (OperatingHours): The entry to delete.
            cascade (bool): Whether or not to delete subsequent recurrences, if the entry recurs.

        Returns:
            None
        """
        self._permission_svc.enforce(
            subject,
            "coworking.operating_hours.delete",
            f"coworking/operating_hours/{operating_hours.id}",
        )

        operating_hours_entity = self._session.get(
            OperatingHoursEntity, operating_hours.id
        )

        if cascade and (operating_hours_entity.recurrence_id != None):
            for entity in (
                self._session.query(OperatingHoursEntity)
                .filter(
                    OperatingHoursEntity.start > operating_hours_entity.start,
                    OperatingHoursEntity.recurrence_id
                    == operating_hours_entity.recurrence_id,
                )
                .all()
            ):
                print(entity.id)
                self._session.delete(entity)
            operating_hours_entity.recurrence.end_date = (
                operating_hours_entity.start.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                    tzinfo=operating_hours_entity.start.tzinfo,
                )
            )

        self._session.delete(operating_hours_entity)
        self._session.commit()
