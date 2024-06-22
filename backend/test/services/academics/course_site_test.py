"""Tests for Course Site Service."""

import pytest

from ....models.pagination import PaginationParams, Paginated
from ....models.academics.my_courses import (
    TermOverview,
    CourseSiteOverview,
    SectionOverview,
    CourseMemberOverview,
    OfficeHoursOverview,
)
from ....services.academics.course_site import CourseSiteService
from ....services.exceptions import (
    ResourceNotFoundException,
)

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, course_site_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from .term_data import fake_data_fixture as insert_order_1
from .course_data import fake_data_fixture as insert_order_2
from .section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from . import section_data
from .. import user_data
from ..academics import term_data
from ..office_hours import office_hours_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_user_course_sites(course_site_svc: CourseSiteService):
    """Test case to retrieve a section member by ID."""
    term_overview = course_site_svc.get_user_course_sites(user_data.instructor)
    assert isinstance(term_overview, list)
    assert isinstance(term_overview[0], TermOverview)
    assert len(term_overview) == 1
    assert term_overview[0].id == term_data.current_term.id
    assert len(term_overview[0].sites) == 1


def test_get_course_site_roster(course_site_svc: CourseSiteService):
    """Test case to retrieve a section member by ID."""
    pagination_params = PaginationParams()
    roster = course_site_svc.get_course_site_roster(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 5


def test_get_current_office_hour_events(course_site_svc: CourseSiteService):
    """Test case to retrieve a section member by ID."""
    office_hours = course_site_svc.get_current_office_hour_events(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    assert len(office_hours) == 1
    assert isinstance(office_hours[0], OfficeHoursOverview)
    assert office_hours[0].id == office_hours_data.comp_110_current_office_hours.id


def test_get_future_office_hour_events(course_site_svc: CourseSiteService):
    """Test case to retrieve a section member by ID."""
    pagination_params = PaginationParams()
    office_hours = course_site_svc.get_future_office_hour_events(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(office_hours, Paginated)
    assert office_hours.length == 1
    assert isinstance(office_hours.items[0], OfficeHoursOverview)
    assert office_hours.items[0].id == office_hours_data.comp_110_future_office_hours.id


def test_get_past_office_hour_events(course_site_svc: CourseSiteService):
    """Test case to retrieve a section member by ID."""
    pagination_params = PaginationParams()
    office_hours = course_site_svc.get_past_office_hour_events(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(office_hours, Paginated)
    assert office_hours.length == 1
    assert isinstance(office_hours.items[0], OfficeHoursOverview)
    assert office_hours.items[0].id == office_hours_data.comp_110_past_office_hours.id
