"""
The Event Service allows the API to manipulate event data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from ..database import db_session
from backend.models.event import Event
from backend.models.event_details import NewEvent, EventDetails
from ..entities import EventEntity
from .permission import PermissionService
from .exceptions import EventNotFoundException

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

class EventService:
    """Service that performs all of the actions on the `Event` table"""

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        """Initializes the `EventService` session"""
        self._session = session
        self._permission = permission

    def all(self) -> list[EventDetails]:
        """
        Retrieves all events from the table

        Returns:
            list[EventDetails]: List of all `EventDetails`
        """
        # Select all entries in `Event` table
        query = select(EventEntity)
        entities = self._session.scalars(query).all()

        # Convert entities to details models and return
        return [entity.to_details_model() for entity in entities]

    def create(self, subject: User, event: NewEvent) -> EventDetails:
        """
        Creates a event based on the input object and adds it to the table.
        If the event's ID is unique to the table, a new entry is added.

        Parameters:
            subject: a valid User model representing the currently logged in User
            event: a valid Event model representing the event to be added

        Returns:
            EventDetails: a valid EventDetails model representing the new Event
        """
        
        # Ensure that the user has appropriate permissions to create users
        self._permission.enforce(subject, "organization.events.create", f"organization/{event.organization_id}")

        # Checks if the role already exists in the table
        if event.id:
            event.id = None
        
        # Otherwise, create new object
        event_entity = EventEntity.from_details_model(event)

        # Add new object to table and commit changes
        self._session.add(event_entity)
        self._session.commit()

        # Return added object
        return event_entity.to_details_model()

    def get_from_id(self, id: int) -> EventDetails:
        """
        Get the event from an id
        If none retrieved, a debug description is displayed.

        Parameters:
            id: a valid int representing a unique event ID

        Returns:
            Event: Object with corresponding ID
        """

        # Query the event with matching id
        entity = self._session.query(EventEntity).get(id)

        # Check if result is null
        if entity:
            # Convert entry to a model and return
            return entity.to_details_model()
        else:
            # Raise exception
            raise EventNotFoundException(id);

    def get_events_from_organization(self, slug: str) -> list[EventDetails]:
        """
        Get all the events hosted by an organization with id

        Parameters:
            slug: a valid str representing a unique Organization slug

        Returns:
            list[EventDetail]: a list of valid EventDetails models
        """

        # Query the event with matching organization slug
        events = self._session.query(EventEntity).filter(EventEntity.organization_slug == slug).all()
        
        # Convert entities to models and return
        return [event.to_details_model() for event in events]

    def update(self, subject: User, event: EventDetails) -> EventDetails:
        """
        Update the event
        If none found, a debug description is displayed.

        Parameters:
            event: a valid Event model

        Returns:
            EventDetails: a valid EventDetails model representing the updated event object
        """
        
        # Ensure that the user has appropriate permissions to update users
        self._permission.enforce(subject, "organization.events.create", f"organization/{event.organization_id}")

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
            
            # Save changes
            self._session.commit()
            
            # Return updated object
            return obj.to_details_model()
        else:
            # Raise exception
            raise EventNotFoundException(id);

    
    def delete(self, subject: User, id: int) -> None:
        """
        Delete the event based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            id: an int representing a unique event ID
        """
        
        # Find object to delete
        event = self._session.query(EventEntity).get(id)

        # Ensure that the user has appropriate permissions to delete users
        self._permission.enforce(subject, "organization.events.delete", f"organization/{event.organization_id}")

        # Ensure object exists
        if event:
            
            # Delete object and commit
            self._session.delete(event)
            
            # Save changes
            self._session.commit()
        else:
            # Raise exception
            raise EventNotFoundException(id);