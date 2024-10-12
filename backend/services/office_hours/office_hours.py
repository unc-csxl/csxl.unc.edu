"""
Service for office hour events.
"""

import math
from fastapi import Depends
from sqlalchemy import select, exists, and_, func
from sqlalchemy.orm import Session, joinedload
from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    OfficeHourTicketOverview,
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ...models.office_hours.ticket import TicketState
from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import (
    CourseSiteEntity,
    OfficeHoursEntity,
    OfficeHoursTicketEntity,
)
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursService:
    """
    Service that performs all actions for office hour events.
    """

    def __init__(self, session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session

    def get_office_hour_queue(
        self, user: User, office_hours_id: int
    ) -> OfficeHourQueueOverview:
        """
        Loads all of the data relevant to an office hour queue.

        Returns:
            OfficeHourQueueOverview
        """
        # Use an enhanced query to check if an office hour event exists.
        office_hour_event_query = (
            select(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == office_hours_id)
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

        office_hour_event = (
            self._session.scalars(office_hour_event_query).unique().one_or_none()
        )

        if not office_hour_event:
            raise ResourceNotFoundException(
                f"Office hour event with ID: {office_hours_id} not found."
            )

        # Check the site permission for the office hours site for the event.
        self._check_site_admin_permissions(user, office_hour_event.course_site_id)

        # Return data
        return self._to_oh_queue_overview(user, office_hour_event)

    def get_office_hour_get_help_overview(
        self, user: User, office_hours_id: int
    ) -> OfficeHourGetHelpOverview:
        """
        Loads all of the data relevant for getting help in office hours.

        Returns:
            OfficeHourGetHelpOverview
        """
        # Start building the query
        queue_query = (
            select(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == office_hours_id)
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

        # Check permissions
        self._check_site_student_permissions(user, queue_entity.course_site_id)

        # Get ticket for user, if any
        active_tickets = [
            ticket
            for ticket in queue_entity.tickets
            if user.id in [creator.user_id for creator in ticket.creators]
            and ticket.state in [TicketState.QUEUED, TicketState.CALLED]
        ]

        active_ticket = active_tickets[0] if len(active_tickets) > 0 else None

        # Find queue position
        queue_tickets: list[OfficeHoursTicketEntity] = sorted(
            [
                ticket
                for ticket in queue_entity.tickets
                if ticket.state == TicketState.QUEUED
            ],
            key=lambda ticket: ticket.created_at,
        )

        queue_position = (
            queue_tickets.index(active_ticket) + 1
            if active_ticket and active_ticket.state == TicketState.QUEUED
            else -1
        )

        # Return data
        return OfficeHourGetHelpOverview(
            event_type=queue_entity.type.to_string(),
            event_mode=queue_entity.mode.to_string(),
            event_start_time=queue_entity.start_time,
            event_end_time=queue_entity.end_time,
            event_location=queue_entity.room.nickname,
            event_location_description=queue_entity.location_description,
            ticket=(
                self._to_oh_ticket_overview(active_ticket) if active_ticket else None
            ),
            queue_position=queue_position,
        )

    def _to_oh_queue_overview(
        self, user: User, oh_event: OfficeHoursEntity
    ) -> OfficeHourQueueOverview:
        active_tickets = [
            ticket
            for ticket in oh_event.tickets
            if ticket.state == TicketState.CALLED and ticket.caller.user_id == user.id
        ]
        called_tickets = [
            ticket
            for ticket in oh_event.tickets
            if ticket.state == TicketState.CALLED
            and ticket.caller
            and ticket.caller.user_id != user.id
        ]
        completed_tickets = [
            ticket for ticket in oh_event.tickets if ticket.state == TicketState.CLOSED
        ]
        personal_completed_tickets = [
            ticket for ticket in completed_tickets if ticket.caller.user_id == user.id
        ]
        personal_minutes = [
            (ticket.closed_at - ticket.called_at).total_seconds() / 60.0
            for ticket in personal_completed_tickets
        ]
        personal_average_minutes = (
            math.floor(sum(personal_minutes) / len(personal_minutes))
            if len(personal_minutes) > 0
            else 0
        )
        completed_tickets = [
            ticket for ticket in oh_event.tickets if ticket.state == TicketState.CLOSED
        ]
        personal_completed_tickets = [
            ticket for ticket in completed_tickets if ticket.caller.user_id == user.id
        ]
        personal_minutes = [
            (ticket.closed_at - ticket.called_at).total_seconds() / 60.0
            for ticket in personal_completed_tickets
        ]
        personal_average_minutes = (
            math.floor(sum(personal_minutes) / len(personal_minutes))
            if len(personal_minutes) > 0
            else 0
        )
        queued_tickets = [
            ticket for ticket in oh_event.tickets if ticket.state == TicketState.QUEUED
        ]
        return OfficeHourQueueOverview(
            id=oh_event.id,
            type=oh_event.type.to_string(),
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
            personal_tickets_called=len(personal_completed_tickets),
            average_minutes=personal_average_minutes,
            total_tickets_called=len(completed_tickets),
            history=[
                self._to_oh_ticket_overview(ticket) for ticket in completed_tickets
            ],
        )

    def get_oh_event_role(
        self, user: User, office_hours_id: int
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
            .where(OfficeHoursEntity.id == office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        if len(user_members) == 0:
            raise CoursePermissionException(
                "User is not a member of the office hour event."
            )

        return OfficeHourEventRoleOverview(role=user_members[0].member_role.value)

    def _to_oh_ticket_overview(
        self, ticket: OfficeHoursTicketEntity
    ) -> OfficeHourTicketOverview:
        return OfficeHourTicketOverview(
            id=ticket.id,
            created_at=ticket.created_at,
            called_at=ticket.called_at,
            state=ticket.state.to_string(),
            type=ticket.type.to_string(),
            description=ticket.description,
            creators=[creator.user.to_public_model() for creator in ticket.creators],
            caller=(ticket.caller.user.to_public_model() if ticket.caller else None),
        )

    def create(self, user: User, site_id: int, event: NewOfficeHours) -> OfficeHours:
        """
        Creates a new office hours event.
        """
        # Check permissions
        self._check_site_admin_permissions(user, site_id)

        # Create office hours event
        office_hours_entity = OfficeHoursEntity.from_new_model(event)
        self._session.add(office_hours_entity)
        self._session.commit()

        # Return model
        return office_hours_entity.to_model()

    def update(self, user: User, site_id: int, event: OfficeHours) -> OfficeHours:
        """
        Updates an existing office hours event.
        """
        # Find existing event
        office_hours_entity = self._session.get(OfficeHoursEntity, event.id)

        if office_hours_entity is None:
            raise ResourceNotFoundException(
                "Office hours event with id: {event.id} does not exist."
            )

        # Check permissions
        self._check_site_admin_permissions(user, site_id)

        # Update
        office_hours_entity.type = event.type
        office_hours_entity.mode = event.mode
        office_hours_entity.description = event.description
        office_hours_entity.location_description = event.location_description
        office_hours_entity.start_time = event.start_time
        office_hours_entity.end_time = event.end_time
        office_hours_entity.course_site_id = event.course_site_id
        office_hours_entity.room_id = event.room_id

        self._session.commit()

        # Return model
        return office_hours_entity.to_model()

    def delete(self, user: User, site_id: int, event_id: int):
        """
        Deletes an existing office hours event.
        """
        # Find existing event
        office_hours_entity = self._session.get(OfficeHoursEntity, event_id)

        if office_hours_entity is None:
            raise ResourceNotFoundException(
                "Office hours event with id: {event_id} does not exist."
            )

        # Check permissions
        self._check_site_admin_permissions(user, site_id)

        self._session.delete(office_hours_entity)
        self._session.commit()

    def get(self, user: User, site_id: int, event_id: int) -> OfficeHours:
        """
        Gets an existing office hours event.
        """
        # Find existing event
        office_hours_entity = self._session.get(OfficeHoursEntity, event_id)

        if office_hours_entity is None:
            raise ResourceNotFoundException(
                "Office hours event with id: {event_id} does not exist."
            )

        # Check permissions
        self._check_site_admin_permissions(user, site_id)

        return office_hours_entity.to_model()

    def _check_site_admin_permissions(self, user: User, site_id: int):

        # Use an enhanced query to check if a course site exists.
        course_site_exists_query = exists().where(CourseSiteEntity.id == site_id)
        course_site_exists = self._session.query(course_site_exists_query).scalar()

        if not course_site_exists:
            raise ResourceNotFoundException(
                f"Course site with ID: {site_id} not found."
            )

        # Determine whether a student does not have permissions for any site.
        #
        # This query does this by first selecting section rows, joined to
        # course site. An outer join then joins with section member data, only
        # where the section member is for the section selected, is the user who
        # made the request, and where the member is *not* a student (ie, is
        # a UTA, GTA, or INSTRUCTOR ).
        #
        # Finally, we count the sections where the course site ID matches and
        # where the user does *not* exist as a UTA/GTA/INSTRUCTOR user. We can
        # check for this by counting where the member ID is none.
        #
        # Ultimately, this query should result in a number counting the number of
        # sections in the course site for which the user is not authorized. If
        # this number is 0, the user passes site permissions. If this number is
        # > 0, then this should fail.

        no_permissions_query = (
            select(func.count())
            .select_from(SectionEntity)
            .join(SectionEntity.course_site)
            .outerjoin(
                SectionMemberEntity,
                and_(
                    SectionMemberEntity.section_id == SectionEntity.id,
                    SectionMemberEntity.user_id == user.id,
                    SectionMemberEntity.member_role != RosterRole.STUDENT,
                ),
            )
            .where(CourseSiteEntity.id == site_id, SectionMemberEntity.id == None)
        )

        no_permissions_length = self._session.execute(no_permissions_query).scalar()

        if no_permissions_length > 0:
            raise CoursePermissionException(
                "Cannot access a course page containing a section you are not an instructor for."
            )

    def _check_site_student_permissions(self, user: User, site_id: int):

        # Use an enhanced query to check if a course site exists.
        course_site_exists_query = exists().where(CourseSiteEntity.id == site_id)
        course_site_exists = self._session.query(course_site_exists_query).scalar()

        if not course_site_exists:
            raise ResourceNotFoundException(
                f"Course site with ID: {site_id} not found."
            )

        # Determine whether a student does not have permissions for any site.
        #
        # This query does this by first selecting section rows, joined to
        # course site. An outer join then joins with section member data, only
        # where the section member is for the section selected, is the user who
        # made the request, and where the member is a student (not a UTA, etc)
        #
        # Finally, we count the sections where the course site ID matches and
        # where the user exists as a student. We can check for this by counting
        # where the member ID is not none.
        #
        # Ultimately, this query should result in a number counting the number of
        # sections in the course site for which the user is a student. If
        # this number is 0, the user passes site fails.

        is_student_query = (
            select(func.count())
            .select_from(SectionEntity)
            .join(SectionEntity.course_site)
            .outerjoin(
                SectionMemberEntity,
                and_(
                    SectionMemberEntity.section_id == SectionEntity.id,
                    SectionMemberEntity.user_id == user.id,
                    SectionMemberEntity.member_role == RosterRole.STUDENT,
                ),
            )
            .where(CourseSiteEntity.id == site_id, SectionMemberEntity.id != None)
        )

        is_student_length = self._session.execute(is_student_query).scalar()

        if is_student_length == 0:
            raise CoursePermissionException(
                "You cannot access office hours for a class you are not enrolled in."
            )
