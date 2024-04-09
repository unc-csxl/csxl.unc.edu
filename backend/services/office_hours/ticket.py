from datetime import datetime
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.roster_role import RosterRole

from ...models.office_hours.ticket_state import TicketState
from ...models.office_hours.section import OfficeHoursSection

from ...services.exceptions import ResourceNotFoundException

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours.event_entity import OfficeHoursEventEntity

from ...entities.office_hours import user_created_tickets_table
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...database import db_session
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...models.office_hours.ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
    OfficeHoursTicketPartial,
)
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...models.user import User

from ..permission import PermissionService


__authors__ = ["Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


# TODO: Add Comments
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
        # PERMISSIONS

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section: OfficeHoursSection = (
            self._get_office_hours_sections_given_oh_event_id(oh_ticket.oh_event.id)
        )

        # Check If Current Users and Creators Are Section Members and thus have permission to create a ticket.
        section_member_entities: list[SectionMemberEntity] = []

        # Case: Current User
        current_user_section_member_entity: SectionMemberEntity = (
            self._check_user_section_membership(subject.id, oh_section.id)
        )

        section_member_entities.append(current_user_section_member_entity)

        # Case: Remaining Creator of Ticket If Any
        for creator in oh_ticket.creators:
            if creator.id != subject.id:
                section_member_entity = self._check_user_section_membership(
                    creator.id, oh_section.id
                )
                section_member_entities.append(section_member_entity)

        # CREATE TICKET AND ASSOCIATIONS

        # Good To Go - Now Tranform Draft Model To Ticket Entity
        oh_ticket_entity = OfficeHoursTicketEntity.from_draft_model(oh_ticket)

        # Add new object to table and commit changes
        self._session.add(oh_ticket_entity)

        # Commit so can get ticket id
        self._session.commit()

        # Now, Associate with Ticket with Creators
        for section_member_entity in section_member_entities:
            self._session.execute(
                user_created_tickets_table.insert().values(
                    {
                        "ticket_id": oh_ticket_entity.id,
                        "member_id": section_member_entity.id,
                    }
                )
            )

        self._session.commit()

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

        query = select(OfficeHoursTicketEntity).filter(
            OfficeHoursTicketEntity.id == oh_ticket_id
        )
        ticket_entity = self._session.scalars(query).one_or_none()

        if ticket_entity is None:
            raise ResourceNotFoundException(
                f"Office Hours Ticket with id={oh_ticket_id} not found."
            )

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_sections_given_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        ticket_creators = ticket_entity.to_details_model().creators

        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            isCreator = False
            for creator in ticket_creators:
                if creator.id == current_user_section_member_entity.id:
                    isCreator = True

            if not isCreator:
                raise PermissionError(
                    f"User Doesn't Have Permission to Get Ticket id={ticket_entity.id}"
                )

        return ticket_entity.to_details_model()

    def update_called_state(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
    ) -> OfficeHoursTicketDetails:
        """Updates an office hours ticket.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_ticket: OfficeHoursTicket to update in the table
        Returns:
            OfficeHoursTicketDetails: Updated object in table
        """
        # PERMISSION

        # Get Ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket.id)
        if ticket_entity is None:
            raise ResourceNotFoundException(
                f"Reservation(id={oh_ticket.id}) does not exist"
            )

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_sections_given_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError("User Doesn't Have Permission to Call Ticket.")

        # If No Caller ID and Ticket is Queued, then update states
        if (
            ticket_entity.caller_id is None
            and ticket_entity.state == TicketState.QUEUED
        ):
            ticket_entity.caller_id = oh_ticket.caller_id
            ticket_entity.state = TicketState.CALLED
            ticket_entity.called_at = datetime.now()
            self._session.commit()

        elif ticket_entity.caller_id is not None:
            raise Exception("Ticket Already has a caller!")

        # Exception if State is Not Queued
        elif ticket_entity.state in (
            TicketState.CLOSED,
            TicketState.CANCELED,
            TicketState.CALLED,
        ):
            raise Exception(
                f"Cannot update from current state of {ticket_entity.state}"
            )
        else:
            raise Exception("Cannot Update Ticket")

        return ticket_entity.to_details_model()

    def cancel_ticket(
        self, subject: User, oh_ticket: OfficeHoursTicketDetails
    ) -> OfficeHoursTicketDetails:

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_sections_given_oh_event_id(
            oh_ticket.oh_event.id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        query = select(OfficeHoursTicketEntity).filter(
            OfficeHoursTicketEntity.id == oh_ticket.id
        )
        ticket_entity = self._session.scalars(query).one_or_none()

        ticket_creators = ticket_entity.to_details_model().creators

        # CASE: Student Permission - Can Only Cancel Their Own Ticket
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            # Check If Current User is in Creator List
            isCreator = False
            for creator in ticket_creators:
                if creator.id == current_user_section_member_entity.id:
                    isCreator = True

            if not isCreator:
                raise PermissionError(
                    f"User Doesn't Have Permission to Cancel Ticket id={oh_ticket.id}"
                )

        if ticket_entity is None:
            raise ResourceNotFoundException(f"Could Not Find Ticket id={oh_ticket.id}")

        if ticket_entity.state != TicketState.QUEUED:
            raise Exception("Ticket is Not Queued - Cannot Cancel Ticket!")

        ticket_entity.state = TicketState.CANCELED
        self._session.commit()

        return ticket_entity.to_details_model()

    def close_ticket(
        self, subject: User, oh_ticket: OfficeHoursTicketDetails
    ) -> OfficeHoursTicketDetails:

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_sections_given_oh_event_id(
            oh_ticket.oh_event.id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        query = select(OfficeHoursTicketEntity).filter(
            OfficeHoursTicketEntity.id == oh_ticket.id
        )
        ticket_entity = self._session.scalars(query).one_or_none()

        # CASE: Student Permission - Can Only Cancel Their Own Ticket
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"User Doesn't Have Permission to Close Ticket id={oh_ticket.id}"
            )

        if ticket_entity is None:
            raise ResourceNotFoundException(f"Could Not Find Ticket id={oh_ticket.id}")

        if ticket_entity.state != TicketState.CALLED:
            raise Exception("Ticket is Not Queued - Cannot Cancel Ticket!")

        ticket_entity.state = TicketState.CLOSED
        ticket_entity.closed_at = datetime.now()
        self._session.commit()

        return ticket_entity.to_details_model()

    def update_ticket_feedback(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
    ) -> OfficeHoursTicketDetails:
        """Updates an office hours ticket's state.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_ticket: OfficeHoursTicket to update in the table
        Returns:
            OfficeHoursTicketDetails: Updated object in table
        """

        # Query Ticket
        query = select(OfficeHoursTicketEntity).filter(
            OfficeHoursTicketEntity.id == oh_ticket.id
        )
        ticket_entity = self._session.scalars(query).one_or_none()

        if ticket_entity is None:
            raise ResourceNotFoundException("Cannot Find")

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_sections_given_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        # CASE: Student Permission - Can Only Cancel Their Own Ticket
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"User Doesn't Have Permission to Give Feedback For Ticket id={oh_ticket.id}"
            )

        # Check If User is the Ticket Caller
        if current_user_section_member_entity.id != ticket_entity.caller_id:
            raise PermissionError(
                f"User Doesn't Have Permission to Give Feedback For Ticket id={oh_ticket.id}"
            )

        # Check is Ticket Is Closed
        if ticket_entity.state != TicketState.CLOSED:
            raise PermissionError(
                f"Ticket is Not Closed. Cannot Give Feedback for Ticket id={oh_ticket.id}"
            )

        # Check Feedback Fields Are Not None
        if oh_ticket.have_concerns is None or oh_ticket.caller_notes is None:
            raise Exception("Missing Data")

        ticket_entity.have_concerns = oh_ticket.have_concerns
        ticket_entity.caller_notes = oh_ticket.caller_notes

        self._session.commit()

        return ticket_entity.to_details_model()

    def _check_user_section_membership(
        self,
        user_id: int,
        oh_section_id: int,
    ) -> SectionMemberEntity:
        """Checks if a given user is a member in academic sections that are a part of an office hours section.

           Note: An Office Hours section can have multiple academic sections assoicated with it.

        Args:
            user_id: The id of given User of interest
            academic_section_ids: The id of a list academic sections.
        Returns:
            SectionMemberEntity: `SectionMemberEntity` associated with a given user and academic section

        Raises:
            PermissionError if cannot user is not a member in given academic section.
        """

        # Find Academic Section and Their IDs
        academic_sections = (
            self._session.query(SectionEntity)
            .filter(SectionEntity.office_hours_id == oh_section_id)
            .all()
        )

        academic_section_ids = [section.id for section in academic_sections]

        # Find User Academic Section Entity
        section_member_entity = (
            self._session.query(SectionMemberEntity)
            .filter(SectionMemberEntity.user_id == user_id)
            .filter(SectionMemberEntity.section_id.in_(academic_section_ids))
            .first()
        )

        if section_member_entity is None:
            raise PermissionError(
                f"Unable To Find Section Member Entity for user with id:{user_id} in academic section with id:{academic_section_ids}"
            )

        return section_member_entity

    def _get_office_hours_sections_given_oh_event_id(
        self, oh_event_id: int
    ) -> OfficeHoursSection:
        """Checks if a given user is a member in academic sections that are a part of an office hours section.

           Note: An Office Hours section can have multiple academic sections assoicated with it.

        Args:
            oh_event_id: The id of Office Hours Section of interest

        Returns:
            OfficeHoursSection: `OfficeHoursSection` associated with a given event.

        Raises:
            ResourceNotFoundException if cannot office hours event or section for given office hours event.
        """

        # Fetch Office Hours Event
        oh_event_entity = self._session.get(OfficeHoursEventEntity, oh_event_id)

        if oh_event_entity is None:
            raise ResourceNotFoundException(
                f"Couldn't Find Office Hours Event with id: {oh_event_id}"
            )

        # Entity to Model
        oh_event_model = oh_event_entity.to_details_model()

        # Fetch Office Hours Section From Event Model
        oh_section = oh_event_model.oh_section

        return oh_section
