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
from .....models.academics.hiring.application_review import (
    HiringStatus,
    ApplicationReviewOverview,
    ApplicationReviewStatus,
)
from .....services.academics import HiringService
from .....services.application import ApplicationService

# Injected Service Fixtures
from .fixtures import hiring_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ...core_data import setup_insert_data_fixture as insert_order_0
from ...academics.term_data import fake_data_fixture as insert_order_1
from ...academics.course_data import fake_data_fixture as insert_order_2
from ...academics.section_data import fake_data_fixture as insert_order_3
from ...room_data import fake_data_fixture as insert_order_4
from ...office_hours.office_hours_data import fake_data_fixture as insert_order_5
from .hiring_data import fake_data_fixture as insert_order_6


# Test data
from ... import user_data
from ...academics import section_data, term_data
from ...office_hours import office_hours_data
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


def test_update_status(hiring_svc: HiringService):
    """Test that an instructor can update the hiring status."""
    status = hiring_svc.get_status(
        user_data.instructor, office_hours_data.comp_110_site.id
    )

    status.not_preferred[0].status = ApplicationReviewStatus.PREFERRED
    status.not_preferred[0].preference = 1
    status.preferred[0].notes = "Updated notes!"
    status.not_processed[0].preference = 1
    status.not_processed[1].preference = 0

    new_status = hiring_svc.update_status(
        user_data.instructor, office_hours_data.comp_110_site.id, status
    )

    assert len(new_status.not_preferred) == 0
    assert len(new_status.preferred) == 2
    assert new_status.preferred[0].application_id == hiring_data.application_two.id
    assert new_status.preferred[0].notes == "Updated notes!"
    assert new_status.preferred[1].application_id == hiring_data.application_one.id
    assert new_status.not_processed[0].application_id == hiring_data.application_four.id
    assert (
        new_status.not_processed[1].application_id == hiring_data.application_three.id
    )


def test_update_status_site_not_found(hiring_svc: HiringService):
    """Ensures that updating hiring is not possible if a course site does not exist."""
    status = hiring_svc.get_status(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.update_status(user_data.instructor, 404, status)
        pytest.fail()


def test_update_status_site_not_instructor(hiring_svc: HiringService):
    """Ensures that updating hiring information can only be viwed by instructors."""
    status = hiring_svc.get_status(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    with pytest.raises(CoursePermissionException):
        hiring_svc.update_status(
            user_data.ambassador, office_hours_data.comp_110_site.id, status
        )
        pytest.fail()
    with pytest.raises(CoursePermissionException):
        hiring_svc.update_status(
            user_data.root, office_hours_data.comp_110_site.id, status
        )
        pytest.fail()


def test_get_hiring_admin_overview(hiring_svc: HiringService):
    """Ensures that the admin is able to get the hiring admin data."""
    hiring_admin_overview = hiring_svc.get_hiring_admin_overview(
        user_data.root, term_data.current_term.id
    )
    assert hiring_admin_overview is not None
    assert len(hiring_admin_overview.sites) == 2


def test_get_hiring_admin_overview_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able to check the hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.get_hiring_admin_overview(
            user_data.ambassador, term_data.current_term.id
        )
        pytest.fail()
