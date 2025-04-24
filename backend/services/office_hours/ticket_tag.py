"""
APIs for academics for office hour tickets.
"""

from fastapi import Depends
from sqlalchemy.orm import Session


from ...entities.office_hours.ticket_tag_entity import OfficeHoursTicketTagEntity
from ...services.office_hours.office_hours import OfficeHoursService
from ...services.exceptions import DuplicateResourceException, ResourceNotFoundException

from ...models.office_hours.ticket_tag import NewOfficeHoursTicketTag, OfficeHoursTicketTag

from ...database import db_session
from ...models.user import User


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OfficeHourTicketTagService:
    """
    Service that performs all of the actions for office hour tickets tags.
    """

    def __init__(self, session: Session = Depends(db_session), _office_hours_svc: OfficeHoursService = Depends(),):
        """
        Initializes the database session.
        """
        self._session = session
        self._office_hours_svc = _office_hours_svc

    def get_tag_by_id(self, user: User, site_id: int, tag_id: int) -> OfficeHoursTicketTag:
        """
        Returns an office hour ticket tag by ID.

        Returns:
            OfficeHourTicketTag
        """
        
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Get ticket tag
        ticket_tag = self._session.get(OfficeHoursTicketTagEntity, tag_id)

        if ticket_tag is None:
            raise ResourceNotFoundException(
                "Office hours ticket tag with id: {tag_id} does not exist."
            )

        # Return model
        return ticket_tag.to_model()

    def get_course_site_tags(self, user: User, site_id: int) -> list[OfficeHoursTicketTag]:
        """
        Returns all office hour ticket tags for a course site.

        Returns:
            list[OfficeHoursTicketTag]
        """
        
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Get all ticket tags
        ticket_tags = self._session.query(OfficeHoursTicketTagEntity).filter(
            OfficeHoursTicketTagEntity.course_site_id == site_id
        ).all()

        # Return models
        return [tag.to_model() for tag in ticket_tags]

    def create(self, user: User, site_id: int, tag: NewOfficeHoursTicketTag) -> OfficeHoursTicketTag:
        """
        Creates a new office hour ticket tag for a course site.

        Returns:
            OfficeHourTicketTag
        """
        
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Fetch existing tags
        existing_tags = self._session.query(OfficeHoursTicketTagEntity).filter(
            OfficeHoursTicketTagEntity.course_site_id == site_id
        ).all()

        if (any(tag.name == existing_tag.name for existing_tag in existing_tags)):
            raise DuplicateResourceException(
                "Office hours ticket tag with name: {tag.name} already exists for this course site."
            )

        # Create ticket tag
        ticket_tag_entity = OfficeHoursTicketTagEntity.from_new_model(tag)
        self._session.add(ticket_tag_entity)
        self._session.commit()

        # Return model
        return ticket_tag_entity.to_model()
    
    
    def update(self, user: User, site_id: int, tag: OfficeHoursTicketTag) -> OfficeHoursTicketTag:
        """
        Updates an existing office hours event.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Find existing tag
        ticket_tag_entity = self._session.get(OfficeHoursTicketTagEntity, tag.id)

        if ticket_tag_entity is None:
            raise ResourceNotFoundException(
                "Office hours ticket tag with id: {tag.id} does not exist."
            )

        # Update
        ticket_tag_entity.name = tag.name

        self._session.commit()

        # Return model
        return ticket_tag_entity.to_model()

    def delete(self, user: User, site_id: int, tag_id: int):
        """
        Deletes an existing office hours event.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Find existing tag
        ticket_tag_entity = self._session.get(OfficeHoursTicketTagEntity, tag_id)

        if ticket_tag_entity is None:
            raise ResourceNotFoundException(
                "Office hours ticket tag with id: {tag_id} does not exist."
            )

        self._session.delete(ticket_tag_entity)
        self._session.commit()