from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from ..database import db_session
from backend.models.event import Event
from ..entities import EventEntity
from datetime import datetime

class EventService:
    """Service that performs all of the actions on the `Event` table"""

    # Current SQLAlchemy Session
    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes the `EventService` session"""
        self._session = session

    def all(self) -> list[Event]:
        """
        Retrieves all events from the table
        Returns:
            list[Event]: List of all `Event`
        """
        # Select all entries in `Event` table
        query = select(EventEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def create(self, event: Event) -> Event:
        """
        Creates a event based on the input object and adds it to the table.
        If the event's ID is unique to the table, a new entry is added.
        If the event's ID already exists in the table, raise an exception.
        Parameters:
            event (Event): Event to add to table
        Returns:
            Event: Object added to table
        """

        # Checks if the role already exists in the table
        if self._session.get(EventEntity, event.id):
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

    def get_from_id(self, id: int) -> Event:
        """
        Get the event from an id
        If none retrieved, a debug description is displayed.
        Parameters:
            id (int): Unique event ID
        Returns:
            Event: Object with corresponding ID
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

    def get_from_org_id(self, org_id: int) -> list[Event]:
        """
        Get all the events hosted by an organization with id
        Parameters:
            org_id (int): Unique organization ID
        Returns:
            list[Event]: Object with corresponding organization ID
        """

        # Query the event with matching org id
        events = self._session.query(EventEntity).filter(EventEntity.org_id == org_id).all()
        return [event.to_model() for event in events]

    def get_from_time_range(self, start: datetime, end: datetime) -> list[Event]:
        """
        Get all the events within a time/date range
        Parameters:
            start (datetime): Start time of range
            end (datetime): End time of range
        Returns:
            list[Event]: Object with corresponding organization ID
        """

        # Query the event with matching org id
        events = self._session.query(EventEntity).filter(EventEntity.time < end).filter(EventEntity.time > start).all()
        return [event.to_model() for event in events]
    
    def update(self, event: Event) -> Event:
        """
        Update the event
        If none found with that id, a debug description is displayed.
        Parameters:
            event (Event): Event to add to table
        Returns:
            Event: Updated event object
        """

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

    
    def delete(self, id: int) -> None:
        """
        Delete the event based on the provided ID.
        If no item exists to delete, a debug description is displayed.
        Parameters:
            id (int): Unique event ID
        """

        # Find object to delete
        obj=self._session.query(EventEntity).get(id)

        # Ensure object exists
        if obj:
            # Delete object and commit
            self._session.delete(obj)
            self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No event found with ID: {id}")