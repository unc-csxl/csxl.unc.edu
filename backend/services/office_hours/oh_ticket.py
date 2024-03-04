from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...database import db_session
from ...entities.office_hours.oh_ticket_entity import OfficeHoursTicketEntity
from ...models.office_hours.oh_ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
)
from ...models.office_hours.oh_ticket_details import OfficeHoursTicketDetails
from ...models.user import User

from ...services.permission import PermissionService


__authors__ = ["Sadie Amato", "Bailey DeSouza"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketService:
    """Service that performs all of the actions on the `OfficeHoursTicket` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def create(
        self, subject: User, oh_ticket: OfficeHoursTicketDraft
    ) -> OfficeHoursTicketDetails:
        """Creates a new office hours ticket.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_ticket: OfficeHoursTicketDraft to add to table
        Returns:
            OfficeHoursTicketDetails: Object added to table
        """
        # TODO
        return None

    def get_ticket_by_id(
        self, subject: User, oh_ticket_id: int
    ) -> OfficeHoursTicketDetails:
        """Retrieves an office hours ticket from the table by its id.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_ticket_id: ID of the ticket to query by.
        Returns:
            OfficeHoursTicketDetails: `OfficeHoursTicketDetails` with the given id
        """
        # TODO
        return None

    def get_tickets_by_section(
        self, subject: User, oh_section_id: int
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets from the table by a section.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section_id: ID of the section to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHsection
        """
        # TODO
        return None

    def get_tickets_by_section_and_user(
        self, subject: User, oh_section_id: int
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all of the subject's office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section_id: ID of the section to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all of a user's `OfficeHoursTicketDetails` in an OHsection
        """
        # TODO
        return None

    def get_tickets_by_event(
        self, subject: User, oh_event_id: int
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_event_id: ID of the event to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent
        """
        # TODO
        return None

    def update(
        self, subject: User, oh_ticket: OfficeHoursTicket
    ) -> OfficeHoursTicketDetails:
        """Updates an office hours ticket.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_ticket: OfficeHoursTicket to update in the table
        Returns:
            OfficeHoursTicketDetails: Updated object in table
        """
        # TODO
        return None

    def update_state(
        self, subject: User, oh_ticket: OfficeHoursTicket
    ) -> OfficeHoursTicketDetails:
        """Updates an office hours ticket's state.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_ticket: OfficeHoursTicket to update in the table
        Returns:
            OfficeHoursTicketDetails: Updated object in table
        """
        # TODO
        return None
