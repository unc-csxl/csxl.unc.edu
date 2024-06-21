"""
Service for office hour events.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    CourseOfficeHourEventOverview,
    OfficeHourTicketOverview,
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)
from ...models.office_hours.ticket import TicketState
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import (
    CourseSiteEntity,
    OfficeHoursEntity,
    OfficeHoursTicketEntity,
)
from ...entities.user_entity import UserEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHourEventService:
    """
    Service that performs all actions for office hour events.
    """

    def __init__(self, session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session

    def get_office_hour_queue(
        self, user: User, oh_event_id: int
    ) -> OfficeHourQueueOverview:
        """
        Loads all of the data relevant to an office hour queue.

        Returns:
            OfficeHourQueueOverview
        """
        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == oh_event_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or user_members[0].member_role == RosterRole.STUDENT:
            raise CoursePermissionException(
                "Not allowed to access the queue of a course you are not a UTA, GTA, or instructor for."
            )

        # Start building the query
        queue_query = (
            select(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == oh_event_id)
            .options(
                joinedload(OfficeHoursEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.caller)
                .joinedload(SectionMemberEntity.user)
            )
            .options(
                joinedload(OfficeHoursEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.creators)
                .joinedload(SectionMemberEntity.user)
            )
        )

        # Load data
        queue_entity = self._session.scalars(queue_query).unique().one_or_none()

        if not queue_entity:
            raise ResourceNotFoundException(
                f"No office hours event for id: {oh_event_id}"
            )

        # Return data
        return self._to_oh_queue_overview(user, queue_entity)

    def get_office_hour_get_help_overview(
        self, user: User, oh_event_id: int
    ) -> OfficeHourGetHelpOverview:
        """
        Loads all of the data relevant for getting help in office hours.

        Returns:
            OfficeHourGetHelpOverview
        """
        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == oh_event_id)
            .options(joinedload(SectionMemberEntity.created_oh_tickets))
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        # If the user is not a member of the looked up course, throw an error
        if not user_member or user_member.member_role != RosterRole.STUDENT:
            raise CoursePermissionException(
                "You cannot access office hours for a class you are not enrolled in."
            )

        # Locate tickets
        user_member.created_oh_tickets

        # Start building the query
        queue_query = (
            select(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == oh_event_id)
            .options(
                joinedload(OfficeHoursEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.caller)
                .joinedload(SectionMemberEntity.user)
            )
            .options(
                joinedload(OfficeHoursEntity.tickets)
                .joinedload(OfficeHoursTicketEntity.creators)
                .joinedload(SectionMemberEntity.user)
            )
        )

        # Load data
        queue_entity = self._session.scalars(queue_query).unique().one_or_none()

        if not queue_entity:
            raise ResourceNotFoundException(
                f"No office hours event for id: {oh_event_id}"
            )

        # Get ticket for user, if any
        active_tickets = [
            ticket
            for ticket in queue_entity.tickets
            if user_member.id in [creator.id for creator in ticket.creators]
            and ticket.state in [TicketState.QUEUED, TicketState.CALLED]
        ]

        active_ticket = active_tickets[0] if len(active_tickets) > 0 else None

        # Find queue position
        queue_tickets = [
            ticket
            for ticket in queue_entity.tickets
            if ticket.state == TicketState.QUEUED
        ]

        queue_position = (
            queue_tickets.index(active_ticket) + 1
            if active_ticket and active_ticket.state == TicketState.QUEUED
            else -1
        )

        # Return data
        return OfficeHourGetHelpOverview(
            event_type=queue_entity.type.value,
            event_mode=queue_entity.mode.value,
            event_start_time=queue_entity.start_time,
            event_end_time=queue_entity.end_time,
            ticket=(
                self._to_oh_ticket_overview(active_ticket) if active_ticket else None
            ),
            queue_position=queue_position,
        )

    def _to_oh_ticket_overview(
        self, ticket: OfficeHoursTicketEntity
    ) -> OfficeHourTicketOverview:
        return OfficeHourTicketOverview(
            id=ticket.id,
            created_at=ticket.created_at,
            called_at=ticket.called_at,
            state=ticket.state.value,
            type=ticket.type.value,
            description=ticket.description,
            creators=[
                f"{creator.user.first_name} {creator.user.last_name}"
                for creator in ticket.creators
            ],
            caller=(
                f"{ticket.caller.user.first_name} {ticket.caller.user.last_name}"
                if ticket.caller
                else None
            ),
        )

    def _to_oh_queue_overview(
        self, user: User, oh_event: OfficeHoursEntity
    ) -> OfficeHourQueueOverview:
        active_tickets = [
            ticket
            for ticket in oh_event.tickets
            if ticket.state == TicketState.CALLED
            and ticket.caller
            and ticket.caller.user_id == user.id
        ]
        called_tickets = [
            ticket
            for ticket in oh_event.tickets
            if ticket.state == TicketState.CALLED
            and ticket.caller
            and ticket.caller.user_id != user.id
        ]
        queued_tickets = [
            ticket for ticket in oh_event.tickets if ticket.state == TicketState.QUEUED
        ]
        return OfficeHourQueueOverview(
            id=oh_event.id,
            type=oh_event.type.value,
            start_time=oh_event.start_time,
            end_time=oh_event.end_time,
            active=(
                self._to_oh_ticket_overview(active_tickets[0])
                if len(active_tickets) > 0
                else None
            ),
            other_called=[
                self._to_oh_ticket_overview(ticket) for ticket in called_tickets
            ],
            queue=[self._to_oh_ticket_overview(ticket) for ticket in queued_tickets],
        )

    def get_oh_event_role(
        self, user: User, oh_event_id: int
    ) -> OfficeHourEventRoleOverview:
        """
        Returns the user's role for an event.

        Returns:
            OfficeHourEventRoleOverview
        """
        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == oh_event_id)
        )

        user_member = self._session.scalars(user_member_query).unique().one_or_none()

        if not user_member:
            raise CoursePermissionException(
                "User is not a member of the office hour event."
            )

        return OfficeHourEventRoleOverview(role=user_member.member_role.value)

    def _to_oh_ticket_overview(
        self, ticket: OfficeHoursTicketEntity
    ) -> OfficeHourTicketOverview:
        return OfficeHourTicketOverview(
            id=ticket.id,
            created_at=ticket.created_at,
            called_at=ticket.called_at,
            state=ticket.state.value,
            type=ticket.type.value,
            description=ticket.description,
            creators=[
                f"{creator.user.first_name} {creator.user.last_name}"
                for creator in ticket.creators
            ],
            caller=(
                f"{ticket.caller.user.first_name} {ticket.caller.user.last_name}"
                if ticket.caller
                else None
            ),
        )
