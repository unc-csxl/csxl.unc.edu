from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database import db_session
from backend.entities.academics.event_entity import EventEntity
from backend.entities.office_hours.oh_event_entity import OfficeHoursEventEntity
from backend.models.coworking.time_range import TimeRange
from backend.models.office_hours.oh_event import OfficeHoursEvent, OfficeHoursEventDraft
from backend.models.office_hours.oh_event_details import OfficeHoursEventDetails
from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException

from backend.services.permission import PermissionService


__authors__ = ["Sadie Amato", "Bailey DeSouza"]
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
            oh_event: OfficeHoursEvent to update in the table

        Returns:
            OfficeHoursEventDetails: Updated object in table
        """ 
        #TODO
        return None
    
    
    def delete(self, subject: User, oh_event_id: int) -> None:
        """Deletes an office hours event.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: ID of office hours event to delete
        """
        #TODO

    
    def get_events_by_section(self, subject: User, oh_section_id: int) -> list[OfficeHoursEventDetails]:
        """Gets all office hours events for a section.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section_id: OfficeHoursSection id to get all events for

        Returns:
            list[OfficeHoursEventDetails]: OH events associated with a given section
        """ 
        #TODO
        return None
    
    def get_upcoming_events_by_section(self, oh_section_id: int, time_range: TimeRange) -> list[OfficeHoursEventDetails]:
        """Gets all upcoming office hours events for a section.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section_id: OfficeHoursSection id to get all upcoming events for
            time_range: Time range to retrieve events for

        Returns:
            list[OfficeHoursEventDetails]: upcoming OH events associated with a given section
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