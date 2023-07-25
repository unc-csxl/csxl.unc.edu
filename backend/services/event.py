from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.services.org_role import OrgRoleService
from backend.services.permission import UserPermissionError
from ..database import db_session
from ..models.event import Event
from ..models.event_detail import EventDetail
from ..entities import EventEntity
from datetime import datetime

__authors__ = ['Ajay Gandecha', 'Jade Keegan', 'Brianna Ta', 'Audrey Toney']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

class EventService:
    """Service that performs all of the actions on the `EventDetail` table"""

    # Current SQLAlchemy Session
    _session: Session

    def __init__(self, session: Session = Depends(db_session), org_roles: OrgRoleService = Depends()):
        """Initializes the `EventService` session"""
        self._session = session
        self._org_roles = org_roles

    def all(self) -> list[EventDetail]:
        """
        Retrieves all events from the table
        Returns:
            list[EventDetail]: List of all `EventDetail`
        """
        # Select all entries in `EventDetail` table
        query = select(EventEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]
    
    def check_permissions(self, subject: User, event: Event, action: str, resource: str):
        # Check if user has manager permissions for the organization
        org_roles = [org_role for org_role in self._org_roles.get_from_userid(subject.id) if
            org_role.org_id == event.org_id and org_role.membership_type > 0]
        
        # If no role is found, raise an exception
        if(len(org_roles) <=0):
            raise UserPermissionError(action, resource)

    def create(self, subject: User, event: Event) -> EventDetail:
        """
        Creates a event based on the input object and adds it to the table.
        If the event's ID is unique to the table, a new entry is added.
        If the event's ID already exists in the table, raise an exception.
        Parameters:
            event (EventDetail): EventDetail to add to table
        Returns:
            EventDetail: Object added to table
        """
        # Ensure user manages organization corresponding to event
        self.check_permissions(subject, event, 'event.create', f'events')

        # Checks if the role already exists in the table
        if event.id:
            # Raise exception
            raise Exception(f"Duplicate event found with ID: {event.id}")
        else:
            # Otherwise, create new object
            event_entity = EventEntity.from_model(event)

            # Add new object to table and commit changes
            self._session.add(event_entity)
            self._session.commit()

            # Return added object
            return event_entity.to_model()

    def get_from_id(self, id: int) -> EventDetail:
        """
        Get the event from an id
        If none retrieved, a debug description is displayed.
        Parameters:
            id (int): Unique event ID
        Returns:
            EventDetail: Object with corresponding ID
        """

        # Query the event with matching id
        event = self._session.query(EventEntity).get(id)

        # Check if result is null
        if event:
            # Convert entry to a model and return
            return event.to_model()
        else:
            # Raise exception
            raise Exception(f"No event found with ID: {id}")

    def get_from_org_id(self, org_id: int) -> list[EventDetail]:
        """
        Get all the events hosted by an organization with id
        Parameters:
            org_id (int): Unique organization ID
        Returns:
            list[EventDetail]: Object with corresponding organization ID
        """

        # Query the event with matching org id
        events = self._session.query(EventEntity).filter(EventEntity.org_id == org_id).all()
        return [event.to_model() for event in events]

    def get_from_time_range(self, start: datetime, end: datetime) -> list[EventDetail]:
        """
        Get all the events within a time/date range
        Parameters:
            start (datetime): Start time of range
            end (datetime): End time of range
        Returns:
            list[EventDetail]: Object with corresponding organization ID
        """

        # Query the event with matching org id
        events = self._session.query(EventEntity).filter(EventEntity.time < end).filter(EventEntity.time > start).all()
        return [event.to_model() for event in events]
    
    def update(self, subject: User, event: EventDetail) -> EventDetail:
        """
        Update the event
        If none found with that id, a debug description is displayed.
        Parameters:
            event (EventDetail): EventDetail to add to table
        Returns:
            EventDetail: Updated event object
        """
        # Ensure user manages organization corresponding to event
        self.check_permissions(subject, event, 'event.update', f'events')

        # Query the event with matching id
        obj = self._session.query(EventEntity).get(event.id)

        # Check if result is null
        if obj:
            # Update event object
            obj.name=event.name
            obj.time=event.time
            obj.description=event.description
            obj.location=event.location
            obj.public=event.public
            self._session.commit()
            # Return updated object
            return obj.to_model()
        else:
            # Raise exception
            raise Exception(f"No event found with ID: {event.id}")

    
    def delete(self, subject: User, id: int) -> None:
        """
        Delete the event based on the provided ID.
        If no item exists to delete, a debug description is displayed.
        Parameters:
            id (int): Unique event ID
        """

        # Find object to delete
        event=self._session.query(EventEntity).get(id)

        # Ensure object exists
        if event:
            # Ensure user manages organization corresponding to event
            self.check_permissions(subject, event, 'event.delete', f'events/{event.org_id}')
            
            # Delete object and commit
            self._session.delete(event)
            self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No event found with ID: {id}")