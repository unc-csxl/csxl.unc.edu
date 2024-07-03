"""Tests for the HiringService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
    CoursePermissionException,
)

# Tested Dependencies
from ....models.application_review import HiringStatus, ApplicationReviewOverview
from ....services import HiringService

# Injected Service Fixtures
from ..fixtures import hiring_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..academics.term_data import fake_data_fixture as insert_order_1
from ..academics.course_data import fake_data_fixture as insert_order_2
from ..academics.section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5
from .hiring_data import fake_data_fixture as insert_order_6


# Test data
from .. import user_data
from ..academics import section_data
from ..office_hours import office_hours_data
from . import hiring_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Test Functions


def test_get_status(hiring_svc: HiringService):
    """Test that an instructor can get status on hiring."""
    hiring_status = hiring_svc.get_status(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    assert isinstance(hiring_status, HiringStatus)
    assert len(hiring_status.not_preferred) == 1
    assert (
        hiring_status.not_preferred[0].application_id == hiring_data.application_one.id
    )
    assert len(hiring_status.preferred) == 1
    assert hiring_status.preferred[0].application_id == hiring_data.application_two.id
    assert len(hiring_status.not_processed) == 2
    assert (
        hiring_status.not_processed[0].application_id
        == hiring_data.application_three.id
    )
    assert (
        hiring_status.not_processed[1].application_id == hiring_data.application_four.id
    )


def test_get_status_site_not_found(hiring_svc: HiringService):
    """Ensures that hiring is not possible if a course site does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.get_status(user_data.instructor, 404)
        pytest.fail()


def test_get_status_site_not_instructor(hiring_svc: HiringService):
    """Ensures that hiring information can only be viwed by instructors."""
    with pytest.raises(CoursePermissionException):
        hiring_svc.get_status(user_data.ambassador, office_hours_data.comp_110_site.id)
        pytest.fail()
    with pytest.raises(CoursePermissionException):
        hiring_svc.get_status(user_data.root, office_hours_data.comp_110_site.id)
        pytest.fail()
