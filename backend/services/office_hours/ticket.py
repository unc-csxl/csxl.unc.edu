from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..exceptions import ResourceNotFoundException
from ...database import db_session
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...models.office_hours.ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
)
from ...models.office_hours.ticket_state import TicketState
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
        # TODO: add permissions
        # Create new object
        oh_ticket_entity = OfficeHoursTicketEntity.from_model(oh_ticket)

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

        # Select all entries in the `OfficeHoursTicket` table and filter by id
        query = select(OfficeHoursTicketEntity).filter(
            OfficeHoursTicketEntity.id == oh_ticket_id
        )
        oh_ticket_entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if oh_ticket_entity is None:
            raise ResourceNotFoundException(
                f"Ticket with id: {oh_ticket_id} does not exist."
            )

        return oh_ticket_entity.to_details_model()

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
        # TODO: permissions

        # Find the entity to update
        oh_ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket.id)

        # Raise an error if no entity was found
        if oh_ticket_entity is None:
            raise ResourceNotFoundException(
                f"Course with id: {oh_ticket.id} does not exist."
            )

        # Update the entity
        oh_ticket_entity.description = oh_ticket.description
        oh_ticket_entity.type = oh_ticket.type

        # Update state if its a valid transition
        if self._valid_state_transition(oh_ticket_entity.state, oh_ticket.state):
            oh_ticket_entity.state = oh_ticket.state

            # NOTE: are these conditionals too complicated/unnecessary?

            # Update the caller ID and time if ticket is now called
            if oh_ticket_entity.state == TicketState.CALLED:
                oh_ticket_entity.caller_id = oh_ticket.caller_id
                # TODO: update call time once added to model
                # oh_ticket_entity.called_at = oh_ticket.called_at

            # Update closed time + TA feedback if ticket is now closed
            if oh_ticket_entity.state == TicketState.CLOSED:
                oh_ticket_entity.closed_at = oh_ticket.closed_at
                oh_ticket_entity.have_concerns = oh_ticket.have_concerns
                oh_ticket_entity.caller_notes = oh_ticket.caller_notes

        # Commit changes
        self._session.commit()

        # Return edited object
        return oh_ticket_entity.to_details_model()

    def _valid_state_transition(
        self, prior_state: TicketState, new_state: TicketState
    ) -> bool:
        """Checks if a state transition is valid for an OfficeHoursTicket.
        Args:
            prior_state: previous state of the ticket entity
            new_state: state that the ticket needs to be updated to
        Returns:
            valid_transition: boolean stating whether state transition is allowed
        """
        TS = TicketState

        transition = (prior_state, new_state)
        valid_transition = False

        match transition:
            case (TS.PENDING, TS.CALLED):
                valid_transition = True
            case (TS.PENDING, TS.CANCELED):
                valid_transition = True
            case (TS.CALLED, TS.CLOSED):
                valid_transition = True
            case (TS.CALLED, TS.CANCELED):
                valid_transition = True
            case _:
                return False

        return valid_transition
