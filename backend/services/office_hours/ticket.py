"""
APIs for academics for office hour tickets.
"""

import math
from datetime import date, datetime, timedelta
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    OfficeHourTicketOverview,
)
from ...models.office_hours.ticket import (
    TicketState,
    NewOfficeHoursTicket,
)

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import (
    CourseSiteEntity,
    OfficeHoursEntity,
    OfficeHoursTicketEntity,
)
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException
from ...entities.office_hours import user_created_tickets_table

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHourTicketService:
    """
    Service that performs all of the actions for office hour tickets.
    """

    def __init__(self, session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session

    def call_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Calls a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        if ticket_entity.state == TicketState.CALLED:
            raise CoursePermissionException("This ticket was already called!")

        if ticket_entity.state != TicketState.QUEUED:
            raise CoursePermissionException(
                "Cannot call a ticket that is not in the queue."
            )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or RosterRole.STUDENT in [
            member.member_role for member in user_members
        ]:
            raise CoursePermissionException(
                "Not allowed to call if a ticket if you are not a UTA, GTA, or instructor for."
            )

        # Call the ticket
        ticket_entity.caller_id = user_members[0].id
        ticket_entity.called_at = datetime.now()
        ticket_entity.state = TicketState.CALLED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return ticket_entity.to_overview_model()

    def cancel_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Cancels a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()
        user_member = user_members[0] if len(user_members) > 0 else None

        # If the user is not a member of the looked up course, throw an error
        if not user_member or (
            user_member.member_role == RosterRole.STUDENT
            and user_member.id not in [creator.id for creator in ticket_entity.creators]
        ):
            raise CoursePermissionException(
                "Not allowed to cancel if a ticket if you are not a UTA, GTA, or instructor for it, or you did not open it."
            )

        # Cancel the ticket
        ticket_entity.state = TicketState.CANCELED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return ticket_entity.to_overview_model()

    def close_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Closes a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        if ticket_entity.state != TicketState.CALLED:
            raise CoursePermissionException(
                "Cannot close a ticket that has not been called."
            )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or RosterRole.STUDENT in [
            member.member_role for member in user_members
        ]:
            raise CoursePermissionException(
                "Not allowed to call if a ticket if you are not a UTA, GTA, or instructor for."
            )

        # Close the ticket
        ticket_entity.closed_at = datetime.now()
        ticket_entity.state = TicketState.CLOSED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return ticket_entity.to_overview_model()

    def create_ticket(
        self, user: User, ticket: NewOfficeHoursTicket
    ) -> OfficeHourTicketOverview:
        """
        Creates a new office hours ticket.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            ticket (OfficeHoursTicket): OfficeHoursTicket object to add to the table.

        Returns:
            OfficeHoursTicketDetails: The newly created OfficeHoursTicket object.

        Raises:
            PermissionError: If the logged-in user is not a section member student.

        """
        # Find the IDs of the creators of the ticket
        creator_ids = [user.id]
        # TODO: Reimplement group tickets
        # list(set([creator.id for creator in oh_ticket_draft.creators] + [user.id]))

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id.in_(creator_ids))
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        user_member_ids = [user_member.user_id for user_member in user_members]

        for creator_id in creator_ids:
            if creator_id not in user_member_ids:
                raise CoursePermissionException(
                    "Not allowed to create a ticket if you are not in the course."
                )

        for user_member in user_members:
            # If the user is not a member of the looked up course, throw an error
            if not user_member or user_member.member_role != RosterRole.STUDENT:
                raise CoursePermissionException(
                    "Not allowed to create a ticket if you are not a student."
                )

        # Check if the user already has a ticket in a queue
        queued_query = (
            select(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(user_created_tickets_table)
            .join(SectionMemberEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
            .where(OfficeHoursTicketEntity.state == TicketState.QUEUED)
            .where(SectionMemberEntity.user_id == user.id)
        )
        queued_tickets_entities = self._session.scalars(queued_query).all()

        if len(queued_tickets_entities) > 0:
            raise CoursePermissionException(
                "You cannot create multiple tickets at once."
            )

        course_query = (
            select(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
        )
        course_entity = self._session.scalars(course_query).one_or_none()

        if course_entity is None:
            raise CoursePermissionException(
                "Cannot create a ticket for a course that does not exist."
            )

        # Check number of tickets for current date
        num_tickets_for_today_query = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(user_created_tickets_table)
            .join(SectionMemberEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
            .where(SectionMemberEntity.user_id == user.id)
            .where(func.date(OfficeHoursTicketEntity.closed_at) == date.today())
        )
        num_tickets_for_today = self._session.execute(
            num_tickets_for_today_query
        ).scalar()

        if num_tickets_for_today >= course_entity.max_tickets_per_day:
            raise CoursePermissionException(
                f"You have created the maximum number of tickets today. Please come back tomorrow."
            )

        # Check if the user is within the ticket cooldown time.
        cooldown_time_cutoff = datetime.now() + timedelta(
            minutes=-course_entity.minimum_ticket_cooldown
        )

        cooldown_tickets_query = (
            select(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(user_created_tickets_table)
            .join(SectionMemberEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
            .where(SectionMemberEntity.user_id == user.id)
            .where(OfficeHoursTicketEntity.closed_at > cooldown_time_cutoff)
        )

        ticket_within_cooldown_range = self._session.scalars(
            cooldown_tickets_query
        ).one_or_none()

        if ticket_within_cooldown_range is not None:
            time_remaining = (
                cooldown_time_cutoff - ticket_within_cooldown_range.closed_at
            )
            minutes_remaining = math.ceil(-(time_remaining.total_seconds() / 60))
            raise CoursePermissionException(
                f"You must wait {minutes_remaining} minute{'' if minutes_remaining == 1 else 's'} before creating another ticket."
            )

        # Create entity
        oh_ticket_entity = OfficeHoursTicketEntity.from_new_model(ticket)

        # Add new object to table and commit changes
        self._session.add(oh_ticket_entity)

        # Commit so can get ticket id
        self._session.commit()

        # Now, Associate ticket with Creators
        for section_member_entity in user_members:
            self._session.execute(
                user_created_tickets_table.insert().values(
                    {
                        "ticket_id": oh_ticket_entity.id,
                        "member_id": section_member_entity.id,
                    }
                )
            )

        self._session.commit()

        # Return details model
        return oh_ticket_entity.to_overview_model()
