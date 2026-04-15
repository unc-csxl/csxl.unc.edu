"""Tests for the OfficeHoursService."""

from datetime import datetime, timedelta
import pytest
from types import SimpleNamespace
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourGetHelpOverview,
    OfficeHourEventRoleOverview,
    OfficeHourTicketOverview,
)
from ....models.office_hours.office_hours import OfficeHours
from ....models.office_hours.ticket import TicketState
from ....models.roster_role import RosterRole
from ....services.office_hours import OfficeHoursService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException
from .scenario import arrange_office_hours_scenario, make_office_hours_service

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


pytestmark = pytest.mark.integration


def test_get_office_hour_queue(session: Session):
    """Ensures instructors can access the office hour queue."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    queue = oh_svc.get_office_hour_queue(
        scenario.instructor, scenario.current_office_hours.id
    )

    # Assert
    assert isinstance(queue, OfficeHourQueueOverview)
    assert queue.active is not None
    assert queue.active.id == scenario.called_ticket.id
    assert len(queue.queue) == 1
    assert queue.queue[0].id == scenario.queued_ticket.id


def test_get_office_hour_queue_not_member(session: Session):
    """Ensures that non-members of the course cannot access the office hour queue."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_queue(
            scenario.ambassador, scenario.current_office_hours.id
        )


def test_get_office_hour_queue_not_staff(session: Session):
    """Ensures that students of the course cannot access the office hour queue."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_queue(scenario.student, scenario.current_office_hours.id)


def test_get_help_overview(session: Session):
    """Ensures students can access the get help overview information."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    overview = oh_svc.get_office_hour_get_help_overview(
        scenario.student, scenario.current_office_hours.id
    )

    # Assert
    assert isinstance(overview, OfficeHourGetHelpOverview)
    assert overview.ticket is not None
    assert overview.ticket.id == scenario.queued_ticket.id
    assert overview.queue_position == 1


def test_get_help_overview_not_member(session: Session):
    """Ensures non-members cannot access the get help overview information."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_get_help_overview(
            scenario.ambassador, scenario.current_office_hours.id
        )


def test_get_help_overview_not_student(session: Session):
    """Ensures non-students cannot access the get help overview information."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_get_help_overview(
            scenario.instructor, scenario.current_office_hours.id
        )


def test_get_help_overview_not_found(session: Session):
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    with pytest.raises(ResourceNotFoundException):
        oh_svc.get_office_hour_get_help_overview(scenario.student, 404)
        pytest.fail()


def test_get_oh_event_role(session: Session):
    """Ensures that the instructor can access their office hour role"""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    role = oh_svc.get_oh_event_role(
        scenario.instructor, scenario.current_office_hours.id
    )

    # Assert
    assert isinstance(role, OfficeHourEventRoleOverview)
    assert role.role == RosterRole.INSTRUCTOR.value


def test_get_oh_event_role_student(session: Session):
    """Ensures that students can access their office hour role"""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    role = oh_svc.get_oh_event_role(scenario.student, scenario.current_office_hours.id)

    # Assert
    assert isinstance(role, OfficeHourEventRoleOverview)
    assert role.role == RosterRole.STUDENT.value


def test_get_oh_event_role_not_member(session: Session):
    """Ensures that non-members cannot access their office hour role"""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.get_oh_event_role(scenario.ambassador, scenario.current_office_hours.id)


def test_get_oh_event_role_not_found(session: Session):
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    with pytest.raises(CoursePermissionException):
        oh_svc.get_oh_event_role(scenario.instructor, 404)
        pytest.fail()


def test_get_entity_or_raise_not_found(session: Session):
    arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    with pytest.raises(ResourceNotFoundException):
        oh_svc._get_entity_or_raise(OfficeHoursEntity, 404)
        pytest.fail()


def test_check_site_student_permissions_not_found(session: Session):
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    with pytest.raises(ResourceNotFoundException):
        oh_svc._check_site_student_permissions(scenario.student, 404)
        pytest.fail()


def test_queue_overview_includes_queued_ticket_unit():
    ticket = SimpleNamespace(
        state=TicketState.QUEUED,
        to_overview_model=lambda: OfficeHourTicketOverview(
            id=1,
            created_at=datetime.now(),
            called_at=None,
            closed_at=None,
            state=TicketState.QUEUED.to_string(),
            type="Conceptual Help",
            description="Need help",
            creators=[],
            caller=None,
            has_concerns=False,
            caller_notes=None,
        ),
    )
    session = create_autospec(Session)
    session.scalars.return_value.all.return_value = [ticket]
    oh_svc = OfficeHoursService(session)

    overview = oh_svc._to_oh_queue_overview(
        SimpleNamespace(id=1),
        SimpleNamespace(
            id=1,
            type=SimpleNamespace(to_string=lambda: "Office Hours"),
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
        ),
    )

    assert len(overview.queue) == 1
    assert overview.queue[0].id == 1


def test_queue_overview_includes_other_called_ticket_unit():
    ticket = SimpleNamespace(
        state=TicketState.CALLED,
        caller=SimpleNamespace(user_id=2),
        to_overview_model=lambda: OfficeHourTicketOverview(
            id=2,
            created_at=datetime.now(),
            called_at=datetime.now(),
            closed_at=None,
            state=TicketState.CALLED.to_string(),
            type="Conceptual Help",
            description="Need help",
            creators=[],
            caller=None,
            has_concerns=False,
            caller_notes=None,
        ),
    )
    session = create_autospec(Session)
    session.scalars.return_value.all.return_value = [ticket]
    oh_svc = OfficeHoursService(session)

    overview = oh_svc._to_oh_queue_overview(
        SimpleNamespace(id=1),
        SimpleNamespace(
            id=1,
            type=SimpleNamespace(to_string=lambda: "Office Hours"),
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
        ),
    )

    assert len(overview.other_called) == 1
    assert overview.other_called[0].id == 2


def test_create_oh_event_instructor(session: Session):
    """Ensures that instructors can create office hour events."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    new_event = oh_svc.create(
        scenario.instructor,
        scenario.course_site.id,
        scenario.new_event,
    )

    # Assert
    assert new_event is not None
    assert isinstance(new_event, OfficeHours)
    assert new_event.id is not None


def test_create_oh_event_course_not_found(session: Session):
    """Ensures that office hour events cannot be created on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.create(
            scenario.instructor,
            404,
            scenario.new_event_site_not_found,
        )


def test_create_oh_event_not_authenticated(session: Session):
    """Ensures that office hour events cannot be created on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.create(
            scenario.root,
            scenario.course_site.id,
            scenario.new_event,
        )


def test_update_oh_event_instructor(session: Session):
    """Ensures that instructors can update office hour events."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    new_event = oh_svc.update(
        scenario.instructor,
        scenario.course_site.id,
        scenario.updated_future_event,
    )

    # Assert
    assert new_event is not None
    assert isinstance(new_event, OfficeHours)
    assert new_event.id == scenario.updated_future_event.id


def test_update_oh_event_course_not_found(session: Session):
    """Ensures that office hour events cannot be updated on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.update(
            scenario.instructor,
            404,
            scenario.updated_future_event,
        )


def test_update_oh_event_not_authenticated(session: Session):
    """Ensures that office hour events cannot be updated on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.update(
            scenario.root,
            scenario.course_site.id,
            scenario.updated_future_event,
        )


def test_update_oh_event_event_not_found(session: Session):
    """Ensures that office hour events cannot be updated that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.update(
            scenario.root,
            scenario.course_site.id,
            scenario.nonexistent_event,
        )


def test_delete_oh_event_instructor(session: Session):
    """Ensures that instructors can delete office hour events."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    oh_svc.delete(
        scenario.instructor,
        scenario.course_site.id,
        scenario.current_office_hours.id,
    )


def test_delete_oh_event_course_not_found(session: Session):
    """Ensures that office hour events cannot be deleted on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.delete(
            scenario.instructor,
            404,
            scenario.current_office_hours.id,
        )


def test_delete_oh_event_not_authenticated(session: Session):
    """Ensures that office hour events cannot be deleted on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.delete(
            scenario.root,
            scenario.course_site.id,
            scenario.current_office_hours.id,
        )


def test_delete_oh_event_event_not_found(session: Session):
    """Ensures that office hour events cannot be deleted that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.delete(
            scenario.root,
            scenario.course_site.id,
            404,
        )


def test_get_oh_event_instructor(session: Session):
    """Ensures that instructors can get office hour events."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act
    office_hours = oh_svc.get(
        scenario.instructor,
        scenario.course_site.id,
        scenario.current_office_hours.id,
    )

    # Assert
    assert office_hours.id == scenario.current_office_hours.id


def test_get_oh_event_course_not_found(session: Session):
    """Ensures that office hour events cannot be fetched on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.get(
            scenario.instructor,
            404,
            scenario.current_office_hours.id,
        )


def test_get_oh_event_not_authenticated(session: Session):
    """Ensures that office hour events cannot be fetched on sites that do not exist."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(CoursePermissionException):
        oh_svc.get(
            scenario.root,
            scenario.course_site.id,
            scenario.current_office_hours.id,
        )


def test_get_oh_event_event_not_found(session: Session):
    """Ensures that office hour events that do not exist cannot be fetched."""
    # Arrange
    scenario = arrange_office_hours_scenario(session)
    oh_svc = make_office_hours_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        oh_svc.get(
            scenario.root,
            scenario.course_site.id,
            404,
        )
