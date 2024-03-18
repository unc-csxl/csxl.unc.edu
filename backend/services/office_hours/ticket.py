from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...database import db_session
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...models.office_hours.ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
)
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...models.user import User

from ..permission import PermissionService


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
        # TODO: this is a WIP!
        # ----- Permission check for section creation ----
        # Check if user has admin permissions
        # self._permission_svc.enforce(subject, "academics.section.create", f"section/")

        # Create new object
        oh_ticket_entity = OfficeHoursTicketEntity.from_draft_model(oh_ticket)

        # Add new object to table and commit changes
        self._session.add(oh_ticket_entity)
        self._session.commit()

        # Return added object
        return oh_ticket_entity.to_details_model()

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
