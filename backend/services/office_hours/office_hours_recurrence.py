from datetime import timedelta
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.services.office_hours.office_hours import OfficeHoursService

from ...database import db_session
from ...models.user import User
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ...entities.office_hours import (
    OfficeHoursEntity,
)

from backend.entities.office_hours.office_hours_recurrence_entity import OfficeHoursRecurrenceEntity
from backend.models.office_hours.office_hours_recurrence import NewOfficeHoursRecurrence

class OfficeHoursRecurrenceService:
    """
    Service that performs all actions for office hour events recurrence.
    """

    def __init__(
            self, 
            session: Session = Depends(db_session), 
            _office_hours_svc: OfficeHoursService = Depends()
    ):
        """
        Initializes the database session.
        """
        self._session = session
        self._office_hours_svc = _office_hours_svc

    def create_recurring(self, user: User, site_id: int, event: NewOfficeHours, recurrence: NewOfficeHoursRecurrence) -> list[OfficeHours]:
          """
          Creates new office hours events for recurring events.
          """
          # Check permissions
          self._office_hours_svc._check_site_permissions(user, site_id)

          # Create recurrence entity
          recurrence_entity = OfficeHoursRecurrenceEntity.from_new_model(recurrence)
          self._session.add(recurrence_entity)

          # Create office hour events
          new_events = []
          current_date = recurrence.start_date
          current_event = event

          original_td = current_event.end_time - current_event.start_time

          # put valid date strings into list
          days_recur = []
          if recurrence.recur_monday:
              days_recur.append('monday')
          
          if recurrence.recur_tuesday:
              days_recur.append('tuesday')
          
          if recurrence.recur_wednesday:
              days_recur.append('wednesday')
          
          if recurrence.recur_thursday:
              days_recur.append('thursday')
          
          if recurrence.recur_friday:
              days_recur.append('friday')
          
          if recurrence.recur_saturday:
              days_recur.append('saturday')
          
          if recurrence.recur_sunday:
              days_recur.append('sunday')

          if len(days_recur) == 0:
              # error out
              ...

          while current_date <= recurrence.end_date:     
              # Get day name of date
              day = current_date.strftime("%A")

              if day.lower() in days_recur:
                  # new date is the start date of original event with "current date" instead (leave the time!)
                  current_event.start_time = event.start_time.replace(year=current_date.year, month=current_date.month, day=current_date.day)
                  # end date is new date plus original timedelta (accounts for edge case of events that span multiple days)
                  current_event.end_time = current_event.start_time + original_td
              else:
                  # move to next iteration if day is not valid
                  current_date += timedelta(days = 1)
                  continue
              
              current_event.recurrence_id = recurrence_entity.id

              # Create new OH entity
              office_hours_entity = OfficeHoursEntity.from_new_model(event)
              self._session.add(office_hours_entity)
              new_events.append(office_hours_entity)

              # Increment date
              current_date += timedelta(days = 1)

          # commit changes
          self._session.commit()

          return [entity.to_model() for entity in new_events]