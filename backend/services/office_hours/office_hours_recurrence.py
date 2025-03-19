from datetime import date, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.services.exceptions import (
    RecurringOfficeHourEventException,
    ResourceNotFoundException,
)
from backend.services.office_hours.office_hours import OfficeHoursService

from ...database import db_session
from ...models.user import User
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours, Weekday
from ...entities.office_hours import (
    OfficeHoursEntity,
)

from ...entities.office_hours.office_hours_recurrence_pattern_entity import (
    OfficeHoursRecurrencePatternEntity,
)
from ...models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
)


class OfficeHoursRecurrenceService:
    """
    Service that performs all actions for office hour events recurrence.
    """

    def __init__(
        self,
        session: Session = Depends(db_session),
        _office_hours_svc: OfficeHoursService = Depends(),
    ):
        """
        Initializes the database session.
        """
        self._session = session
        self._office_hours_svc = _office_hours_svc

    def create_recurring(
        self,
        user: User,
        site_id: int,
        event: NewOfficeHours,
        recurrence_pattern: NewOfficeHoursRecurrencePattern,
    ) -> list[OfficeHours]:
        """
        Creates new office hours events for recurring events.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Create events
        new_events = self.create_events(event, recurrence_pattern)

        # Commit changes
        self._session.commit()
        return [entity.to_model() for entity in new_events]

    def create_events(
        self, event: NewOfficeHours, recurrence_pattern: NewOfficeHoursRecurrencePattern
    ):
        # Create recurrence entity
        recurrence_pattern_entity = OfficeHoursRecurrencePatternEntity.from_new_model(
            recurrence_pattern
        )
        self._session.add(recurrence_pattern_entity)
        self._session.commit()

        # Create office hour events
        new_events = []
        current_date = recurrence_pattern.start_date
        current_event = event

        current_event.recurrence_pattern_id = recurrence_pattern_entity.id

        original_td = current_event.end_time - current_event.start_time

        # put valid date strings into list
        days_recur = []
        if recurrence_pattern.recur_monday:
            days_recur.append(Weekday.Monday)

        if recurrence_pattern.recur_tuesday:
            days_recur.append(Weekday.Tuesday)

        if recurrence_pattern.recur_wednesday:
            days_recur.append(Weekday.Wednesday)

        if recurrence_pattern.recur_thursday:
            days_recur.append(Weekday.Thursday)

        if recurrence_pattern.recur_friday:
            days_recur.append(Weekday.Friday)

        if recurrence_pattern.recur_saturday:
            days_recur.append(Weekday.Saturday)

        if recurrence_pattern.recur_sunday:
            days_recur.append(Weekday.Sunday)

        if len(days_recur) == 0:
            raise RecurringOfficeHourEventException("No recurrence pattern selected.")

        # Error out if recurrence pattern end date is before the first event.
        if recurrence_pattern.end_date <= event.start_time:
            raise RecurringOfficeHourEventException(
                "Recurrence pattern end date precedes first event's start."
            )

        while current_date <= recurrence_pattern.end_date:
            # Get number corresponding to day
            day = current_date.weekday()

            if Weekday(day) in days_recur:
                # new date is the start date of original event with "current date" instead (leave the time!)
                current_event.start_time = event.start_time.replace(
                    year=current_date.year,
                    month=current_date.month,
                    day=current_date.day,
                )
                # end date is new date plus original timedelta (accounts for edge case of events that span multiple days)
                current_event.end_time = current_event.start_time + original_td

                # Create new OH entity
                office_hours_entity = OfficeHoursEntity.from_new_model(current_event)

                self._session.add(office_hours_entity)
                new_events.append(office_hours_entity)

            # Increment date
            current_date += timedelta(days=1)

        if len(new_events) == 0:
            raise RecurringOfficeHourEventException(
                "Cannot create any with the given recurrence pattern before the recurrence end date."
            )

        return new_events

    def update_recurring(
        self,
        user: User,
        site_id: int,
        event: OfficeHours,
        recurrence_pattern: NewOfficeHoursRecurrencePattern,
    ):
        """
        Updates an existing office hours event and future events in the recurrence pattern.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Delete all future events.
        self.delete_events(event.id)

        # Recreate events according to the new recurrence pattern.
        new_events = self.create_events(event, recurrence_pattern)

        # Commit changes
        self._session.commit()

        return [entity.to_model() for entity in new_events]

    def delete_recurring(self, user: User, site_id: int, event_id: int):
        """
        Deletes an existing office hours event and future events in the event's recurrence pattern.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        self.delete_events(event_id)

        self._session.commit()

    def delete_events(self, event_id: int):
        # Find existing event
        office_hours_entity = self._session.get(OfficeHoursEntity, event_id)

        if office_hours_entity is None:
            raise ResourceNotFoundException(
                "Office hours event with id: {event_id} does not exist."
            )

        # Find future events in recurrence pattern
        start_date = (
            office_hours_entity.start_time.date()
            if (office_hours_entity.start_time.date() > date.today())
            else date.today()
        )
        future_events_query = (
            select(OfficeHoursEntity)
            .where(
                OfficeHoursEntity.recurrence_pattern_id
                == office_hours_entity.recurrence_pattern_id
            )
            .where(OfficeHoursEntity.start_time >= start_date)
        )

        future_event_entities = (
            self._session.scalars(future_events_query).unique().all()
        )

        for entity in future_event_entities:
            self._session.delete(entity)
