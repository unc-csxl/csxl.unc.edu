from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session

from ...database import db_session

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours.event_entity import OfficeHoursEventEntity
from ...entities.office_hours import user_created_tickets_table
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity

from ...models.roster_role import RosterRole
from ...models.office_hours.ticket_state import TicketState
from ...models.office_hours.section import OfficeHoursSection
from ...models.office_hours.ticket import (
    OfficeHoursTicket,
    OfficeHoursTicketDraft,
    OfficeHoursTicketPartial,
)
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...models.user import User

from ...services.exceptions import ResourceNotFoundException

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
        """
        Creates a new office hours ticket.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            oh_ticket (OfficeHoursTicketDraft): OfficeHoursTicketDraft object to add to the table.

        Returns:
            OfficeHoursTicketDetails: The newly created OfficeHoursTicket object.

        Raises:
            PermissionError: If the logged-in user is not a section member student.

        """
        # PERMISSIONS

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section: OfficeHoursSection = self._get_office_hours_section_by_oh_event_id(
            oh_ticket.oh_event.id
        )

        # Check If Current Users and Creators Are Section Members and thus have permission to create a ticket.
        section_member_entities: list[SectionMemberEntity] = []

        # Case: Current User
        current_user_section_member_entity: SectionMemberEntity = (
            self._check_user_section_membership(subject.id, oh_section.id)
        )

        if current_user_section_member_entity.member_role != RosterRole.STUDENT:
            raise PermissionError(
                "Only Section Member Students Are Allowed to Create Tickets."
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
        """
        Retrieves an office hours ticket from the table by its id.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            oh_ticket_id (int): ID of the ticket to query by.

        Returns:
            OfficeHoursTicketDetails: `OfficeHoursTicketDetails` with the given id
        """
        # Fetch Ticket By ID
        ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket_id)

        if ticket_entity is None:
            raise ResourceNotFoundException(
                f"Office Hours Ticket with id={oh_ticket_id} not found."
            )

        # USER PERMISSIONS:

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_section_by_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Fetch Current User Section Membership
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        # If current user is student, check if they are creator of ticket
        # Raise Exception if Not Creator!
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            is_creator = False
            ticket_creators = ticket_entity.to_details_model().creators

            for creator in ticket_creators:
                if creator.id == current_user_section_member_entity.id:
                    is_creator = True

            if not is_creator:
                raise PermissionError(
                    f"User Doesn't Have Permission to Get Ticket id={ticket_entity.id}"
                )

        # Passed Permissions - Good to Return Ticket Information
        return ticket_entity.to_details_model()

    def call_ticket(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
    ) -> OfficeHoursTicketDetails:
        """
        Updates an office hours ticket.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            oh_ticket (OfficeHoursTicketPartial): Office Hours Ticket to update in the table

        Returns:
            OfficeHoursTicketDetails: Updated object in table

        Raises:
            ResourceNotFoundException: If the ticket with the specified ID (`oh_ticket_id`) is not found.
            PermissionError: If the logged-in user is a student or/and is not one of the creators of the ticket.
        """

        # Fetch Ticket By ID
        ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket.id)

        if ticket_entity is None:
            raise ResourceNotFoundException(
                f"Cannot Find Ticket with id={oh_ticket.id}"
            )

        # PERMISSIONS
        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_section_by_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Fetch Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        # 1. Caller Must Have Roles - UTA/GTA/INSTRUCTOR
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                "User is a Student and Do Not Have Permission to Call Ticket."
            )

        # 2. Ticket Must Be Queued and Not Have a Caller Linked (Queued Is Only State at which Caller Is Not Linked)
        if (
            ticket_entity.state != TicketState.QUEUED
            or ticket_entity.caller_id is not None
        ):
            raise Exception(
                f"Ticket Must Be Queued In Order to Be Called/ Have No Caller Linked To It. Current Ticket State is {ticket_entity.state}"
            )

        # If No Caller ID and Ticket is Queued, then update states
        if (
            ticket_entity.caller_id is None
            and ticket_entity.state == TicketState.QUEUED
        ):
            ticket_entity.caller_id = current_user_section_member_entity.id
            ticket_entity.state = TicketState.CALLED
            ticket_entity.called_at = datetime.now()
            self._session.commit()

        return ticket_entity.to_details_model()

    def cancel_ticket(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
    ) -> OfficeHoursTicketDetails:
        """
        Updates state to cancel an office hours ticket.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            oh_ticket (OfficeHoursTicketPartial): OfficeHoursTicketPartial object representing the ticket to be canceled.

        Returns:
            OfficeHoursTicketDetails: Updated OfficeHoursTicketDetails object after canceling the ticket.

        Raises:
            ResourceNotFoundException: If the ticket with the specified ID (`oh_ticket.id`) is not found.
            Exception: If the ticket is not in the "Queued" state, indicating it cannot be canceled.
            PermissionError: If the logged-in user is a student and is not one of the creators of the ticket.
        """

        ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket.id)

        if ticket_entity is None:
            raise ResourceNotFoundException(
                f"Cannot Find Ticket with id={oh_ticket.id}"
            )

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_section_by_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        # PERMISSION CHECK:
        # 1. Ticket Must be Queued State
        if ticket_entity.state != TicketState.QUEUED:
            raise Exception("Ticket is Not Queued - Cannot Cancel Ticket!")

        # 2. If Student, Can Only Cancel Their Own Ticket; Otherwise, other roles are fine to cancel.
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:

            ticket_creators = ticket_entity.to_details_model().creators
            # Check If Current User is in Creator List
            is_creator = False
            for creator in ticket_creators:
                if creator.id == current_user_section_member_entity.id:
                    is_creator = True

            if not is_creator:
                raise PermissionError(
                    f"User Doesn't Have Permission to Cancel Ticket id={oh_ticket.id}"
                )

        # Good to Update Cancel State
        ticket_entity.state = TicketState.CANCELED
        self._session.commit()

        return ticket_entity.to_details_model()

    def close_ticket(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
    ) -> OfficeHoursTicketDetails:
        """
        Updates Office Hours Ticket To Closed State.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            oh_ticket (OfficeHoursTicketPartial): OfficeHoursTicket to close.

        Returns:
            OfficeHoursTicketDetails: Updated OfficeHoursTicket object after closing.

        Raises:
            ResourceNotFoundException: If the ticket with the specified ID (`oh_ticket.id`) is not found.
            Exception: If the ticket is not in the "Called" state, indicating it cannot be closed.
            PermissionError: If the logged-in user is a student, as students do not have permission to close tickets.
        """
        # Query Ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket.id)

        if ticket_entity is None:
            raise ResourceNotFoundException(f"Cannot Find Ticket id={oh_ticket.id}")

        if ticket_entity.state != TicketState.CALLED:
            raise Exception("Ticket is Not Queued - Cannot Cancel Ticket!")

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_section_by_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        # PERMISSIONS

        # 1. If student, cannot close ticket - a student can onlyl cancel ticket
        if current_user_section_member_entity.member_role == RosterRole.STUDENT:
            raise PermissionError(
                f"User Doesn't Have Permission to Close Ticket id={oh_ticket.id}"
            )

        ticket_entity.state = TicketState.CLOSED
        ticket_entity.closed_at = datetime.now()
        self._session.commit()

        return ticket_entity.to_details_model()

    def update_ticket_feedback(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
    ) -> OfficeHoursTicketDetails:
        """
        Updates an office hours ticket's feedback details.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            oh_ticket (OfficeHoursTicketPartial): OfficeHoursTicket to update in the table.

        Returns:
            OfficeHoursTicketDetails: Updated OfficeHoursTicket object after feedback update.

        Raises:
            Exception: If `have_concerns` or `caller_notes` fields of `oh_ticket` are None.
            ResourceNotFoundException: If the ticket with the specified ID (`oh_ticket.id`) is not found.
            PermissionError: If the ticket is not closed or if the logged-in user is not the caller of the ticket.
        """

        # Check Feedback Fields Are Not None
        if oh_ticket.have_concerns is None or oh_ticket.caller_notes is None:
            raise Exception("Missing Data To Update Ticket Feedback")

        # Query Ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, oh_ticket.id)

        if ticket_entity is None:
            raise ResourceNotFoundException(f"Cannot Find Ticket id={oh_ticket.id}")

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_section_by_oh_event_id(
            ticket_entity.oh_event_id
        )

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        # PERMISSIONS:
        # 1. Check if Ticket Is Closed
        if ticket_entity.state != TicketState.CLOSED:
            raise PermissionError(
                f"Ticket is Not Closed. Cannot Give Feedback for Ticket id={oh_ticket.id}"
            )

        # 2. CASE: Only Caller of Ticket Can Update
        if ticket_entity.caller_id != current_user_section_member_entity.id:
            raise PermissionError(
                f"Section member id={current_user_section_member_entity.id} is not caller of ticket and do not have permssion to give feedback."
            )

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
                f"Unable To Find Section Member Entity for user with id:{user_id} in academic section with id:{academic_section_ids}. User Doesn't Have Permission to Perform Action."
            )

        return section_member_entity

    def _get_office_hours_section_by_oh_event_id(
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
