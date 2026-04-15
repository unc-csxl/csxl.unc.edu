"""Tests for the OfficeHoursTicketService."""

from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from ....models.academics.my_courses import OfficeHourTicketOverview
from ....models.academics.section import Section
from ....models.academics.section_member import SectionMemberDraft
from ....models.office_hours.course_site import CourseSite
from ....models.office_hours.ticket import (
    NewOfficeHoursTicket,
    OfficeHoursTicketClosePayload,
)
from ....models.office_hours.ticket import TicketState
from ....models.office_hours.ticket_type import TicketType
from ....models.roster_role import RosterRole
from ....models.user import User
from ....entities.academics.section_entity import SectionEntity
from ....entities.academics.section_member_entity import SectionMemberEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ....entities.user_entity import UserEntity
from ....services.office_hours import OfficeHourTicketService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException
from ..reset_table_id_seq import reset_table_id_seq
from .scenario import arrange_office_hours_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def make_office_hours_ticket_service(session: Session) -> OfficeHourTicketService:
    return OfficeHourTicketService(session)


def make_close_payload() -> OfficeHoursTicketClosePayload:
    return OfficeHoursTicketClosePayload(
        has_concerns=True,
        caller_notes="I have concerns.",
    )


def arrange_additional_student(
    session: Session, section_id: int, user_id: int, onyen: str
) -> User:
    user = User(
        id=user_id,
        pid=user_id,
        onyen=onyen,
        first_name=onyen.title(),
        last_name="Student",
        email=f"{onyen}@unc.edu",
    )
    session.add(UserEntity.from_model(user))
    session.flush()

    membership = SectionMemberEntity.from_draft_model(
        SectionMemberDraft(
            section_id=section_id,
            user_id=user.id,
            member_role=RosterRole.STUDENT,
        )
    )
    session.add(membership)
    session.flush()
    reset_table_id_seq(
        session, SectionMemberEntity, SectionMemberEntity.id, membership.id + 1
    )
    session.commit()
    return user


def arrange_policy_ticket_request(
    session: Session,
    scenario,
    *,
    site_id: int,
    section_id: int,
    event_id: int,
    closed_ticket_id: int,
    minimum_ticket_cooldown: int = 0,
    max_tickets_per_day: int = 100,
    closed_offset_minutes: int = 0,
) -> NewOfficeHoursTicket:
    site_entity = CourseSiteEntity(
        id=site_id,
        title=f"Policy Site {site_id}",
        term_id=scenario.course_site.term_id,
        minimum_ticket_cooldown=minimum_ticket_cooldown,
        max_tickets_per_day=max_tickets_per_day,
    )
    session.add(site_entity)

    section = Section(
        id=section_id,
        course_id=scenario.section.course_id,
        number=f"{section_id:03d}",
        term_id=scenario.section.term_id,
        meeting_pattern="MWF 10:00-10:50",
        override_title="",
        override_description="",
        enrolled=1,
        total_seats=30,
    )
    section_entity = SectionEntity.from_model(section)
    section_entity.course_site_id = site_id
    session.add(section_entity)
    session.flush()

    instructor_membership = SectionMemberEntity.from_draft_model(
        SectionMemberDraft(
            section_id=section.id,
            user_id=scenario.instructor.id,
            member_role=RosterRole.INSTRUCTOR,
        )
    )
    student_membership = SectionMemberEntity.from_draft_model(
        SectionMemberDraft(
            section_id=section.id,
            user_id=scenario.student.id,
            member_role=RosterRole.STUDENT,
        )
    )
    session.add_all([instructor_membership, student_membership])
    session.flush()

    event = scenario.current_office_hours.model_copy(
        update={
            "id": event_id,
            "course_site_id": site_id,
        }
    )
    session.add(OfficeHoursEntity.from_model(event))
    session.flush()

    closed_ticket = scenario.closed_ticket.model_copy(
        update={
            "id": closed_ticket_id,
            "office_hours_id": event.id,
            "caller_id": instructor_membership.id,
            "closed_at": datetime.now().replace(microsecond=0)
            - timedelta(minutes=closed_offset_minutes),
        }
    )
    closed_ticket_entity = OfficeHoursTicketEntity.from_model(closed_ticket)
    closed_ticket_entity.creators = [student_membership]
    closed_ticket_entity.caller = instructor_membership
    session.add(closed_ticket_entity)

    reset_table_id_seq(session, CourseSiteEntity, CourseSiteEntity.id, site_id + 1)
    reset_table_id_seq(session, SectionEntity, SectionEntity.id, section_id + 1)
    reset_table_id_seq(
        session,
        SectionMemberEntity,
        SectionMemberEntity.id,
        student_membership.id + 1,
    )
    reset_table_id_seq(session, OfficeHoursEntity, OfficeHoursEntity.id, event_id + 1)
    reset_table_id_seq(
        session,
        OfficeHoursTicketEntity,
        OfficeHoursTicketEntity.id,
        closed_ticket_id + 1,
    )
    session.commit()

    return NewOfficeHoursTicket(
        description="Help me!",
        type=scenario.queued_ticket.type,
        office_hours_id=event.id,
    )


# Call Ticket Tests


def test_call_ticket(session: Session):
    """Ensures that instructors can call tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act
    called = oh_ticket_svc.call_ticket(scenario.instructor, scenario.queued_ticket.id)

    # Assert
    assert called.state == TicketState.CALLED.to_string()
    assert called.caller.id == scenario.instructor.id


def test_call_ticket_already_called(session: Session):
    """Ensures an error is thrown when a ticket has already been called."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(scenario.instructor, scenario.called_ticket.id)


@pytest.mark.parametrize("ticket_attr", ["closed_ticket", "cancelled_ticket"])
def test_call_ticket_not_queued(session: Session, ticket_attr: str):
    """Ensures that only queued tickets can be called."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(
            scenario.instructor, getattr(scenario, ticket_attr).id
        )


def test_call_ticket_not_found(session: Session):
    """Ensures that an error is thrown if attempting to call a ticket that does not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.call_ticket(scenario.instructor, 404)


def test_call_ticket_not_member(session: Session):
    """Ensures that non-members cannot call tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(scenario.ambassador, scenario.queued_ticket.id)


def test_call_ticket_not_staff(session: Session):
    """Ensures that non-staff members cannot call tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.call_ticket(scenario.student, scenario.queued_ticket.id)


# Cancel Ticket Tests


def test_cancel_ticket(session: Session):
    """Ensures that instructors can cancel tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act
    called = oh_ticket_svc.cancel_ticket(scenario.instructor, scenario.queued_ticket.id)

    # Assert
    assert called.state == TicketState.CANCELED.to_string()


def test_cancel_ticket_not_found(session: Session):
    """Ensures that an error is thrown if attempting to cancel a ticket that does not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.cancel_ticket(scenario.instructor, 404)


def test_cancel_ticket_not_member(session: Session):
    """Ensures that non-members cannot cancel tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.cancel_ticket(scenario.ambassador, scenario.queued_ticket.id)


def test_cancel_ticket_student(session: Session):
    """Ensures that students can cancel tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act
    called = oh_ticket_svc.cancel_ticket(scenario.student, scenario.queued_ticket.id)

    # Assert
    assert called.state == TicketState.CANCELED.to_string()


def test_open_ticket_requires_course_site(session: Session):
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    new_ticket = NewOfficeHoursTicket(
        description="Need help",
        type=TicketType.CONCEPTUAL_HELP,
        office_hours_id=404,
    )

    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(scenario.student, new_ticket)
        pytest.fail()


def test_create_ticket_unit_requires_course_entity():
    session = create_autospec(Session)
    session.scalars.side_effect = [
        SimpleNamespace(
            unique=lambda: SimpleNamespace(
                all=lambda: [SimpleNamespace(user_id=1, member_role=RosterRole.STUDENT)]
            )
        ),
        SimpleNamespace(all=lambda: []),
        SimpleNamespace(one_or_none=lambda: None),
    ]
    oh_ticket_svc = OfficeHourTicketService(session)

    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(
            SimpleNamespace(id=1),
            NewOfficeHoursTicket(
                description="Need help",
                type=TicketType.CONCEPTUAL_HELP,
                office_hours_id=1,
            ),
        )
        pytest.fail()


# Close Ticket Tests


def test_close_ticket(session: Session):
    """Ensures that instructors can close tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act
    called = oh_ticket_svc.close_ticket(
        scenario.instructor,
        scenario.called_ticket.id,
        make_close_payload(),
    )

    # Assert
    assert called.state == TicketState.CLOSED.to_string()


@pytest.mark.parametrize(
    "ticket_attr", ["queued_ticket", "closed_ticket", "cancelled_ticket"]
)
def test_close_ticket_not_called(session: Session, ticket_attr: str):
    """Ensures that only called tickets can be closed."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.close_ticket(
            scenario.instructor,
            getattr(scenario, ticket_attr).id,
            make_close_payload(),
        )


def test_close_ticket_not_found(session: Session):
    """Ensures that an error is thrown if attempting to close a ticket that does not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_svc.close_ticket(scenario.instructor, 404, make_close_payload())


def test_close_ticket_not_member(session: Session):
    """Ensures that non-members cannot close tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.close_ticket(
            scenario.ambassador,
            scenario.called_ticket.id,
            make_close_payload(),
        )


def test_close_ticket_not_staff(session: Session):
    """Ensures that non-staff members cannot close tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.close_ticket(
            scenario.student,
            scenario.called_ticket.id,
            make_close_payload(),
        )


def test_create_ticket(session: Session):
    """Ensurs that students can create new tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    user = arrange_additional_student(session, scenario.section.id, 5, "user")
    new_ticket = NewOfficeHoursTicket(
        description="Help me!",
        type=scenario.queued_ticket.type,
        office_hours_id=scenario.current_office_hours.id,
    )

    # Act
    created = oh_ticket_svc.create_ticket(user, new_ticket)

    # Assert
    assert created is not None
    assert isinstance(created, OfficeHourTicketOverview)
    assert created.state == TicketState.QUEUED.to_string()


def test_create_ticket_with_one_in_queue(session: Session):
    """Ensures that users can only create one ticket at a time."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    new_ticket = NewOfficeHoursTicket(
        description="Help me!",
        type=scenario.queued_ticket.type,
        office_hours_id=scenario.current_office_hours.id,
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(scenario.student, new_ticket)


def test_create_ticket_not_member(session: Session):
    """Ensures that non-members cannot create tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    new_ticket = NewOfficeHoursTicket(
        description="Help me!",
        type=scenario.queued_ticket.type,
        office_hours_id=scenario.current_office_hours.id,
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(scenario.ambassador, new_ticket)


def test_create_ticket_not_student(session: Session):
    """Ensures that only students can create tickets."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    new_ticket = NewOfficeHoursTicket(
        description="Help me!",
        type=scenario.queued_ticket.type,
        office_hours_id=scenario.current_office_hours.id,
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(scenario.instructor, new_ticket)


def test_create_ticket_with_cooldown(session: Session):
    """Ensures that users cannot create a ticket if they are on cooldown."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    new_ticket = arrange_policy_ticket_request(
        session,
        scenario,
        site_id=2,
        section_id=2,
        event_id=3,
        closed_ticket_id=5,
        minimum_ticket_cooldown=5,
        closed_offset_minutes=0,
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(scenario.student, new_ticket)


def test_create_ticket_with_maximum(session: Session):
    """Ensures that users cannot create a ticket if they have exceeded the maximum."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_ticket_svc = make_office_hours_ticket_service(session)
    new_ticket = arrange_policy_ticket_request(
        session,
        scenario,
        site_id=3,
        section_id=3,
        event_id=4,
        closed_ticket_id=6,
        max_tickets_per_day=1,
        closed_offset_minutes=10,
    )

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_ticket_svc.create_ticket(scenario.student, new_ticket)
