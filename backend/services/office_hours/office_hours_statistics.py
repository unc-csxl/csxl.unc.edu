from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, select, and_, func

from backend.models.office_hours.ticket_statistics import OfficeHoursTicketStatistics
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

    def create_ticket_query(
        self, site_id: int, pagination_params: TicketPaginationParams
    ) -> tuple:
        """
        Create the ticket query based on the filters selected.
        """
        # Alias the section member entity so that we can join to this table
        # multiple times. The `CreatorEntity` alias will be used for filtering
        # based on the ticket creators, and the `CallerEntity` alias will
        # be used for filtering staff members.
        CreatorEntity = aliased(SectionMemberEntity)
        CallerEntity = aliased(SectionMemberEntity)

        statement = (
            select(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
        )

        length_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
        )

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
            length_statement = length_statement.where(criteria)

        # Filter by student who created ticket
        if len(pagination_params.student_ids) != 0:
            statement = (
                statement.join(user_created_tickets_table)
                .join(
                    CreatorEntity,
                    CreatorEntity.id == user_created_tickets_table.c.member_id,
                )
                .where(CreatorEntity.user_id.in_(pagination_params.student_ids))
            )
            length_statement = (
                length_statement.join(user_created_tickets_table)
                .join(
                    CreatorEntity,
                    CreatorEntity.id == user_created_tickets_table.c.member_id,
                )
                .where(CreatorEntity.user_id.in_(pagination_params.student_ids))
            )

        # Filter by staff member who called ticket
        if len(pagination_params.staff_ids) != 0:
            statement = statement.join(
                CallerEntity,
                CallerEntity.id == OfficeHoursTicketEntity.caller_id,
            ).where(CallerEntity.user_id.in_(pagination_params.staff_ids))
            length_statement = length_statement.join(
                CallerEntity,
                CallerEntity.id == OfficeHoursTicketEntity.caller_id,
            ).where(CallerEntity.user_id.in_(pagination_params.staff_ids))

        return statement, length_statement

    def get_statistics(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> OfficeHoursTicketStatistics:
        """
        Retrieve various statistics for a course site.
        """
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Call create_ticket_query to get the statements
        statement, length_statement = self.create_ticket_query(
            site_id, pagination_params
        )

        # Total tickets
        total_tickets = self._session.execute(length_statement).scalar()

        # Total tickets per week
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        week_tickets_statement = statement.where(
            OfficeHoursTicketEntity.created_at >= start_of_week
        )
        week_tickets = self._session.execute(week_tickets_statement).scalar()

        # Avg wait time
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
        avg_wait_time = self._session.execute(avg_wait_time_statement).scalar()
        avg_wait_time_minutes = avg_wait_time / 60 if avg_wait_time else 0

        # Avg duration
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
        avg_duration = self._session.execute(avg_duration_statement).scalar()
        avg_duration_minutes = avg_duration / 60 if avg_duration else 0

        # Total conceptual
        conceptual_help_statement = statement.where(
            OfficeHoursTicketEntity.type == TicketType.CONCEPTUAL_HELP
        )
        total_conceptual_help = self._session.execute(
            conceptual_help_statement
        ).scalar()

        # Total assignment
        assignment_help_statement = statement.where(
            OfficeHoursTicketEntity.type == TicketType.ASSIGNMENT_HELP
        )
        total_assignment_help = self._session.execute(
            assignment_help_statement
        ).scalar()

        return OfficeHoursTicketStatistics(
            total_tickets=total_tickets,
            total_tickets_weekly=week_tickets,
            average_wait_time=avg_wait_time_minutes,
            average_duration=avg_duration_minutes,
            total_conceptual=total_conceptual_help,
            total_assignment=total_assignment_help,
        )

    def get_paginated_tickets(
        self, user: User, site_id: int, pagination_params: TicketPaginationParams
    ) -> Paginated[OfficeHourTicketOverview]:
        # Check permissions
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        # Alias the section member entity so that we can join to this table
        # multiple times. The `CreatorEntity` alias will be used for filtering
        # based on the ticket creators, and the `CallerEntity` alias will
        # be used for filtering staff members.
        CreatorEntity = aliased(SectionMemberEntity)
        CallerEntity = aliased(SectionMemberEntity)

        statement = (
            select(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
        )

        length_statement = (
            select(func.count())
            .select_from(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(CourseSiteEntity)
            .where(CourseSiteEntity.id == site_id)
            .where(OfficeHoursTicketEntity.state == TicketState.CLOSED)
        )

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
            length_statement = length_statement.where(criteria)

        # Filter by student who created ticket
        if len(pagination_params.student_ids) != 0:
            statement = (
                statement.join(user_created_tickets_table)
                .join(
                    CreatorEntity,
                    CreatorEntity.id == user_created_tickets_table.c.member_id,
                )
                .where(CreatorEntity.user_id.in_(pagination_params.student_ids))
            )
            length_statement = (
                length_statement.join(user_created_tickets_table)
                .join(
                    CreatorEntity,
                    CreatorEntity.id == user_created_tickets_table.c.member_id,
                )
                .where(CreatorEntity.user_id.in_(pagination_params.student_ids))
            )

        # Filter by staff member who called ticket
        if len(pagination_params.staff_ids) != 0:
            statement = statement.join(
                CallerEntity,
                CallerEntity.id == OfficeHoursTicketEntity.caller_id,
            ).where(CallerEntity.user_id.in_(pagination_params.staff_ids))
            length_statement = length_statement.join(
                CallerEntity,
                CallerEntity.id == OfficeHoursTicketEntity.caller_id,
            ).where(CallerEntity.user_id.in_(pagination_params.staff_ids))

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
            items=[entity.to_overview_model() for entity in entities],
            length=length,
            params=pagination_params,
        )
