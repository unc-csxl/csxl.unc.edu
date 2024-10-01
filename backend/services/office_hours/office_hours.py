"""
Service for office hour events.
"""

from datetime import timedelta
import math
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.entities.office_hours.office_hours_recurrence_entity import OfficeHoursRecurrenceEntity
from backend.models.office_hours.office_hours_recurrence import NewOfficeHoursRecurrence, OfficeHoursRecurrence
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

__authors__ = ["Ajay Gandecha", "Jade Keegan"]
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

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or user_members[0].member_role == RosterRole.STUDENT:
            raise CoursePermissionException(
                "Not allowed to access the queue of a course you are not a UTA, GTA, or instructor for."
            )

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

        # Return data
        return self._to_oh_queue_overview(user, queue_entity)

    def get_office_hour_get_help_overview(
        self, user: User, office_hours_id: int
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
            .where(OfficeHoursEntity.id == office_hours_id)
            .options(joinedload(SectionMemberEntity.created_oh_tickets))
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0:
            raise CoursePermissionException(
                "You cannot access office hours for a class you are not enrolled in."
            )

        for user_member in user_members:
            if user_member.member_role != RosterRole.STUDENT:
                raise CoursePermissionException(
                    "You cannot access office hours for a class you are not enrolled in."
                )

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
        self._check_site_permissions(user, site_id)

        # Create office hours event
        office_hours_entity = OfficeHoursEntity.from_new_model(event)
        self._session.add(office_hours_entity)
        self._session.commit()

        # Return model
        return office_hours_entity.to_model()
    
    def create_recurring(self, user: User, site_id: int, event: NewOfficeHours, recurrence: NewOfficeHoursRecurrence) -> list[OfficeHours]:
        """
        Creates new office hours events for recurring events.
        """
        # Check permissions
        self._check_site_permissions(user, site_id)

        # Create recurrence entity
        recurrence_entity = OfficeHoursRecurrenceEntity.from_new_model(recurrence)
        self._session.add(recurrence_entity)

        # Create office hour events
        new_events = []
        current_date = recurrence.start_date
        current_event = event

        original_td = recurrence.end_date - recurrence.start_date

        # put valid date strings into list
        days_recur = []
        if recurrence.recurs_monday:
            days_recur.append('monday')
        
        if recurrence.recurs_tuesday:
            days_recur.append('tuesday')
        
        if recurrence.recurs_wednesday:
            days_recur.append('wednesday')
        
        if recurrence.recurs_thursday:
            days_recur.append('thursday')
        
        if recurrence.recurs_friday:
            days_recur.append('friday')
        
        if recurrence.recurs_saturday:
            days_recur.append('saturday')
        
        if recurrence.recurs_sunday:
            days_recur.append('sunday')

        if days_recur.length == 0:
            # error out
            ...

        while current_date <= recurrence.end_date:     
            # Get day name of date
            day = current_date.strftime("%A")

            if day.lower() in days_recur:
                # new date is the start date of original event with "current date" instead (leave the time!)
                current_event.start_time = event.start_time.replace(year=current_date.year, month=current_date.month, day=current_date.day)
                # end date is new date plus original timedelta (accounts for edge case of events that span multiple days)
                current_event.end_time = current_event.start_time + original_td
            else:
                # move to next iteration if day is not valid
                continue
            
            current_event.recurrence_id = recurrence_entity.id

            new_events.append(current_event)

            # Create new OH entity
            new_office_hours_entity = OfficeHoursEntity.from_new_model(current_event)
            self._session.add(new_office_hours_entity)

            # Increment date
            current_date += timedelta(days = 1)

        # commit changes
        self._session.commit()

        return new_events
        
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
        self._check_site_permissions(user, site_id)

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
        self._check_site_permissions(user, site_id)

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
        self._check_site_permissions(user, site_id)

        return office_hours_entity.to_model()

    def _check_site_permissions(self, user: User, site_id: int):
        # Get the course site
        course_site_query = (
            select(CourseSiteEntity)
            .join(SectionEntity)
            .join(SectionMemberEntity)
            .where(CourseSiteEntity.id == site_id)
            .options(
                joinedload(CourseSiteEntity.sections),
                joinedload(CourseSiteEntity.sections).joinedload(SectionEntity.members),
            )
        )
        course_site_entity = (
            self._session.scalars(course_site_query).unique().one_or_none()
        )

        # Complete error handling
        if course_site_entity is None:
            raise ResourceNotFoundException(
                f"Course site with ID: {site_id} not found."
            )

        section_entities = [section for section in course_site_entity.sections]
        for section in section_entities:
            members = [
                member
                for member in section.members
                if member.user_id == user.id
                and member.member_role != RosterRole.STUDENT
            ]
            if len(members) == 0:
                raise CoursePermissionException(
                    "Cannot modify a course page containing a section you are not an instructor for."
                )
