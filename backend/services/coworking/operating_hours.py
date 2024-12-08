"""Service that manages operating hours of the XL."""

from datetime import datetime, time, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.entities.coworking.operating_hours_recurrence_entity import (
    OperatingHoursRecurrenceEntity,
)
from backend.models.coworking.operating_hours import OperatingHoursDraft
from .exceptions import OperatingHoursCannotOverlapException
from ..exceptions import ResourceNotFoundException
from ..permission import PermissionService
from ...models import User
from ...database import db_session
from ...models.coworking import OperatingHours, TimeRange
from ...entities.coworking import OperatingHoursEntity

__authors__ = ["Kris Jordan", "Tobenna Okoli", "David Foss"]
__copyright__ = "Copyright 2024"
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

    def _create_recurring_hours(
        self,
        operating_hours_draft: OperatingHoursDraft,
        recurrence: OperatingHoursRecurrenceEntity,
    ):
        """Helper function to create operating hours following a recurrence schedule

        Args:
            operating_hours_draft (OperatingHoursDraft): A draft of the original operating hours to be recurred.
            recurrence (OperatingHoursRecurrenceEntity): The recurrence to apply to all of the new hours.
        """

        start_date = operating_hours_draft.start.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=operating_hours_draft.recurrence.end_date.tzinfo,
        ) + timedelta(days=1)

        self._create_recurring_hours_on_schedule(
            operating_hours_draft,
            start_date,
            operating_hours_draft.recurrence.end_date,
            operating_hours_draft.recurrence.recurs_on,
            recurrence,
        )

    def _create_recurring_hours_on_schedule(
        self,
        operating_hours_draft: OperatingHoursDraft,
        start_date: datetime,
        end_date: datetime,
        recurs_on: int,
        recurrence: OperatingHoursRecurrenceEntity,
    ):
        """Helper function to create operating hours following a given schedule.

        Args:
            operating_hours_draft (OperatingHoursDraft): A draft of the original operating hours to be recurred.
            start_date (datetime): The start date of recurrence.
            end_date (datetime): The end date (non-inclusive) of recurrence.
            recurs_on (int): A bitmask representing the days to recur on, with Monday=0, Sunday=127
            recurrence (OperatingHoursRecurrenceEntity): The recurrence to apply to all of the new hours.
        """
        operating_hours_to_create = []

        # Go through every day between the start date and end date(inclusive)
        # https://stackoverflow.com/a/24637447

        for day in [
            start_date + timedelta(days=x)
            for x in range(
                0,
                (end_date - start_date).days,
            )
        ]:
            # If date is in recurrence, create a new operating hours object for that day
            if (1 << day.weekday()) & recurs_on:
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
        self._session.add_all(entities)

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

        if operating_hours_draft.recurrence:
            self._create_recurring_hours(
                operating_hours_draft, operating_hours.recurrence
            )
        self._session.commit()

        # Return original operating hour
        # I believe this isn't used anywhere on the frontend yet
        # Might be worth switching to returning an array, however that might lead to weird behavior when not doing recurrence
        return operating_hours

    def update(
        self, subject: User, operating_hours_draft: OperatingHoursDraft, cascade: bool
    ) -> OperatingHours:
        """Update existing, open Operating Hours for XL coworking.

        Args:
            subject (User): The user updating the Operating Hours entry.
            operating_hours_draft (OperatingHoursDraft): Object containing the id of the entity to update and the new operating hours.
            cascade (bool): Whether or not to cascade the update across future recurrences, if the entity has a recurrence.

        Returns:
            OperatingHours: The persisted object.
        """
        self._permission_svc.enforce(
            subject, "coworking.operating_hours.update", "coworking/operating_hours"
        )

        new_time_range = TimeRange(
            start=operating_hours_draft.start, end=operating_hours_draft.end
        )
        all_hours = self.schedule(new_time_range)

        conflicts = [
            opHours
            for opHours in all_hours
            if opHours.id
            != operating_hours_draft.id  # ignore the hours we are currently updating
        ]
        if len(conflicts) > 0:
            raise OperatingHoursCannotOverlapException(
                f"Conflicts in the range of {str(new_time_range)}"
            )

        operating_hours_entity = self._session.get(
            OperatingHoursEntity, operating_hours_draft.id
        )

        operating_hours_entity.start = operating_hours_draft.start
        operating_hours_entity.end = operating_hours_draft.end

        # Update future operating hours if cascading and has recurrence information
        if cascade and operating_hours_entity.recurrence:
            for entity in (
                self._session.query(OperatingHoursEntity)
                .filter(
                    OperatingHoursEntity.start > operating_hours_entity.start,
                    OperatingHoursEntity.recurrence_id
                    == operating_hours_entity.recurrence_id,
                )
                .all()
            ):
                entity.start = datetime.combine(
                    entity.start.date(),
                    operating_hours_draft.start.time().replace(
                        tzinfo=operating_hours_draft.start.tzinfo
                    ),
                )
                entity.end = datetime.combine(
                    entity.end.date(),
                    operating_hours_draft.end.time().replace(
                        tzinfo=operating_hours_draft.end.tzinfo
                    ),
                )

        # Create new recurring operating hours if adding a recurrence
        if (not operating_hours_entity.recurrence) and operating_hours_draft.recurrence:
            new_recurrence = OperatingHoursRecurrenceEntity.from_model(
                operating_hours_draft.recurrence
            )

            self._create_recurring_hours(operating_hours_draft, new_recurrence)

        # Delete all recurring operating hours if removing recurrence information
        if operating_hours_entity.recurrence and (not operating_hours_draft.recurrence):
            for entity in (
                self._session.query(OperatingHoursEntity)
                .filter(
                    OperatingHoursEntity.start > operating_hours_entity.start,
                    OperatingHoursEntity.recurrence_id
                    == operating_hours_entity.recurrence_id,
                )
                .all()
            ):
                self._session.delete(entity)

        # Three operations that only happen when recurrence exists both in original and edited
        if operating_hours_entity.recurrence and operating_hours_draft.recurrence:

            # Create new hours if end_date is made later
            if (
                operating_hours_entity.recurrence.end_date
                < operating_hours_draft.recurrence.end_date
            ):
                self._create_recurring_hours_on_schedule(
                    operating_hours_draft,
                    operating_hours_entity.recurrence.end_date,
                    operating_hours_draft.recurrence.end_date,
                    operating_hours_draft.recurrence.recurs_on,
                    operating_hours_entity.recurrence,
                )

            # Delete hours if end_date is made earlier
            if (
                operating_hours_entity.recurrence.end_date
                > operating_hours_draft.recurrence.end_date
            ):
                for entity in (
                    self._session.query(OperatingHoursEntity)
                    .filter(
                        OperatingHoursEntity.start
                        > operating_hours_draft.recurrence.end_date,
                        OperatingHoursEntity.recurrence_id
                        == operating_hours_entity.recurrence_id,
                    )
                    .all()
                ):
                    self._session.delete(entity)

            operating_hours_entity.recurrence.end_date = (
                operating_hours_draft.recurrence.end_date
            )

            # Create/delete hours if recurrence pattern changed
            if (
                operating_hours_entity.recurrence.recurs_on
                != operating_hours_draft.recurrence.recurs_on
            ):
                start_date = operating_hours_draft.start.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                    tzinfo=operating_hours_draft.recurrence.end_date.tzinfo,
                ) + timedelta(days=1)
                # Create new hours
                self._create_recurring_hours_on_schedule(
                    operating_hours_draft,
                    start_date,
                    operating_hours_draft.recurrence.end_date,
                    (operating_hours_entity.recurrence.recurs_on ^ 0b11111)
                    & operating_hours_draft.recurrence.recurs_on,
                    operating_hours_entity.recurrence,
                )

                # Delete hours no longer in recurrence
                for entity in (
                    self._session.query(OperatingHoursEntity)
                    .filter(
                        OperatingHoursEntity.start > start_date,
                        OperatingHoursEntity.recurrence_id
                        == operating_hours_entity.recurrence_id,
                    )
                    .all()
                ):
                    if 1 << entity.start.weekday() & (
                        operating_hours_draft.recurrence.recurs_on ^ 0b11111
                    ):
                        self._session.delete(entity)

                operating_hours_entity.recurrence.recurs_on = (
                    operating_hours_draft.recurrence.recurs_on
                )

        self._session.commit()  # once edits have been made to the entity, session.commit() will update it in the db.
        return operating_hours_entity.to_model()

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

        if operating_hours_entity.recurrence_id:
            if cascade:
                for entity in (
                    self._session.query(OperatingHoursEntity)
                    .filter(
                        OperatingHoursEntity.start > operating_hours_entity.start,
                        OperatingHoursEntity.recurrence_id
                        == operating_hours_entity.recurrence_id,
                    )
                    .all()
                ):
                    self._session.delete(entity)
            else:
                future_recurrences = (
                    self._session.query(OperatingHoursEntity)
                    .filter(
                        OperatingHoursEntity.start > operating_hours_entity.start,
                        OperatingHoursEntity.recurrence_id
                        == operating_hours_entity.recurrence_id,
                    )
                    .all()
                )

                # Update future recurrences with a new recurrence
                if len(future_recurrences) > 0:
                    new_recurrence = OperatingHoursRecurrenceEntity(
                        end_date=operating_hours_entity.recurrence.end_date,
                        recurs_on=operating_hours_entity.recurrence.recurs_on,
                    )
                    for entity in future_recurrences:
                        entity.recurrence = new_recurrence

            # Update current recurrence to stop at the day of this recurrence
            # We do this regardless of cascade value
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
