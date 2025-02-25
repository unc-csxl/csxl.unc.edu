from datetime import datetime
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func, select, and_, func

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
                OfficeHoursTicketEntity.start >= datetime.fromisoformat(range_start),
                OfficeHoursTicketEntity.start <= datetime.fromisoformat(range_end),
            )
            statement = statement.where(criteria)
            length_statement = length_statement.where(criteria)

        # Filter by student who created ticket
        if len(pagination_params.student_ids) != 0:
            statement = (
                statement.join(user_created_tickets_table)
                .join(SectionMemberEntity)
                .where(SectionMemberEntity.user_id.in_(pagination_params.student_ids))
            )
            length_statement = (
                length_statement.join(user_created_tickets_table)
                .join(SectionMemberEntity)
                .where(SectionMemberEntity.user_id.in_(pagination_params.student_ids))
            )

        # Filter by staff member who called ticket
        if len(pagination_params.staff_ids) != 0:
            statement = statement.join(SectionMemberEntity).where(
                SectionMemberEntity.user_id.in_(pagination_params.staff_ids)
            )
            length_statement = length_statement.join(SectionMemberEntity).where(
                SectionMemberEntity.user_id.in_(pagination_params.staff_ids)
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
