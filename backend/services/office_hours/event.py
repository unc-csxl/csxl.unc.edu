from operator import or_
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import date, datetime, timedelta

from ...entities.academics.section_entity import SectionEntity
from ...entities.academics.section_member_entity import SectionMemberEntity
from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...entities.office_hours import OfficeHoursEventEntity

from ...models.office_hours.event_status import (
    OfficeHoursEventStatus,
    StaffHelpingStatus,
    StudentOfficeHoursEventStatus,
    StudentQueuedTicketStatus,
)
from ...models.office_hours.ticket_state import TicketState
from ...models.roster_role import RosterRole
from ...models.office_hours.ticket_state import TicketState

from ...models.office_hours.ticket_details import OfficeHoursTicketDetails

from ...database import db_session

from ...models.office_hours.event import (
    OfficeHoursEvent,
    OfficeHoursEventDraft,
    OfficeHoursEventPartial,
    OfficeHoursEventRecurringDraft,
    Weekday,
)
from ...models.office_hours.event_details import OfficeHoursEventDetails
from ...models.user import User

from ..exceptions import ResourceNotFoundException
from ..permission import PermissionService


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursEventService:
    """Service that performs all of the actions on the `OfficeHoursEvent` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def create(
        self, subject: User, oh_event: OfficeHoursEventDraft
    ) -> OfficeHoursEvent:
        """Creates a new office hours event.

        Args:
            subject (User): a valid User model representing the currently logged in User
            oh_event (OfficeHoursEventDraft): Event draft to add to table

        Returns:
            OfficeHoursEvent: Object added to table

        Raises:
            PermissionError: If subject not a member or is a student.
        """
        # Permissions - Raises Exception if Permission Fails
        self._check_user_section_permissions(subject.id, oh_event.oh_section.id)

        # Create new object
        oh_event_entity = OfficeHoursEventEntity.from_draft_model(oh_event)

        # Add new object to table and commit changes
        self._session.add(oh_event_entity)
        self._session.commit()

        # Return added object
        return oh_event_entity.to_model()

    def create_weekly_events(
        self,
        subject: User,
        oh_event: OfficeHoursEventRecurringDraft,
    ) -> list[OfficeHoursEvent]:
        """
        Create weekly recurring office hours events.

        Args:
            subject (User): The user initiating the event creation.
            oh_event (OfficeHoursEventRecurringDraft): The recurring draft event.

        Returns:
            list[OfficeHoursEvent]: A list of created office hours events.
        Raises:
            PermissionError: If the subject is not a member of OH Section or is a student.
            Exception: If the end date is before the start date or the range exceeds 16 weeks.
        """
        # Permissions - Raises Exception if Permission Fails
        self._check_user_section_permissions(subject.id, oh_event.draft.oh_section.id)

        if oh_event.recurring_end_date < oh_event.recurring_start_date:
            raise Exception("End Date Is Before Start Date!")

        days_range = (oh_event.recurring_end_date - oh_event.recurring_start_date).days

        if days_range > (16 * 7):
            raise Exception("Range Greater Than 16 Weeks!")

        # Get All Recurring Event Dates
        event_dates = self._get_recurring_weekday_dates(
            oh_event.recurring_start_date,
            oh_event.recurring_end_date,
            oh_event.selected_week_days,
        )
        event_entity_drafts = []

        for event_date in event_dates:
            event_draft = oh_event.draft

            # Update Event Date
            event_draft.event_date = event_date

            # Update Event Start Time
            event_draft.start_time = self._transform_date(
                event_draft.start_time, event_date
            )

            # Update Event End Time
            event_draft.end_time = self._transform_date(
                event_draft.end_time, event_date
            )

            oh_event_entity = OfficeHoursEventEntity.from_draft_model(event_draft)
            event_entity_drafts.append(oh_event_entity)

        # Add new objects to table and commit changes
        self._session.add_all(event_entity_drafts)
        self._session.commit()

        # Return added objects
        return [oh_event_entity.to_model() for oh_event_entity in event_entity_drafts]

    def update(
        self, subject: User, oh_event_delta: OfficeHoursEventPartial
    ) -> OfficeHoursEvent:
        """Updates an office hours event.

        Args:
            subject (User): a valid User model representing the currently logged in User
            oh_event_delta (OfficeHoursEventPartial): OfficeHoursEventPartial delta to update in the table

        Returns:
            OfficeHoursEvent: Updated object in table

        Raises:
            PermissionError: If subject is not a member of OH Section or is a student.

        """
        oh_event_entity = self._session.get(OfficeHoursEventEntity, oh_event_delta.id)

        if oh_event_entity is None:
            raise ResourceNotFoundException(
                f"Could not find Office Hours event with id={oh_event_delta.id}"
            )

        self._check_user_section_permissions(
            subject.id, oh_event_entity.office_hours_section_id
        )

        # Update Delta Fields
        if oh_event_delta.event_date is not None:
            oh_event_entity.date = oh_event_delta.event_date

        if oh_event_delta.start_time is not None:
            oh_event_entity.start_time = oh_event_delta.start_time

        if oh_event_delta.end_time is not None:
            oh_event_entity.end_time = oh_event_delta.end_time

        if oh_event_delta.location_description is not None:
            oh_event_entity.location_description = oh_event_delta.location_description

        if oh_event_delta.description is not None:
            oh_event_entity.description = oh_event_delta.description

        if oh_event_delta.type is not None:
            oh_event_entity.type = oh_event_delta.type

        if oh_event_delta.room is not None:
            oh_event_entity.room_id = oh_event_delta.room.id

        if (
            oh_event_delta.oh_section is not None
            and oh_event_delta.oh_section.id != oh_event_entity.office_hours_section_id
        ):
            raise Exception("Updating Office Hours Event OH Section is Not Allowed.")

        self._session.commit()

        # Return the model
        return oh_event_entity.to_model()

    def delete(self, subject: User, oh_event: OfficeHoursEvent) -> None:
        """Delete the specified office hours event.

        Args:
            subject (User): The user initiating the delete operation.
            oh_event (OfficeHoursEvent): The office hours event to be deleted.

        Returns:
            None

        Raises:
            PermissionError: If the user attempting to delete the event is a student or not a member of OH Section.
            ResourceNotFoundException: If the specified office hours event does not exist.

        """
        self._check_user_section_permissions(subject.id, oh_event.oh_section.id)

        oh_event_entity = self._session.get(OfficeHoursEventEntity, oh_event.id)

        if len(oh_event_entity.tickets) != 0:
            raise Exception(
                f"Ticket data exists for office hours event with id={oh_event.id}. Unable to delete event due to existing ticket data."
            )

        self._session.delete(oh_event_entity)
        self._session.commit()

    def get_event_by_id(self, subject: User, oh_event_id: int) -> OfficeHoursEvent:
        """Gets an office hour event based on OH event id.

        Args:
            subject (User): a valid User model representing the currently logged in User
            oh_event_id (int): OfficeHoursEvent id to get the corresponding event for

        Returns:
            OfficeHoursEvent: OH event associated with the OH event id

        Raises:
            ResourceNotFoundException: If office hours event is not found given `oh_event_id`.
            PermissionError: If subject is not a member of OH Section.
        """

        # Get Entity in the `OfficeHoursEventEntity` table with event id
        query = select(OfficeHoursEventEntity).filter(
            OfficeHoursEventEntity.id == oh_event_id
        )
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(
                f"Event with id: {oh_event_id} does not exist."
            )

        # Good to Go - return the model
        return entity.to_model()

    def get_queued_and_called_tickets_by_event(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.

        Args:
            subject (User): a valid User model representing the currently logged in User
            oh_event (OfficeHoursEvent): the OfficeHoursEvent to query by.

        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent

        Raises:
            PermissionError: If subject is not a member of OH Section or is a student.
        """

        self._check_user_section_permissions(subject.id, oh_event.oh_section.id)

        query = (
            select(OfficeHoursTicketEntity)
            .where(OfficeHoursTicketEntity.oh_event_id == oh_event.id)
            .where(
                or_(
                    OfficeHoursTicketEntity.state == TicketState.QUEUED,
                    OfficeHoursTicketEntity.state == TicketState.CALLED,
                )
            )
            .order_by(OfficeHoursTicketEntity.created_at)
        )

        entities = self._session.scalars(query).all()

        # Return the details models
        return [entity.to_details_model() for entity in entities]

    def get_event_tickets(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> list[OfficeHoursTicketDetails]:
        """Retrieves all office hours tickets in an event from the table.

        Args:
            subject (User): a valid User model representing the currently logged in User
            oh_event (OfficeHoursEvent): the OfficeHoursEvent to query by.

        Returns:
            list[OfficeHoursTicketDetails]: List of all `OfficeHoursTicketDetails` in an OHEvent

        Raises:
            PermissionError: If subject is not a member of OH Section or is a student.
        """

        self._check_user_section_permissions(subject.id, oh_event.oh_section.id)

        query = (
            select(OfficeHoursTicketEntity)
            .where(OfficeHoursTicketEntity.oh_event_id == oh_event.id)
            .order_by(OfficeHoursTicketEntity.created_at.desc())
        )

        entities = self._session.scalars(query).all()

        # Return the details models
        return [entity.to_details_model() for entity in entities]

    def get_event_queue_stats(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> OfficeHoursEventStatus:
        """Retrieve queued and called ticket statistics for a specific office hours event.

        Args:
            subject (User): The user object representing the authenticated user making the request.
            oh_event (OfficeHoursEvent): The details of the office hours event.

        Returns:
            OfficeHoursEventStatus: An `OfficeHoursEventStatus` object representing the statistics
                (queued and called ticket counts) for the specified office hours event.

        Raises:
            PermissionError: If subject is not a member of OH Section.
        """
        # PERMISSIONS: Check If User is an OH Section Member - Exception If Not.
        self._check_user_section_permissions(
            subject.id, oh_event.oh_section.id, student_acess=True
        )

        # Queued Tickets
        queued_ticket_entities = self._get_queued_tickets_by_oh_event(oh_event.id)
        queued_ticket_count = len(queued_ticket_entities)

        # Called Tickets
        called_ticket_entities = self._get_called_tickets_by_oh_event(oh_event.id)
        called_ticket_count = len(called_ticket_entities)

        # Build Event Status
        event_status = OfficeHoursEventStatus(
            open_tickets_count=called_ticket_count,
            queued_tickets_count=queued_ticket_count,
        )

        # Return the Status model
        return event_status

    def get_event_queue_stats_for_student_with_ticket(
        self, subject: User, oh_event: OfficeHoursEvent, ticket_id: int
    ) -> StudentOfficeHoursEventStatus:
        """Retrieve student ticket position, queued and called ticket statistics for a specific office hours event.

        Args:
            subject (User): The user object representing the authenticated user making the request.
            oh_event (OfficeHoursEvent): The details of the office hours event.

        Returns:
            OfficeHoursEventStatus: An `OfficeHoursEventStatus` object representing the statistics
                (queued and called ticket counts) for the specified office hours event.

        Raises:
             PermissionError: If subject is not a member of OH Section.
        """
        # PERMISSIONS:

        # 1. Check If User is an OH Section Member - Exception If Not.
        current_user_section_member_entity = self._check_user_section_permissions(
            subject.id, oh_event.oh_section.id, student_acess=True
        )

        # 2. Check Ticket Exists in Office Hours Event
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if ticket_entity is None:
            raise ResourceNotFoundException(f"Ticket id={ticket_id} doesn't exist.")

        if ticket_entity.oh_event_id != oh_event.id:
            raise Exception(
                f"Given Ticket id={ticket_id} Is Not A Part of OH Event id={oh_event.id}"
            )

        # 3. Check if User is Creator of Ticket
        ticket_creators = ticket_entity.to_details_model().creators

        # True if Current Section Mement Exists In Ticket Creators List
        is_creator: bool = current_user_section_member_entity.id in [
            creator.id for creator in ticket_creators
        ]
        if not is_creator:
            raise PermissionError(
                f"User Doesn't Have Permission to View Queue Stats for Ticket id={ticket_entity.id}"
            )

        # Queued Tickets
        queued_ticket_entities = self._get_queued_tickets_by_oh_event(oh_event.id)
        queued_ticket_count = len(queued_ticket_entities)

        # Current Ticket Position in Queue
        current_ticket_position = self._find_ticket_position(
            queued_ticket_entities, ticket_id
        )

        if current_ticket_position == -1:
            raise Exception(
                f"Ticket with id={ticket_id} Doesn't Exist in Queued Ticket List."
            )

        # Called Tickets
        called_ticket_entities = self._get_called_tickets_by_oh_event(oh_event.id)
        called_ticket_count = len(called_ticket_entities)

        # Build Event Status
        student_event_status = StudentOfficeHoursEventStatus(
            open_tickets_count=called_ticket_count,
            queued_tickets_count=queued_ticket_count,
            ticket_position=current_ticket_position,
        )

        # Return the Status model
        return student_event_status

    def check_staff_helping_status(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> StaffHelpingStatus:
        """
        Retrieve the ticket a staff member is currently helping, if there is one.

        Args:
            subject (User): The user object representing the authenticated user making the request.
            oh_event (OfficeHoursEvent): The office hours event.
        Returns:
            StaffHelpingStatus: A `StaffHelpingStatus` object representing the ticket a staff member is working on.

        Raises:
            PermissionError: If subject is not a member of OH Section or is a student.
        """
        # Throws PermissionError if user is not a SectionMember of the given OH section
        section_member_entity = self._check_user_section_permissions(
            subject.id, oh_event.oh_section.id
        )

        # Get all called tickets in the given event
        called_event_ticket_entities = self._get_called_tickets_by_oh_event(oh_event.id)

        # Find queued ticket with subject's id as caller
        for ticket in called_event_ticket_entities:
            if section_member_entity.id == ticket.caller_id:
                return StaffHelpingStatus(ticket_id=ticket.id)

        # Return Status with id = None if not found to be helping a ticket
        return StaffHelpingStatus(ticket_id=None)

    def check_student_in_queue_status(
        self, subject: User, oh_event: OfficeHoursEvent
    ) -> StudentQueuedTicketStatus:
        """
        Retrieve the ticket a student currently has in the queue, if there is one.

        Args:
            subject (User): The user object representing the authenticated user making the request.
            oh_event (OfficeHoursEvent): The office hours event.
        Returns:
            StudentQueuedTicketStatus: A `StudentQueuedTicketStatus` object representing the ticket a student has queued up.

        Raises:
            PermissionError: If subject is not a member of OH Section.
        """

        # Throws PermissionError if user is not a SectionMember of the given OH section
        section_member_entity = self._check_user_section_permissions(
            subject.id, oh_event.oh_section.id, student_acess=True
        )

        queued_event_ticket_entities = self._get_queued_tickets_by_oh_event(oh_event.id)

        # Find queued ticket with student's id as creator, or assign id to None in Status model
        for ticket in queued_event_ticket_entities:
            creator_ids = [creator.id for creator in ticket.creators]
            if section_member_entity.id in creator_ids:
                return StudentQueuedTicketStatus(ticket_id=ticket.id)

        # Return Status with id = None if no ticket currently queued
        return StudentQueuedTicketStatus(ticket_id=None)

    def _find_ticket_position(
        self, tickets_list: list[OfficeHoursTicketEntity], ticket_id: int
    ) -> int:
        """Find the position (1-based index) of a ticket in a list by ticket ID.

        Args:
            tickets_list (list[OfficeHoursTicketEntity]): List of OfficeHoursTicketEntity objects.
            ticket_id (int): ID of the ticket to find.

        Returns:
            int: 1-based index of the ticket in the list if found; otherwise, returns -1.
        """
        for index, ticket in enumerate(tickets_list, start=1):
            if ticket.id == ticket_id:
                return index
        return -1

    def _get_called_tickets_by_oh_event(
        self, oh_event_id: int
    ) -> list[OfficeHoursTicketEntity]:
        """Retrieve a list of called tickets for a specific office hours event.

        Args:
            oh_event_id (int): ID of the office hours event.

        Returns:
            list[OfficeHoursTicketEntity]: List of OfficeHoursTicketEntity objects
                that are in the 'CALLED' state for the specified event.
        """
        # Fetch Called Tickets
        called_tickets_query = (
            select(OfficeHoursTicketEntity)
            .filter(OfficeHoursTicketEntity.oh_event_id == oh_event_id)
            .filter(OfficeHoursTicketEntity.state == TicketState.CALLED)
        )

        called_ticket_entities = self._session.scalars(called_tickets_query).all()

        # Return the entities
        return called_ticket_entities

    def _get_queued_tickets_by_oh_event(
        self, oh_event_id: int
    ) -> list[OfficeHoursTicketEntity]:
        """Retrieve a list of queued tickets for a specific office hours event.

        Args:
            oh_event_id (int): ID of the office hours event.

        Returns:
            list[OfficeHoursTicketEntity]: List of OfficeHoursTicketEntity objects
                that are in the 'QUEUED' state for the specified event, ordered by ticket ID.
        """
        # Fetch Queued Tickets
        queued_tickets_query = (
            select(OfficeHoursTicketEntity)
            .filter(OfficeHoursTicketEntity.oh_event_id == oh_event_id)
            .filter(OfficeHoursTicketEntity.state == TicketState.QUEUED)
            .order_by(OfficeHoursTicketEntity.id)
        )

        queued_ticket_entities = self._session.scalars(queued_tickets_query).all()

        # Return the entities
        return queued_ticket_entities

    def _check_user_section_permissions(
        self, user_id: int, oh_section_id: int, student_acess: bool = False
    ) -> SectionMemberEntity:
        """
        Check user permissions for a specific office hours section.

        Args:
            user_id (int): The ID of the user whose permissions are being checked.
            oh_section_id (int): The ID of the office hours section to check permissions for.
            student_access (bool, optional): Flag indicating whether student access is allowed.
                Defaults to False.

        Returns:
            SectionMemberEntity: An entity representing the user's membership status in the section.

        Raises:
            PermissionError: If subject is not a member or student access is not allowed and the user is a student.
        """

        section_member_entity = self._check_user_section_membership(
            user_id, oh_section_id
        )

        if (
            not student_acess
            and section_member_entity.member_role == RosterRole.STUDENT
        ):
            raise PermissionError(
                f"Section Member is a Student. User does not have permision for this action."
            )
        return section_member_entity

    def _check_user_section_membership(
        self,
        user_id: int,
        oh_section_id: int,
    ) -> SectionMemberEntity:
        """Checks if a given user is a member in the academic section associate with given office hours section ID.

        Note: An Office Hours section can have multiple academic sections assoicated with it.

        Args:
            user_id (int): The id of given User of interest
            oh_section_id (int): The id of office hours section.
        Returns:
            SectionMemberEntity: `SectionMemberEntity` associated with a given user and academic section

        Raises:
            PermissionError: If cannot find user in given academic section.
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

        # Return the entity
        return section_member_entity

    def _get_recurring_weekday_dates(
        self, start_date: date, end_date: date, weekdays: list[Weekday]
    ) -> list[date]:
        """
        Get recurring weekday dates within a specified date range.

        Args:
            start_date (date): The start date of the date range.
            end_date (date): The end date of the date range.
            weekdays (list[Weekday]): A list of Weekday enum values representing
                the weekdays to include.

        Returns:
            list[date]: A list of date objects representing the recurring
                weekday dates within the specified range.
        """
        dates_in_range = []
        current_date = start_date

        weekday_names: list[str] = [weekday.name.lower() for weekday in weekdays]
        # Iterate through each date in the range
        while current_date <= end_date:
            # Check if the current date falls on any of the desired weekdays
            if current_date.strftime("%A").lower() in weekday_names:
                dates_in_range.append(current_date)
            # Move to the next day
            current_date += timedelta(days=1)

        return dates_in_range

    def _transform_date(self, orginal_date: datetime, new_event_date: date) -> datetime:
        """
        Transform a datetime object to a new date while preserving time components.

        Args:
            orginal_date (datetime): The original datetime object to transform.
            new_event_date (date): The new date to set while preserving time components.

        Returns:
            datetime: A new datetime object with the date components from new_event_date
                and the time components from orginal_date.
        """
        # Extract time components from the original datetime
        hour = orginal_date.hour
        minute = orginal_date.minute

        # Combine the new date with the time components
        new_datetime = datetime.combine(new_event_date, datetime.min.time())

        # Set the time components to the new datetime
        new_datetime = new_datetime.replace(hour=hour, minute=minute)

        return new_datetime
