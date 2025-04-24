"""Tests for the OfficeHoursTicketService."""

import pytest

from ....models.academics.my_courses import OfficeHourTicketOverview

from ....models.office_hours.ticket import TicketState

from ....services.office_hours import OfficeHourTicketTagService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import oh_ticket_tag_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..academics.term_data import fake_data_fixture as insert_order_1
from ..academics.course_data import fake_data_fixture as insert_order_2
from ..academics.section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import user_data
from ..office_hours import office_hours_data

__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


# Call Ticket Tag Tests
def test_get_tag_by_id(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test retrieving a ticket tag by ID.
    """
    # Get the ticket tag by ID
    tag = oh_ticket_tag_svc.get_tag_by_id(
        user_data.instructor, office_hours_data.comp_110_site.id, office_hours_data.ticket_tag_1.id
    )

    # Check the tag ID
    assert tag.id == office_hours_data.ticket_tag_1.id
    # Check the tag name
    assert tag.name == office_hours_data.ticket_tag_1.name
    
def test_get_course_site_tags(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test retrieving tags for a course site.
    """
    # Get the course site tags
    tags = oh_ticket_tag_svc.get_course_site_tags(
        user_data.instructor, office_hours_data.comp_110_site.id
    )

    # Check the number of tags
    assert len(tags) == 2

    # Check the tag names
    assert tags[0].name == office_hours_data.ticket_tag_1.name
    assert tags[1].name == office_hours_data.ticket_tag_2.name

def test_get_course_site_tags_unauthenticated(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test retrieving tags for a course site with an unauthenticated user.
    """
    # Attempt to get the course site tags
    with pytest.raises(CoursePermissionException):
        oh_ticket_tag_svc.get_course_site_tags(
            user_data.student, office_hours_data.comp_110_site.id
        )

def test_create_ticket_tag(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test creating a new ticket tag.
    """
    # Create a new ticket tag
    new_tag = office_hours_data.new_ticket_tag
    created_tag = oh_ticket_tag_svc.create(
        user_data.instructor, office_hours_data.comp_110_site.id, new_tag
    )


    # Check the created tag ID
    assert created_tag.id == 3
    # Check the created tag
    assert created_tag.name == new_tag.name

def test_create_ticket_tag_unauthenticated(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test creating a new ticket tag with an unauthenticated user.
    """
    # Create a new ticket tag
    new_tag = office_hours_data.sample_ticket_tag

    # Attempt to create the ticket tag
    with pytest.raises(CoursePermissionException):
        oh_ticket_tag_svc.create(
            user_data.student, office_hours_data.comp_110_site.id, new_tag
        )

def test_update_ticket_tag(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test updating an existing ticket tag.
    """
    updated_tag = oh_ticket_tag_svc.update(
        user_data.instructor, office_hours_data.comp_110_site.id, office_hours_data.updated_ticket_tag_1
    )

    # Check the updated tag ID
    assert updated_tag.id == office_hours_data.updated_ticket_tag_1.id
    # Check the updated tag name
    assert updated_tag.name == office_hours_data.updated_ticket_tag_1.name

def test_update_ticket_tag_unauthenticated(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test updating an existing ticket tag with an unauthenticated user.
    """
    # Attempt to update the ticket tag
    with pytest.raises(CoursePermissionException):
        oh_ticket_tag_svc.update(
            user_data.student, office_hours_data.comp_110_site.id, office_hours_data.updated_ticket_tag_1
        )

def test_delete_ticket_tag(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test deleting an existing ticket tag.
    """
    # Delete the ticket tag
    oh_ticket_tag_svc.delete(
        user_data.instructor, office_hours_data.comp_110_site.id, office_hours_data.ticket_tag_1.id
    )

    # Attempt to retrieve the deleted tag
    with pytest.raises(ResourceNotFoundException):
        oh_ticket_tag_svc.get_tag_by_id(
            user_data.instructor, office_hours_data.comp_110_site.id, office_hours_data.ticket_tag_1.id
        )

def test_delete_ticket_tag_unauthenticated(oh_ticket_tag_svc: OfficeHourTicketTagService):
    """
    Test deleting an existing ticket tag with an unauthenticated user.
    """
    # Attempt to delete the ticket tag
    with pytest.raises(CoursePermissionException):
        oh_ticket_tag_svc.delete(
            user_data.student, office_hours_data.comp_110_site.id, office_hours_data.ticket_tag_1.id
        )