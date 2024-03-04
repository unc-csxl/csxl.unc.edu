from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...database import db_session
from ...entities.academics.event_entity import EventEntity
from ...entities.office_hours.oh_event_entity import OfficeHoursEventEntity
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.oh_event import OfficeHoursEvent, OfficeHoursEventDraft
from ...models.office_hours.oh_event_details import OfficeHoursEventDetails
from ...models.user import User
from ..services.exceptions import ResourceNotFoundException

from ..services.permission import PermissionService


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventService:
    """Service that performs all of the actions on the `OfficeHoursEvent` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    
    def create(self, subject: User, oh_event: OfficeHoursEventDraft) -> OfficeHoursEventDetails:
        """Creates a new office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDraft to add to table

        Returns:
            OfficeHoursEventDetails: Object added to table
        """
        #TODO
        return None
    

    def update(self, subject: User, oh_event: OfficeHoursEvent) -> OfficeHoursEventDetails:
        """Updates an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: id of the OfficeHoursEvent to update in the table
            oh_event: OfficeHoursEvent to update in the table

        Returns:
            OfficeHoursEventDetails: Updated object in table
        """ 
        #TODO
        return None
    
    
    def delete(self, subject: User, oh_event: OfficeHoursEventDetails) -> None:
        """Deletes an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event: OfficeHoursEventDetails to delete
        """
        #TODO

    
    def get_event_by_id(self, subject: User, oh_event_id: int) -> OfficeHoursEventDetails:
        """Gets an office hour event based on OH event id.
        
        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: OfficeHoursEvent id to get the corresponding event for
        
        Returns:
            OfficeHoursEventDetails: OH event associated with the OH event id
        """
        #TODO
        return None
    

    def get_upcoming_events_by_user(self, subject: User, time_range: TimeRange) -> list[OfficeHoursEventDetails]:
        """Gets all upcoming office hours events for a user.

        Args:
            subject: a valid User model representing the currently logged in User
            time_range: Time range to retrieve events for

        Returns:
            list[OfficeHoursEventDetails]: upcoming OH events associated with a user
        """ 
        #TODO
        return None 