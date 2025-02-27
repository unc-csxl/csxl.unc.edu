"""Tests for the OfficeHoursService."""

import pytest

from ....models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourGetHelpOverview,
    OfficeHourEventRoleOverview,
)
from ....models.office_hours.office_hours import NewOfficeHours, OfficeHours
from ....services.office_hours import OfficeHoursService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import oh_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..academics.term_data import fake_data_fixture as insert_order_1
from ..academics.course_data import fake_data_fixture as insert_order_2
from ..academics.section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import user_data
from ..academics import term_data, section_data
from ..office_hours import office_hours_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_office_hour_queue(oh_svc: OfficeHoursService):
    """Ensures instructors can access the office hour queue."""
    queue = oh_svc.get_office_hour_queue(
        user_data.instructor, office_hours_data.comp_110_current_office_hours.id
    )
    assert isinstance(queue, OfficeHourQueueOverview)
    assert queue.active is not None
    assert queue.active.id == office_hours_data.comp_110_called_ticket.id
    assert len(queue.queue) == 1
    assert queue.queue[0].id == office_hours_data.comp_110_queued_ticket.id


def test_get_office_hour_queue_not_member(oh_svc: OfficeHoursService):
    """Ensures that non-members of the course cannot access the office hour queue."""
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_queue(
            user_data.ambassador, office_hours_data.comp_110_current_office_hours.id
        )
        pytest.fail()


def test_get_office_hour_queue_not_staff(oh_svc: OfficeHoursService):
    """Ensures that students of the course cannot access the office hour queue."""
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_queue(
            user_data.student, office_hours_data.comp_110_current_office_hours.id
        )
        pytest.fail()


def test_get_help_overview(oh_svc: OfficeHoursService):
    """Ensures students can access the get help overview information."""
    overview = oh_svc.get_office_hour_get_help_overview(
        user_data.student, office_hours_data.comp_110_current_office_hours.id
    )
    assert isinstance(overview, OfficeHourGetHelpOverview)
    assert overview.ticket is not None
    assert overview.ticket.id == office_hours_data.comp_110_queued_ticket.id
    assert overview.queue_position == 1


def test_get_help_overview_not_member(oh_svc: OfficeHoursService):
    """Ensures non-members cannot access the get help overview information."""
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_get_help_overview(
            user_data.ambassador, office_hours_data.comp_110_current_office_hours.id
        )
        pytest.fail()


def test_get_help_overview_not_student(oh_svc: OfficeHoursService):
    """Ensures non-students cannot access the get help overview information."""
    with pytest.raises(CoursePermissionException):
        oh_svc.get_office_hour_get_help_overview(
            user_data.instructor, office_hours_data.comp_110_current_office_hours.id
        )
        pytest.fail()


def test_get_oh_event_role(oh_svc: OfficeHoursService):
    """Ensures that the instructor can access their office hour role"""
    role = oh_svc.get_oh_event_role(
        user_data.instructor, office_hours_data.comp_110_current_office_hours.id
    )
    assert isinstance(role, OfficeHourEventRoleOverview)
    assert role.role == section_data.comp110_instructor.member_role.value


def test_get_oh_event_role_student(oh_svc: OfficeHoursService):
    """Ensures that students can access their office hour role"""
    role = oh_svc.get_oh_event_role(
        user_data.student, office_hours_data.comp_110_current_office_hours.id
    )
    assert isinstance(role, OfficeHourEventRoleOverview)
    assert role.role == section_data.comp110_student_1.member_role.value


def test_get_oh_event_role_not_member(oh_svc: OfficeHoursService):
    """Ensures that non-members cannot access their office hour role"""
    with pytest.raises(CoursePermissionException):
        oh_svc.get_oh_event_role(
            user_data.ambassador, office_hours_data.comp_110_current_office_hours.id
        )
        pytest.fail()


def test_create_oh_event_instructor(oh_svc: OfficeHoursService):
    """Ensures that instructors can create office hour events."""
    office_hours_data.new_event.recurrence_pattern_id = None
    new_event = oh_svc.create(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.new_event,
    )
    assert new_event is not None
    assert isinstance(new_event, OfficeHours)
    assert new_event.id is not None


def test_create_oh_event_course_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be created on sites that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.create(
            user_data.instructor,
            404,
            office_hours_data.new_event_site_not_found,
        )
        pytest.fail()


def test_create_oh_event_not_authenticated(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be created on sites that do not exist."""
    with pytest.raises(CoursePermissionException):
        oh_svc.create(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.new_event_site_not_found,
        )
        pytest.fail()


def test_update_oh_event_instructor(oh_svc: OfficeHoursService):
    """Ensures that instructors can update office hour events."""
    new_event = oh_svc.update(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.updated_future_event,
    )
    assert new_event is not None
    assert isinstance(new_event, OfficeHours)
    assert new_event.id == office_hours_data.updated_future_event.id


def test_update_oh_event_course_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be updated on sites that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.update(
            user_data.instructor,
            404,
            office_hours_data.updated_future_event,
        )
        pytest.fail()


def test_update_oh_event_not_authenticated(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be updated on sites that do not exist."""
    with pytest.raises(CoursePermissionException):
        oh_svc.update(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.updated_future_event,
        )
        pytest.fail()


def test_update_oh_event_event_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be updated that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.update(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.nonexistent_event,
        )
        pytest.fail()


def test_delete_oh_event_instructor(oh_svc: OfficeHoursService):
    """Ensures that instructors can delete office hour events."""
    oh_svc.delete(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.comp_110_current_office_hours.id,
    )


def test_delete_oh_event_course_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be deleted on sites that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.delete(
            user_data.instructor,
            404,
            office_hours_data.comp_110_current_office_hours.id,
        )
        pytest.fail()


def test_delete_oh_event_not_authenticated(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be deleted on sites that do not exist."""
    with pytest.raises(CoursePermissionException):
        oh_svc.delete(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.comp_110_current_office_hours.id,
        )
        pytest.fail()


def test_delete_oh_event_event_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be deleted that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.delete(
            user_data.root,
            office_hours_data.comp_110_site.id,
            404,
        )
        pytest.fail()


def test_get_oh_event_instructor(oh_svc: OfficeHoursService):
    """Ensures that instructors can get office hour events."""
    oh_svc.get(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        office_hours_data.comp_110_current_office_hours.id,
    )


def test_get_oh_event_course_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be fetched on sites that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.get(
            user_data.instructor,
            404,
            office_hours_data.comp_110_current_office_hours.id,
        )
        pytest.fail()


def test_get_oh_event_not_authenticated(oh_svc: OfficeHoursService):
    """Ensures that office hour events cannot be fetched on sites that do not exist."""
    with pytest.raises(CoursePermissionException):
        oh_svc.get(
            user_data.root,
            office_hours_data.comp_110_site.id,
            office_hours_data.comp_110_current_office_hours.id,
        )
        pytest.fail()


def test_get_oh_event_event_not_found(oh_svc: OfficeHoursService):
    """Ensures that office hour events that do not exist cannot be fetched."""
    with pytest.raises(ResourceNotFoundException):
        oh_svc.get(
            user_data.root,
            office_hours_data.comp_110_site.id,
            404,
        )
        pytest.fail()
