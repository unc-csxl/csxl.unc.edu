from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...models.coworking.time_range import TimeRange

from ...models.office_hours.event_details import OfficeHoursEventDetails
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...database import db_session
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import OfficeHoursSectionEntity
from ...models.office_hours.section import (
    OfficeHoursSection,
    OfficeHoursSectionDraft,
)
from ...models.office_hours.section_details import OfficeHoursSectionDetails
from ...models.user import User
from ..exceptions import ResourceNotFoundException

from ..permission import PermissionService


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursSectionService:
    """Service that performs all of the actions on the `OfficeHoursSection` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def create(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDraft,
        academic_ids: list[int],
    ) -> OfficeHoursSectionDetails:
        """Creates a new office hours section.

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSection to add to table

        Returns:
            OfficeHoursSectionDetails: Object added to table
        """
        # TODO: this is a WIP!
        # ----- Permission check for section creation ----
        # Check if user has admin permissions
        # self._permission_svc.enforce(subject, "academics.section.create", f"section/")

        # TODO: investigate what permission checks we will need to do here
        # Add Office Section Academic Section

        # Create new object
        oh_section_entity = OfficeHoursSectionEntity.from_draft_model(oh_section)

        # Add new object to table and commit changes
        self._session.add(oh_section_entity)
        self._session.commit()

        for id in academic_ids:
            section = self._session.get(SectionEntity, id)
            section.office_hours_id = oh_section_entity.id

        self._session.commit()

        # Return added object
        return oh_section_entity.to_details_model()

    def get_section_by_id(
        self, subject: User, oh_section_id: int
    ) -> OfficeHoursSectionDetails:
        """Returns the office hours section from the table by an OH section id

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section_id: ID of the office hours section to query by.
        Returns:
            OfficeHoursSectionDetails: the office hours section with the given id
        """
        # TODO
        return None

    def get_events_by_section(
        self,
        subject: User,
        oh_section: OfficeHoursSectionDetails,
        time_range: TimeRange | None = None,
    ) -> list[OfficeHoursEventDetails]:
        """Returns all events for a given office hours section

        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to get all the events of
        Returns:
            list[OfficeHoursEventDetails]: list of all office hours events for the given section
        """
        # TODO
        # make sure to check if time range is None
        # if time range is not None, you are retrieving upcoming events
        return None

    def get_sections_by_term(
        self, subject: User, term_id: int
    ) -> list[OfficeHoursSectionDetails]:
        """Retrieves all office hours sections from the table by a term.

        Args:
            subject: a valid User model representing the currently logged in User
            term_id: ID of the term to query by.
        Returns:
            list[OfficeHoursSectionDetails]: List of all `OfficeHoursSectionDetails`
        """
        # TODO: this is a WIP!
        # Select all entries in the `OfficeHoursSection` table where their section(s)'s term id == term_id
        query = (
            select(OfficeHoursSectionEntity)
            .join(SectionEntity)
            .where(SectionEntity.term_id == term_id)
            .order_by(OfficeHoursSectionEntity.title)
        )
        entities = self._session.scalars(query).all()

        # Return the model
        return [entity.to_details_model() for entity in entities]

    def get_user_sections_by_term(
        self, subject: User, term_id: int
    ) -> list[OfficeHoursSectionDetails]:
        """Retrieves all office hours sections from the table by a term and specific user.
        Args:
            subject: a valid User model representing the currently logged in User
            term_id: ID of the term to query by.
        Returns:
            list[OfficeHoursSectionDetails]: List of all `OfficeHoursSectionDetails`
        """
        # TODO
        return []

    def get_section_tickets(
        self, subject: User, oh_section: OfficeHoursSectionDetails
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets from the table by a section.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHsection
        """
        # TODO
        return None

    def get_user_section_tickets(
        self, subject: User, oh_section_id: int
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all of the subject's office hours tickets in a section from the table.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the OfficeHoursSectionDetails to query by.
        Returns:
            list[OfficeHoursTicketDetails]: List of all of a user's `OfficeHoursTicketDetails` in an OHsection
        """
        # TODO
        return None

    def update(
        self, subject: User, oh_section: OfficeHoursSection
    ) -> OfficeHoursSectionDetails:
        """Updates an OfficeHoursSection.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: the updated OfficeHoursSection
        Returns:
            OfficeHoursSectionDetails: updated OfficeHoursSectionDetails
        """
        # TODO
        return None

    def delete(self, subject: User, oh_section: int) -> None:
        """Deletes an office hours section.
        Args:
            subject: a valid User model representing the currently logged in User
            oh_section: OfficeHoursSectionDetails to delete
        """
        # TODO
