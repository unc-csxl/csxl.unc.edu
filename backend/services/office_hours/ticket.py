from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...services.exceptions import ResourceNotFoundException

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours.event_entity import OfficeHoursEventEntity
from ...entities.office_hours.section_entity import OfficeHoursSectionEntity

from ...entities.office_hours import user_created_tickets_table
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...models.roster_role import RosterRole
from ...database import db_session
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...models.office_hours.ticket import (
    OfficeHoursTicketDraft,
    OfficeHoursTicketPartial,
)
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...models.user import User

from ..permission import PermissionService


__authors__ = ["Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
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
        # PERMISSIONS

        # Need event_id to fetch office hours section id
        if oh_ticket.oh_event.id is None:
            raise Exception(
                "Create Office Hours Ticket Request Doesn't Include Office Hours Event id."
            )

        # Fetch Office Hours Section - Needed To Determine if User Membership
        oh_section_entity = self._get_office_hours_sections_given_oh_event_id(
            oh_ticket.oh_event.id
        )

        # Check If Current Users and Creators Are Section Members and thus have permission to create a ticket.
        section_member_entities: list[SectionMemberEntity] = []

        # Case: Current User
        current_user_section_member_entity = self._check_user_section_membership(
            subject.id, oh_section_entity.id
        )

        section_member_entities.append(current_user_section_member_entity)

        # Case: Remaining Creator of Ticket If Any
        for creator in oh_ticket.creators:
            if creator.id != subject.id:
                section_member_entity = self._check_user_section_membership(
                    creator.id, oh_section_entity.id
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
        entity = self._session.get(OfficeHoursTicketEntity, oh_ticket_id)

        # Check if result is null
        if entity is None:
            raise ResourceNotFoundException(
                f"No event found with matching ID: {oh_ticket_id}"
            )

        # Convert entry to a model and return
        return entity.to_details_model()

    def update(
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
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
        self, subject: User, oh_ticket: OfficeHoursTicketPartial
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
            ResourceNotFoundException if cannot user is not a member in given academic section.
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
            raise ResourceNotFoundException(
                f"Unable To Find Section Member Entity for user with id:{user_id} in academic section with id:{academic_section_ids}"
            )

        return section_member_entity

    def _get_office_hours_sections_given_oh_event_id(
        self, oh_event_id: int
    ) -> OfficeHoursSectionEntity:
        """Checks if a given user is a member in academic sections that are a part of an office hours section.

           Note: An Office Hours section can have multiple academic sections assoicated with it.

        Args:
            oh_event_id: The id of Office Hours Section of interest

        Returns:
            OfficeHoursSectionEntity: `OfficeHoursSectionEntity` associated with a given event.

        Raises:
            ResourceNotFoundException if cannot office hours section for given office hours event.
        """

        # Find Office Hours Section
        oh_section_entity = (
            self._session.query(OfficeHoursSectionEntity)
            .filter(OfficeHoursEventEntity.id == oh_event_id)
            .filter(
                OfficeHoursSectionEntity.id
                == OfficeHoursEventEntity.office_hours_section_id
            )
            .first()
        )

        if oh_section_entity is None:
            raise ResourceNotFoundException(
                f"Couldn't Find Office Hours Section related to office hours event with id: {oh_event_id}"
            )

        return oh_section_entity
