from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, select, and_, func

from backend.models.office_hours.ticket_type import TicketType

from ...models.office_hours.ticket_state import TicketState

from ...entities.academics.section_member_entity import SectionMemberEntity
from ...entities.office_hours import user_created_tickets_table
from ...entities.office_hours.course_site_entity import CourseSiteEntity
from ...entities.office_hours.office_hours_entity import OfficeHoursEntity

from ...database import db_session

from ...entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ...models.pagination import Paginated, TicketPaginationParams
from ...models.user import User
from ...models.academics.my_courses import OfficeHourTicketOverview
from ...services.office_hours.office_hours import OfficeHoursService


__authors__ = ["Ajay Gandecha", "Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OfficeHoursStatisticsService:
    """
    Service that performs all of the actions for office hour tickets.
    """

    def __init__(
        self,
        session: Session = Depends(db_session),
        _office_hours_svc: OfficeHoursService = Depends(),
    ):
        """
        Initializes the database session.
        """
        self._session = session
        self._office_hours_svc = _office_hours_svc

    def apply_filters(
        self, statement: Select, site_id: int, pagination_params: TicketPaginationParams
    ):
        """
        Apply filters to the given statement based on the pagination parameters.
        """
        # Alias the section member entity so that we can join to this table
        # multiple times. The `CreatorEntity` alias will be used for filtering
        # based on the ticket creators, and the `CallerEntity` alias will
        # be used for filtering staff members.
        CreatorEntity = aliased(SectionMemberEntity)
        CallerEntity = aliased(SectionMemberEntity)

        # Filter by Start/End Range
        if pagination_params.range_start != "":
            range_start = pagination_params.range_start
            range_end = pagination_params.range_end
            criteria = and_(
                OfficeHoursTicketEntity.created_at
                >= datetime.fromisoformat(range_start),
                OfficeHoursTicketEntity.created_at <= datetime.fromisoformat(range_end),
            )
            statement = statement.where(criteria)

        # Filter by student who created ticket
        if len(pagination_params.student_ids) != 0:
            statement = (
                statement.join(user_created_tickets_table)
                .join(
                    CreatorEntity,
                    CreatorEntity.id
                    == user_created_tickets_table.c.member_id,  # why no definition
                )
                .where(CreatorEntity.user_id.in_(pagination_params.student_ids))
            )

        # Filter by staff member who called ticket
        if len(pagination_params.staff_ids) != 0:
            statement = statement.join(
                CallerEntity,
                CallerEntity.id == OfficeHoursTicketEntity.caller_id,
            ).where(CallerEntity.user_id.in_(pagination_params.staff_ids))

        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        # Retrieve limited items
        statement = statement.offset(offset).limit(limit)

        return statement

    def get_paginated_tickets(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> Paginated[OfficeHourTicketOverview]:
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        statement = (
            select(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
        )

        statement = self.apply_filters(statement, site_id, pagination_params)

        length_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
        )
        length_statement = self.apply_filters(
            length_statement, site_id, pagination_params
        )

        # Calculate where to begin retrieving rows and how many to retrieve
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        # Retrieve limited items
        statement = statement.offset(offset).limit(limit)

        # Execute statement and retrieve entities
        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        # Convert `UserEntity`s to model and return page
        return Paginated(
            items=[
                entity.to_overview_model() for entity in entities
            ],  # why no definition
            length=length,
            params=pagination_params,
        )

    def get_ticket_count(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> int:
        """
        Retrieve the total number of filtered tickets created for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        total_tickets_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
        )
        total_tickets_statement = self.apply_filters(
            total_tickets_statement, site_id, pagination_params
        )
        total_tickets = self._session.execute(total_tickets_statement).scalar()
        return total_tickets

    def get_week_ticket_count(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> int:
        """
        Retrieve the total number of tickets, for the current week, created for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        week_tickets_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.created_at >= start_of_week)
        )
        week_tickets_statement = self.apply_filters(
            week_tickets_statement, site_id, pagination_params
        )
        week_tickets = self._session.execute(week_tickets_statement).scalar()
        return week_tickets

    def get_average_wait(self, user: User, site_id: int) -> int:
        """
        Retrieve the average wait time of tickets for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        avg_wait_time_statement = (
            select(
                func.avg(
                    func.extract(
                        "epoch",
                        OfficeHoursTicketEntity.called_at
                        - OfficeHoursTicketEntity.created_at,
                    )
                )
            )
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.called_at.isnot(None))
        )
        avg_wait_time_statement = self.apply_filters(
            avg_wait_time_statement, site_id, pagination_params
        )
        avg_wait_time = self._session.execute(avg_wait_time_statement).scalar()
        avg_wait_time_minutes = avg_wait_time / 60 if avg_wait_time else 0
        return avg_wait_time_minutes

    def get_average_duration(self, user: User, site_id: int) -> int:
        """
        Retrieve the average duration of tickets for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        avg_duration_statement = (
            select(
                func.avg(
                    func.extract(
                        "epoch",
                        OfficeHoursTicketEntity.closed_at
                        - OfficeHoursTicketEntity.called_at,
                    )
                )
            )
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.closed_at.isnot(None))
        )
        avg_duration_statement = self.apply_filters(
            avg_duration_statement, site_id, pagination_params
        )
        avg_duration = self._session.execute(avg_duration_statement).scalar()
        avg_duration_minutes = avg_duration / 60 if avg_duration else 0
        return avg_duration_minutes

    def total_assignment_help(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> int:
        """
        Retrieve the total number of 'Assignment Help' tickets for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        assignment_help_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.type == TicketType.ASSIGNMENT_HELP)
        )
        assignment_help_statement = self.apply_filters(
            assignment_help_statement, site_id, pagination_params
        )
        total_assignment_help = self._session.execute(
            assignment_help_statement
        ).scalar()
        return total_assignment_help

    def total_conceptual_help(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> int:
        """
        Retrieve the total number of 'Conceptual Help' tickets for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        conceptual_help_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.type == TicketType.CONCEPTUAL_HELP)
        )
        conceptual_help_statement = self.apply_filters(
            conceptual_help_statement, site_id, pagination_params
        )
        total_conceptual_help = self._session.execute(
            conceptual_help_statement
        ).scalar()
        return total_conceptual_help
