from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased, joinedload
from sqlalchemy import func, select, and_, func, Select

from backend.entities.academics.section_entity import SectionEntity
from backend.entities.user_entity import UserEntity
from backend.models.roster_role import RosterRole

from ...models.office_hours.office_hours_statistics import StatisticsFilterData
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
from ...models.academics.my_courses import (
    CourseMemberOverview,
    OfficeHourTicketOverview,
)
from ...services.office_hours.office_hours import OfficeHoursService


__authors__ = ["Ajay Gandecha", "Jade Keegan", "Mira Mohan", "Lauren Ferlito"]
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
    ) -> tuple[Select, Select]:
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
        if pagination_params.range_start != "" and pagination_params.range_end != "":
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
        # Create a subquery from statement
        stmt_subquery = statement.subquery()

        # Create an alias to reference the subquery's columns
        ticket_alias = aliased(OfficeHoursTicketEntity, stmt_subquery)

        # Total tickets
        result = self._session.execute(length_statement).scalar()
        total_tickets = float(result) if result is not None else 0

        # Total tickets per week
        today = datetime.today()
        start_of_week = (
            today - timedelta(days=today.weekday() + 1)
            if today.weekday() != 6
            else today
        )

        week_tickets_statement = (
            select(func.count())
            .select_from(stmt_subquery)
            .where(ticket_alias.created_at >= start_of_week)
        )
        result = self._session.execute(week_tickets_statement).scalar()
        week_tickets = float(result) if result is not None else 0

        # Avg wait time
        avg_wait_time_statement = (
            select(
                func.avg(
                    func.extract(
                        "epoch",
                        ticket_alias.called_at - ticket_alias.created_at,
                    )
                )
            )
            .select_from(stmt_subquery)
            .where(ticket_alias.called_at.isnot(None))
        )

        result = self._session.execute(avg_wait_time_statement).scalar()
        avg_wait_time = float(result) if result is not None else 0

        avg_wait_time_minutes = avg_wait_time / 60 if avg_wait_time else 0

        # Avg duration
        avg_duration_statement = (
            select(
                func.avg(
                    func.extract(
                        "epoch",
                        ticket_alias.closed_at - ticket_alias.called_at,
                    )
                )
            )
            .select_from(stmt_subquery)
            .where(ticket_alias.closed_at.isnot(None))
        )
        result = self._session.execute(avg_duration_statement).scalar()
        avg_duration = float(result) if result is not None else 0

        avg_duration_minutes = avg_duration / 60 if avg_duration else 0

        # Total conceptual
        conceptual_help_statement = (
            select(func.count())
            .select_from(stmt_subquery)
            .where(ticket_alias.type == TicketType.CONCEPTUAL_HELP)
        )
        result = self._session.execute(conceptual_help_statement).scalar()
        total_conceptual_help = float(result) if result is not None else 0

        # Total assignment
        assignment_help_statement = (
            select(func.count())
            .select_from(stmt_subquery)
            .where(ticket_alias.type == TicketType.ASSIGNMENT_HELP)
        )
        result = self._session.execute(assignment_help_statement).scalar()
        total_assignment_help = float(result) if result is not None else 0

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

        statement, length_statement = self.create_ticket_query(
            site_id, pagination_params
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
            items=[entity.to_overview_model() for entity in entities],
            length=length,
            params=pagination_params,
        )

    def get_filter_data(self, user: User, site_id: int) -> StatisticsFilterData:
        self._office_hours_svc._check_site_admin_permissions(user, site_id)

        student_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .join(UserEntity)
            .where(SectionEntity.course_site_id == site_id)
            .where(SectionMemberEntity.member_role == RosterRole.STUDENT)
            .options(joinedload(SectionMemberEntity.section))
            .options(joinedload(SectionMemberEntity.user))
        )
        students = self._session.scalars(student_query).unique().all()

        staff_query = (
            select(SectionMemberEntity)
            .join(SectionEntity)
            .join(UserEntity)
            .where(SectionEntity.course_site_id == site_id)
            .where(
                SectionMemberEntity.member_role.in_(
                    [RosterRole.UTA, RosterRole.GTA, RosterRole.INSTRUCTOR]
                )
            )
            .options(joinedload(SectionMemberEntity.section))
            .options(joinedload(SectionMemberEntity.user))
        )
        staff = self._session.scalars(staff_query).unique().all()

        term = self._session.get(CourseSiteEntity, site_id).term

        return StatisticsFilterData(
            students=list(
                set([student.user.to_public_model() for student in students])
            ),
            staff=list(set([member.user.to_public_model() for member in staff])),
            term_start=term.start,
            term_end=term.end,
        )
