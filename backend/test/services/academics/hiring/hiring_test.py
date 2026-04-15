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
from .....services.academics.course_site import CourseSiteService

# Injected Service Fixtures
from .fixtures import hiring_svc
from ..fixtures import course_site_svc
from .scenario import HiringScenario, arrange_hiring_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def hiring_scenario(session) -> HiringScenario:
    return arrange_hiring_scenario(session)


def test_get_status(hiring_svc: HiringService, hiring_scenario: HiringScenario):
    """Test that an instructor can get status on hiring."""
    hiring_status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )
    assert isinstance(hiring_status, HiringStatus)
    assert len(hiring_status.not_preferred) == 1
    assert (
        hiring_status.not_preferred[0].application_id
        == hiring_scenario.application_one.id
    )
    assert len(hiring_status.preferred) == 1
    assert hiring_status.preferred[0].application_id == hiring_scenario.application_two.id
    assert len(hiring_status.not_processed) == 2
    assert (
        hiring_status.not_processed[0].application_id
        == hiring_scenario.application_three.id
    )
    assert (
        hiring_status.not_processed[1].application_id == hiring_scenario.application_four.id
    )


def test_get_status_site_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring is not possible if a course site does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.get_status(hiring_scenario.course_site.academics.auth.instructor, 404)
        pytest.fail()


def test_get_status_site_not_instructor(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring information can only be viwed by instructors."""
    with pytest.raises(UserPermissionException):
        hiring_svc.get_status(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.course_site.comp_110_site.id,
        )
        pytest.fail()


def test_get_status_with_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring information can only be viwed by instructors."""
    status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.comp_110_site.id,
    )
    assert status is not None


def test_update_status(hiring_svc: HiringService, hiring_scenario: HiringScenario):
    """Test that an instructor can update the hiring status."""
    status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )

    status.not_preferred[0].status = ApplicationReviewStatus.PREFERRED
    status.not_preferred[0].preference = 1
    status.preferred[0].notes = "Updated notes!"
    status.not_processed[0].preference = 1
    status.not_processed[1].preference = 0

    new_status = hiring_svc.update_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
        status,
    )

    assert len(new_status.not_preferred) == 0
    assert len(new_status.preferred) == 2
    assert new_status.preferred[0].application_id == hiring_scenario.application_two.id
    assert new_status.preferred[0].notes == "Updated notes!"
    assert new_status.preferred[1].application_id == hiring_scenario.application_one.id
    assert new_status.not_processed[0].application_id == hiring_scenario.application_four.id
    assert (
        new_status.not_processed[1].application_id == hiring_scenario.application_three.id
    )


def test_update_status_site_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that updating hiring is not possible if a course site does not exist."""
    status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.update_status(
            hiring_scenario.course_site.academics.auth.instructor, 404, status
        )
        pytest.fail()


def test_update_status_site_not_instructor(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that updating hiring information can only be viwed by instructors."""
    status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )
    with pytest.raises(UserPermissionException):
        hiring_svc.update_status(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.course_site.comp_110_site.id,
            status,
        )
        pytest.fail()


def test_update_status_administrator(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )
    hiring_svc.update_status(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.comp_110_site.id,
        status,
    )
    assert True


def test_get_hiring_admin_overview(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin is able to get the hiring admin data."""
    hiring_admin_overview = hiring_svc.get_hiring_admin_overview(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.academics.current_term.id,
    )
    assert hiring_admin_overview is not None
    assert len(hiring_admin_overview.sites) == 2


def test_get_hiring_admin_overview_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able to check the hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.get_hiring_admin_overview(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.course_site.academics.current_term.id,
        )
        pytest.fail()


def test_create_hiring_assignment(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin can create hiring assignments."""
    assignment = hiring_svc.create_hiring_assignment(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.new_hiring_assignment,
    )
    assert assignment is not None


def test_create_hiring_assignment_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.create_hiring_assignment(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.new_hiring_assignment,
        )
        pytest.fail()


def test_update_hiring_assignment(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin can update hiring assignments."""
    assignment = hiring_svc.update_hiring_assignment(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.updated_hiring_assignment,
    )
    assert assignment is not None
    assert assignment.id == hiring_scenario.updated_hiring_assignment.id


def test_update_hiring_assignment_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.update_hiring_assignment(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.updated_hiring_assignment,
        )
        pytest.fail()


def test_update_hiring_assignment_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring data cannot be updated if it does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.update_hiring_assignment(
            hiring_scenario.course_site.academics.auth.root,
            hiring_scenario.new_hiring_assignment,
        )
        pytest.fail()


def test_delete_hiring_assignment(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin can delete hiring assignments."""
    hiring_svc.delete_hiring_assignment(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.hiring_assignment.id,
    )


def test_delete_hiring_assignment_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.delete_hiring_assignment(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.hiring_assignment.id,
        )
        pytest.fail()


def test_delete_hiring_assignment_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring data cannot be deleted if it does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.delete_hiring_assignment(
            hiring_scenario.course_site.academics.auth.root,
            hiring_scenario.new_hiring_assignment.id,
        )
        pytest.fail()


def test_get_hiring_levels(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin can see all hiring levels."""
    levels = hiring_svc.get_hiring_levels(hiring_scenario.course_site.academics.auth.root)
    assert levels is not None
    assert len(levels) == 1


def test_get_hiring_level_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able see hiring levels."""
    with pytest.raises(UserPermissionException):
        hiring_svc.get_hiring_levels(hiring_scenario.course_site.academics.auth.ambassador)
        pytest.fail()


def test_create_hiring_level(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin can create hiring levels."""
    level = hiring_svc.create_hiring_level(
        hiring_scenario.course_site.academics.auth.root, hiring_scenario.new_level
    )
    assert level is not None


def test_create_hiring_level_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.create_hiring_level(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.new_level,
        )
        pytest.fail()


def test_update_hiring_level(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that the admin can update hiring levels."""
    level = hiring_svc.update_hiring_level(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.updated_uta_level,
    )
    assert level is not None
    assert level.id == hiring_scenario.updated_uta_level.id


def test_update_hiring_level_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.update_hiring_level(
            hiring_scenario.course_site.academics.auth.ambassador,
            hiring_scenario.updated_uta_level,
        )
        pytest.fail()


def test_update_hiring_level_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring data cannot be deleted if it does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.update_hiring_level(
            hiring_scenario.course_site.academics.auth.root,
            hiring_scenario.new_level,
        )
        pytest.fail()


def test_create_missing_course_sites_for_term(
    hiring_svc: HiringService,
    course_site_svc: CourseSiteService,
    hiring_scenario: HiringScenario,
):
    user = hiring_scenario.course_site.academics.auth.root
    term = hiring_scenario.course_site.academics.current_term
    overview_pre = hiring_svc.get_hiring_admin_overview(user, term.id)
    hiring_svc.create_missing_course_sites_for_term(user, term.id)
    overview_post = hiring_svc.get_hiring_admin_overview(user, term.id)
    assert len(overview_post.sites) > len(overview_pre.sites)


def test_get_phd_applicants(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    user = hiring_scenario.course_site.academics.auth.root
    term = hiring_scenario.course_site.academics.current_term
    applicants = hiring_svc.get_phd_applicants(user, term.id)
    assert len(applicants) > 0
    for applicant in applicants:
        assert applicant.program_pursued in {"PhD", "PhD (ABD)"}
