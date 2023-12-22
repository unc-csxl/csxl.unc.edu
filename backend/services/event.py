"""
The Event Service allows the API to manipulate event data in the database.
"""

from fastapi import Depends
from sqlalchemy import select, and_, func, or_, exists
from sqlalchemy.orm import Session

from ..models import User, Event, EventDetails, Paginated, EventPaginationParams
from ..database import db_session
from ..entities import EventEntity, OrganizationEntity
from .permission import PermissionService
from .exceptions import ResourceNotFoundException
from datetime import datetime

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EventService:
    """Service that performs all of the actions on the `Event` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
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

    def create(self, subject: User, event: Event) -> EventDetails:
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
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Checks if the event already exists in the table
        if event.id:
            event.id = None

        # Otherwise, create new object
        event_entity = EventEntity.from_model(event)

        # Add new object to table and commit changes
        self._session.add(event_entity)
        self._session.commit()

        # Return added object
        return event_entity.to_details_model()

    def get_by_id(self, id: int) -> EventDetails:
        """
        Get the event from an id
        If none retrieved, a debug description is displayed.

        Parameters:
            id: a valid int representing a unique event ID

        Returns:
            Event: Object with corresponding ID
        """

        # Query the event with matching id
        entity = self._session.get(EventEntity, id)

        # Check if result is null
        if entity is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Convert entry to a model and return
        return entity.to_details_model()

    def get_events_by_organization(self, slug: str) -> list[EventDetails]:
        """
        Get all the events hosted by an organization with slug

        Parameters:
            slug: a valid str representing a unique Organization slug

        Returns:
            list[EventDetail]: a list of valid EventDetails models
        """

        # Query the organization with the matching slug
        events = (
            self._session.query(EventEntity)
            .join(OrganizationEntity)
            .where(OrganizationEntity.slug == slug)
            .all()
        )

        # Convert entities to models and return
        return [event.to_details_model() for event in events]

    def list(self, pagination_params: EventPaginationParams) -> Paginated[EventDetails]:
        """List Events.

        Parameters:
            pagination_params: The pagination parameters.

        Returns:
            Paginated[Event]: The paginated list of events.
        """

        statement = select(EventEntity)
        length_statement = select(func.count()).select_from(EventEntity)
        if pagination_params.range_start != "":
            range_start = pagination_params.range_start
            range_end = pagination_params.range_end
            criteria = and_(
                EventEntity.time
                >= datetime.strptime(range_start, "%d/%m/%Y, %H:%M:%S"),
                EventEntity.time <= datetime.strptime(range_end, "%d/%m/%Y, %H:%M:%S"),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        if pagination_params.filter != "":
            query = pagination_params.filter

            criteria = or_(
                EventEntity.name.ilike(f"%{query}%"),
                EventEntity.description.ilike(f"%{query}%"),
                exists().where(
                    OrganizationEntity.id == EventEntity.organization_id,
                    OrganizationEntity.name.ilike(f"%{query}%"),
                ),
                exists().where(
                    OrganizationEntity.id == EventEntity.organization_id,
                    OrganizationEntity.slug.ilike(f"%{query}%"),
                ),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != "":
            if pagination_params.ascending == "false":
                statement = statement.order_by(
                    getattr(EventEntity, pagination_params.order_by).desc()
                )
            else:
                statement = statement.order_by(
                    getattr(EventEntity, pagination_params.order_by)
                )

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(
            items=[entity.to_details_model() for entity in entities],
            length=length,
            params=pagination_params,
        )

    def update(self, subject: User, event: Event) -> EventDetails:
        """
        Update the event

        Parameters:
            event: a valid Event model

        Returns:
            EventDetails: a valid EventDetails model representing the updated event object
        """

        # Ensure that the user has appropriate permissions to update users
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Query the event with matching id
        event_entity = self._session.get(EventEntity, event.id)

        # Check if result is null
        if event_entity is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Update event object
        event_entity.name = event.name
        event_entity.time = event.time
        event_entity.description = event.description
        event_entity.location = event.location
        event_entity.public = event.public

        # Save changes
        self._session.commit()

        # Return updated object
        return event_entity.to_details_model()

    def delete(self, subject: User, id: int) -> None:
        """
        Delete the event based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            id: an int representing a unique event ID
        """

        # Find object to delete
        event = self._session.get(EventEntity, id)

        # Ensure that the user has appropriate permissions to delete users
        self._permission.enforce(
            subject,
            "organization.events.manage",
            f"organization/{event.organization_id}",
        )

        # Ensure object exists
        if event is None:
            raise ResourceNotFoundException(f"No event found with matching ID: {id}")

        # Delete object and commit
        self._session.delete(event)

        # Save changes
        self._session.commit()
