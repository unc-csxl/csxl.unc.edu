from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours.event_entity import OfficeHoursEventEntity
from ...entities.office_hours.section_entity import OfficeHoursSectionEntity
from ...models.office_hours.event import OfficeHoursEventPartial

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
        # PERMISSIONS

        # Fetch Academic Section - Needed To Determine if user is a member in a section
        academic_sections = self._get_academic_sections_given_oh_event_id(
            oh_ticket.oh_event.id
        )

        academic_section_ids = [section.id for section in academic_sections]

        # Check If Current User Is A Section Member and thus have Permission To create ticket - Raises Exception If Not Member
        section_member_entity = self._check_user_section_membership(
            subject.id, academic_section_ids
        )

        # Check If Each Creator Is a Member in Course Section
        section_member_entities: list[SectionMemberEntity] = []
        for creator in oh_ticket.creators:
            section_member_entity = self._check_user_section_membership(
                creator.id, academic_section_ids
            )
            section_member_entities.append(section_member_entity)

        # CREATE TICKET AND ASSOCIATIONS

        # Good To Go - Now Tranform Draft Model To Ticket Entity
        oh_ticket_entity = OfficeHoursTicketEntity.from_draft_model(oh_ticket)

        # Add new object to table and commit changes
        self._session.add(oh_ticket_entity)
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
        # TODO
        return None

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

    # TODO: Fix Doc String
    def _check_user_section_membership(
        self,
        user_id: int,
        academic_section_ids: list[int],
    ) -> SectionMemberEntity:
        """Checks if current user has all proper permissions to handle ticket entities.

            1. Checks If
        Args:
            user_id: a valid User model representing the currently logged in User
            academic_section_ids: a ticket draft passed from request
        Returns:
            SectionMemberEntity: `SectionMemberEntity` associated with a given user and academic section
        """

        section_member_entity = (
            self._session.query(SectionMemberEntity)
            .filter(SectionMemberEntity.user_id == user_id)
            .filter(SectionMemberEntity.section_id.in_(academic_section_ids))
            .first()
        )

        if section_member_entity is None:
            raise Exception(
                f"Unable To Find User with id:{user_id} in Academic Section with id:{academic_section_ids}"
            )

        return section_member_entity

    # TODO: Add Comments
    def _get_academic_sections_given_oh_event_id(
        self, oh_event_id: int
    ) -> list[SectionEntity]:
        if oh_event_id is None:
            raise Exception(
                "Office Hours Ticket Request Doesn't Include Office Hours Event id."
            )

        academic_sections = (
            self._session.query(SectionEntity)
            .filter(OfficeHoursEventEntity.id == oh_event_id)
            .filter(
                OfficeHoursSectionEntity.id
                == OfficeHoursEventEntity.office_hours_section_id
            )
            .filter(SectionEntity.office_hours_id == OfficeHoursSectionEntity.id)
            .all()
        )

        if len(academic_sections) == 0:
            raise Exception("Couldn't Find Academic Section")

        return academic_sections
