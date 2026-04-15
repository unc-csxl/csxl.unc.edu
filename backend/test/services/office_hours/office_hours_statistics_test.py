"""Tests for the OfficeHoursStatisticsService."""

from datetime import datetime, timedelta

import pytest
from pytest import approx
from sqlalchemy.orm import Session

from ....entities.academics.section_member_entity import SectionMemberEntity
from ....entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ....entities.user_entity import UserEntity
from ....models.academics.section_member import SectionMemberDraft
from ....models.office_hours.ticket_type import TicketType
from ....models.pagination import TicketPaginationParams
from ....models.roster_role import RosterRole
from ....models.user import User
from ....services.exceptions import CoursePermissionException
from ....services.office_hours import OfficeHoursService, OfficeHoursStatisticsService
from ..reset_table_id_seq import reset_table_id_seq
from .scenario import arrange_office_hours_scenario

__authors__ = ["Jade Keegan", "Ajay Gandecha", "Mira Mohan", "Lauren Ferlito"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def make_statistics_service(session: Session) -> OfficeHoursStatisticsService:
    return OfficeHoursStatisticsService(session, OfficeHoursService(session))


def make_ticket_params(
    *,
    range_start: str = "",
    range_end: str = "",
    student_ids: list[int] | None = None,
    staff_ids: list[int] | None = None,
) -> TicketPaginationParams:
    return TicketPaginationParams(
        range_start=range_start,
        range_end=range_end,
        student_ids=student_ids or [],
        staff_ids=staff_ids or [],
    )


def arrange_extra_member(
    session: Session,
    scenario,
    *,
    user_id: int,
    onyen: str,
    member_role: RosterRole,
) -> SectionMemberEntity:
    user = User(
        id=user_id,
        pid=user_id,
        onyen=onyen,
        first_name=onyen.title(),
        last_name="Member",
        email=f"{onyen}@unc.edu",
    )
    session.add(UserEntity.from_model(user))
    session.flush()

    membership = SectionMemberEntity.from_draft_model(
        SectionMemberDraft(
            section_id=scenario.section.id,
            user_id=user.id,
            member_role=member_role,
        )
    )
    session.add(membership)
    session.flush()
    return membership


def arrange_statistics_extension(session: Session, scenario) -> None:
    now = datetime.now().replace(microsecond=0)

    base_closed_ticket = session.get(OfficeHoursTicketEntity, scenario.closed_ticket.id)
    assert base_closed_ticket is not None
    base_closed_ticket.type = TicketType.CONCEPTUAL_HELP
    base_closed_ticket.created_at = now - timedelta(minutes=3)
    base_closed_ticket.called_at = now - timedelta(minutes=2)
    base_closed_ticket.closed_at = now - timedelta(minutes=1)

    arrange_extra_member(
        session,
        scenario,
        user_id=5,
        onyen="helper",
        member_role=RosterRole.STUDENT,
    )
    arrange_extra_member(
        session,
        scenario,
        user_id=6,
        onyen="uta",
        member_role=RosterRole.UTA,
    )

    additional_tickets = []
    for ticket_id, created_minutes, called_minutes, closed_minutes in [
        (5, 6, 5, 4),
        (6, 9, 8, 7),
    ]:
        ticket = scenario.closed_ticket.model_copy(
            update={
                "id": ticket_id,
                "description": f"Closed ticket {ticket_id}",
                "type": TicketType.CONCEPTUAL_HELP,
                "created_at": now - timedelta(minutes=created_minutes),
                "called_at": now - timedelta(minutes=called_minutes),
                "closed_at": now - timedelta(minutes=closed_minutes),
                "caller_id": scenario.instructor_membership.id,
            }
        )
        ticket_entity = OfficeHoursTicketEntity.from_model(ticket)
        ticket_entity.creators = [scenario.student_membership]
        ticket_entity.caller = scenario.instructor_membership
        additional_tickets.append(ticket_entity)

    session.add_all(additional_tickets)
    session.flush()
    reset_table_id_seq(
        session,
        SectionMemberEntity,
        SectionMemberEntity.id,
        7,
    )
    reset_table_id_seq(
        session,
        OfficeHoursTicketEntity,
        OfficeHoursTicketEntity.id,
        7,
    )
    session.commit()


def make_wide_range() -> tuple[str, str]:
    now = datetime.now().replace(microsecond=0)
    return (
        (now - timedelta(days=365)).isoformat(),
        (now + timedelta(days=365)).isoformat(),
    )


def test_get_paginated_tickets(session: Session):
    """Ensures that users with the appropriate site permissions can get paginated tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act
    ticket_history = oh_statistics_svc.get_paginated_tickets(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert len(ticket_history.items) == 3


def test_get_paginated_tickets_not_staff(
    session: Session,
):
    """Ensures that users without the appropriate site permissions cannot get paginated tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_statistics_svc.get_paginated_tickets(
            scenario.student,
            scenario.course_site.id,
            ticket_params,
        )


def test_get_statistics(session: Session):
    """Ensures that users with the appropriate site permissions can get statistics."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act
    statistics = oh_statistics_svc.get_statistics(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert statistics.total_tickets == 3
    assert statistics.total_tickets_weekly == 3
    assert statistics.average_wait_time == approx(1.0)
    assert statistics.average_duration == approx(1.0)
    assert statistics.total_conceptual == 3
    assert statistics.total_assignment == 0


def test_get_paginated_tickets_student_filter(
    session: Session,
):
    """Ensures that filtering by student works correctly."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params(student_ids=[scenario.student.id])

    # Act
    ticket_history = oh_statistics_svc.get_paginated_tickets(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert (
        len(ticket_history.items) == 3
        and ticket_history.items[0].creators[0].id == scenario.student.id
    )


def test_get_paginated_tickets_staff_filter(
    session: Session,
):
    """Ensures that filtering by staff works correctly."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params(staff_ids=[scenario.instructor.id])

    # Act
    ticket_history = oh_statistics_svc.get_paginated_tickets(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert (
        len(ticket_history.items) == 3
        and ticket_history.items[0].caller.id == scenario.instructor.id
    )


def test_get_statistics_staff_filter(session: Session):
    """Ensures that filtering by student returns corrcet statistcs."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params(staff_ids=[scenario.instructor.id])

    # Act
    statistics = oh_statistics_svc.get_statistics(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert statistics.total_tickets == 3
    assert statistics.total_tickets_weekly == 3
    assert statistics.average_wait_time == approx(1.0)
    assert statistics.average_duration == approx(1.0)
    assert statistics.total_conceptual == 3
    assert statistics.total_assignment == 0


def test_get_paginated_tickets_date_filter(
    session: Session,
):
    """Ensures that filtering by date works correctly."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    range_start, range_end = make_wide_range()
    ticket_params = make_ticket_params(range_start=range_start, range_end=range_end)

    # Act
    ticket_history = oh_statistics_svc.get_paginated_tickets(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert len(ticket_history.items) == 3


def test_get_statistics_date_filter(
    session: Session,
):
    """Ensures that filtering by date returns correct statistics."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    range_start, range_end = make_wide_range()
    ticket_params = make_ticket_params(range_start=range_start, range_end=range_end)

    # Act
    statistics = oh_statistics_svc.get_statistics(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert statistics.total_tickets == 3
    assert statistics.total_tickets_weekly == 3
    assert statistics.average_wait_time == approx(1.0)
    assert statistics.average_duration == approx(1.0)
    assert statistics.total_conceptual == 3
    assert statistics.total_assignment == 0


def test_get_paginated_tickets_unauthenticated(
    session: Session,
):
    """Ensures that filtering by date works correctly."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_statistics_svc.get_paginated_tickets(
            scenario.student,
            scenario.course_site.id,
            ticket_params,
        )


def test_get_statistics_unauthenticated(
    session: Session,
):
    """Ensures that students cannot view statistics."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_statistics_svc.get_statistics(
            scenario.student,
            scenario.course_site.id,
            ticket_params,
        )


def test_get_statistics_filter_options(session: Session):
    """Ensures that instructors can get the filter options for the statistics page."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)

    # Act
    filter_data = oh_statistics_svc.get_filter_data(
        scenario.instructor,
        scenario.course_site.id,
    )

    # Assert
    assert len(filter_data.students) == 2
    assert len(filter_data.staff) == 2


def test_get_statistics_filter_options_no_permissions(
    session: Session,
):
    """Ensures that students are not able to get the filter options for the statistics page."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_statistics_svc.get_filter_data(
            scenario.student,
            scenario.course_site.id,
        )


def test_get_statistics_multiple_filters(session: Session):
    """Ensures that multiple filters can be applied at the same time."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    range_start, range_end = make_wide_range()
    ticket_params = make_ticket_params(
        range_start=range_start,
        range_end=range_end,
        student_ids=[scenario.student.id],
        staff_ids=[scenario.instructor.id],
    )

    # Act
    statistics = oh_statistics_svc.get_statistics(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert statistics.total_tickets == 3
    assert statistics.total_tickets_weekly == 3
    assert statistics.average_wait_time == approx(1.0)
    assert statistics.average_duration == approx(1.0)
    assert statistics.total_conceptual == 3
    assert statistics.total_assignment == 0


def test_get_ticket_csv(
    session: Session,
):
    """Ensures that the CSV file is generated correctly."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act
    ticket_csv = oh_statistics_svc.get_ticket_csv(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert len(ticket_csv) == 3


def test_get_ticket_csv_unauthenticated(
    session: Session,
):
    """Ensures that students cannot view the CSV file."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params()

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_statistics_svc.get_ticket_csv(
            scenario.student,
            scenario.course_site.id,
            ticket_params,
        )


def test_get_ticket_csv_with_filters(
    session: Session,
):
    """Ensures that the CSV file is generated correctly with filters."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    arrange_statistics_extension(session, scenario)
    oh_statistics_svc = make_statistics_service(session)
    ticket_params = make_ticket_params(
        student_ids=[scenario.student.id],
        staff_ids=[scenario.instructor.id],
    )

    # Act
    ticket_csv = oh_statistics_svc.get_ticket_csv(
        scenario.instructor,
        scenario.course_site.id,
        ticket_params,
    )

    # Assert
    assert len(ticket_csv) == 3
