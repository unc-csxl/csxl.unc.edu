"""Tests for Section Member Service."""

import pytest

from ....models.office_hours.course_site_details import CourseSiteDetails
from ....models.academics.section_member import SectionMember
from ....models.roster_role import RosterRole
from ....models.pagination import PaginationParams

from ....services.academics.section_member import SectionMemberService
from ....services.academics.my_courses import MyCoursesService
from ....services.exceptions import (
    ResourceNotFoundException,
)

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_member_svc, my_courses_svc

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
from ..office_hours import office_hours_data

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_section_member_by_id(section_member_svc: SectionMemberService):
    """Test case to retrieve a section member by ID."""
    section_member = section_member_svc.get_section_member_by_id(id=1)

    assert isinstance(section_member, SectionMember)
    assert section_member.id == section_data.comp110_instructor.id


def test_get_section_member_by_id_exception_if_invalid_id(
    section_member_svc: SectionMemberService,
):
    """Test case to check if retrieving a section member by an invalid ID raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        section_member_svc.get_section_member_by_id(id=99)
        pytest.fail()
