"""Tests for `update()` in Office Hours Event Service."""

from datetime import date, datetime, timedelta
import pytest

from backend.models.office_hours.office_hours import (
    OfficeHoursEvent,
    OfficeHoursEventPartial,
)
from backend.models.office_hours.event_type import OfficeHoursEventType
from backend.models.room import Room
from backend.services.exceptions import ResourceNotFoundException


from .....services.office_hours.office_hours import OfficeHoursEventService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_event_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ...core_data import setup_insert_data_fixture as insert_order_0
from ...room_data import fake_data_fixture as insert_order_1
from ...academics.term_data import fake_data_fixture as insert_order_2
from ...academics.course_data import fake_data_fixture as insert_order_3
from ...academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import office_hours_data
from ...academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_uta_0,
    user__comp110_non_member,
)


__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_update_event_description_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to update the description of an office hours event by a teaching assistant."""
    updated_description = "Updated Event Description"
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, description=updated_description
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.description != updated_description

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.description == updated_description

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.description == updated_description


def test_update_event_location_description_by_uta(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to update the location description of an office hours event by a teaching assistant."""
    updated_location_description = "Meet at Sitterson Lobby"
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, location_description=updated_location_description
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.location_description != updated_location_description

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.location_description == updated_location_description

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.location_description == updated_location_description


def test_update_event_room_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to update the room of an office hours event by a teaching assistant."""
    updated_room = Room(id="SN135")
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, room=updated_room)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.room.id != updated_room.id

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.room.id == updated_room.id

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.room.id == updated_room.id


def test_update_event_type_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to update the type of an office hours event by a teaching assistant."""
    updated_event_type = OfficeHoursEventType.TUTORING
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, type=updated_event_type)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.type != updated_event_type

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.type == updated_event_type

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.type == updated_event_type


def test_update_event_date_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to update the date of an office hours event by a teaching assistant."""
    updated_date = date.today() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, event_date=updated_date)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.event_date != updated_date

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.event_date == updated_date

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.event_date == updated_date


def test_update_start_time_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to update the start time of an office hours event by a teaching assistant."""
    updated_start_time = datetime.now() + timedelta(hours=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, start_time=updated_start_time
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.start_time != updated_start_time

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.start_time == updated_start_time

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.start_time == updated_start_time


def test_update_end_time_by_uta(oh_event_svc: OfficeHoursEventService):
    """Test case to update the end time of an office hours event by a teaching assistant."""
    updated_end_time = datetime.now() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, end_time=updated_end_time)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.end_time != updated_end_time

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.end_time == updated_end_time

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.end_time == updated_end_time


def test_update_multiple_fields_start_end_time_by_uta(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to update multiple fields (start time and end time) of an office hours event by a teaching assistant."""
    updated_start_time = datetime.now() + timedelta(hours=1)
    updated_end_time = datetime.now() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, start_time=updated_start_time, end_time=updated_end_time
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event is not None
    assert oh_event.end_time != updated_end_time
    assert oh_event.start_time != updated_start_time

    # Update
    updated_event = oh_event_svc.update(user__comp110_uta_0, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.end_time == updated_end_time
    assert updated_event.start_time == updated_start_time

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(user__comp110_uta_0, target_oh_event_id)
    assert oh_event.end_time == updated_end_time
    assert oh_event.start_time == updated_start_time


def test_update_event_description_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to update the description of an office hours event by an instructor."""
    updated_description = "Updated Event Description"
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, description=updated_description
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.description != updated_description

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.description == updated_description

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.description == updated_description


def test_update_event_location_description_by_instructor(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to update the location description of an office hours event by an instructor."""
    updated_location_description = "Meet at Sitterson Lobby"
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, location_description=updated_location_description
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.location_description != updated_location_description

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.location_description == updated_location_description

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.location_description == updated_location_description


def test_update_event_room_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to update the room of an office hours event by an instructor."""
    updated_room = Room(id="SN135")
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, room=updated_room)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.room.id != updated_room.id

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.room.id == updated_room.id

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.room.id == updated_room.id


def test_update_event_type_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to update the type of an office hours event by an instructor."""
    updated_event_type = OfficeHoursEventType.TUTORING
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, type=updated_event_type)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.type != updated_event_type

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.type == updated_event_type

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.type == updated_event_type


def test_update_event_date_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to update the date of an office hours event by an instructor."""
    updated_date = date.today() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, event_date=updated_date)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.event_date != updated_date

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.event_date == updated_date

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.event_date == updated_date


def test_update_start_time_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to update the start time of an office hours event by an instructor."""
    updated_start_time = datetime.now() + timedelta(hours=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, start_time=updated_start_time
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.start_time != updated_start_time

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.start_time == updated_start_time

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.start_time == updated_start_time


def test_update_end_time_by_instructor(oh_event_svc: OfficeHoursEventService):
    """Test case to update the end time of an office hours event by an instructor."""
    updated_end_time = datetime.now() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, end_time=updated_end_time)

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.end_time != updated_end_time

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.end_time == updated_end_time

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.end_time == updated_end_time


def test_update_multiple_fields_start_end_time_by_instructor(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to update multiple fields (start time and end time) of an office hours event by an instructor."""
    updated_start_time = datetime.now() + timedelta(hours=1)
    updated_end_time = datetime.now() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, start_time=updated_start_time, end_time=updated_end_time
    )

    # Check Original State
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event is not None
    assert oh_event.end_time != updated_end_time
    assert oh_event.start_time != updated_start_time

    # Update
    updated_event = oh_event_svc.update(user__comp110_instructor, delta)
    assert isinstance(updated_event, OfficeHoursEvent)
    assert updated_event.end_time == updated_end_time
    assert updated_event.start_time == updated_start_time

    # Check Updated
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_instructor, target_oh_event_id
    )
    assert oh_event.end_time == updated_end_time
    assert oh_event.start_time == updated_start_time


def test_update_exception_if_student(oh_event_svc: OfficeHoursEventService):
    """Test case to check if updating an office hours event throws an exception when attempted by a student."""
    updated_end_time = datetime.now() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, end_time=updated_end_time)

    with pytest.raises(PermissionError):
        oh_event_svc.update(user__comp110_student_0, delta)
        pytest.fail()


def test_update_exception_if_non_member(oh_event_svc: OfficeHoursEventService):
    """Test case to check if updating an office hours event throws an exception when attempted by a non-member."""
    updated_end_time = datetime.now() + timedelta(days=1)
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(id=target_oh_event_id, end_time=updated_end_time)

    with pytest.raises(PermissionError):
        oh_event_svc.update(user__comp110_non_member, delta)
        pytest.fail()


def test_update_exception_invalid_event_id(oh_event_svc: OfficeHoursEventService):
    """Test case to check if updating an office hours event throws an exception for an invalid event ID."""
    updated_end_time = datetime.now() + timedelta(days=1)
    inavlid_oh_event_id = 99

    delta = OfficeHoursEventPartial(id=inavlid_oh_event_id, end_time=updated_end_time)

    with pytest.raises(ResourceNotFoundException):
        oh_event_svc.update(user__comp110_uta_0, delta)
        pytest.fail()


def test_update_event_oh_section_raises_exception(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to check if updating an office hours event raises an exception for attempt to update oh section."""
    updated_oh_section = office_hours_data.comp_523_oh_section
    target_oh_event_id = office_hours_data.comp_110_upcoming_oh_event.id

    delta = OfficeHoursEventPartial(
        id=target_oh_event_id, oh_section=updated_oh_section
    )

    with pytest.raises(Exception):
        oh_event_svc.update(user__comp110_uta_0, delta)
        pytest.fail()
