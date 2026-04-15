"""Tests for the HiringService class."""

# PyTest
import pytest
from types import SimpleNamespace
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
    CoursePermissionException,
)
from .....entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)

# Tested Dependencies
from .....models.academics.hiring.application_review import (
    ApplicationReview,
    HiringStatus,
    ApplicationReviewOverview,
    ApplicationReviewStatus,
)
from .....models.academics.hiring.hiring_level import HiringLevelClassification
from .....models.pagination import PaginationParams
from .....services.academics import HiringService
from .....services.academics.course_site import CourseSiteService
from .....services.permission import PermissionService

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
    assert (
        hiring_status.preferred[0].application_id == hiring_scenario.application_two.id
    )
    assert len(hiring_status.not_processed) == 2
    assert (
        hiring_status.not_processed[0].application_id
        == hiring_scenario.application_three.id
    )
    assert (
        hiring_status.not_processed[1].application_id
        == hiring_scenario.application_four.id
    )


def test_get_status_site_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that hiring is not possible if a course site does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.get_status(
            hiring_scenario.course_site.academics.auth.instructor, 404
        )
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
    assert (
        new_status.not_processed[0].application_id
        == hiring_scenario.application_four.id
    )
    assert (
        new_status.not_processed[1].application_id
        == hiring_scenario.application_three.id
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


def test_calculate_coverage_counts_assignment_types(hiring_svc: HiringService):
    coverage = hiring_svc._calculate_coverage(
        120,
        [
            SimpleNamespace(
                hiring_level=SimpleNamespace(
                    classification=HiringLevelClassification.PHD, load=1.0
                )
            ),
            SimpleNamespace(
                hiring_level=SimpleNamespace(
                    classification=HiringLevelClassification.UG, load=1.0
                )
            ),
            SimpleNamespace(
                hiring_level=SimpleNamespace(
                    classification=HiringLevelClassification.IOR, load=1.0
                )
            ),
        ],
    )

    assert coverage == pytest.approx(0.75)


def test_get_hiring_admin_course_overview(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    overview = hiring_svc.get_hiring_admin_course_overview(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.comp_110_site.id,
    )

    assert len(overview.reviews) == 1
    assert overview.reviews[0].application_id == hiring_scenario.application_two.id
    assert len(overview.assignments) == 1
    assert overview.assignments[0].id == hiring_scenario.hiring_assignment.id
    assert len(overview.instructor_preferences) == 1
    assert (
        overview.instructor_preferences[0].id == hiring_scenario.application_two.user_id
    )


def test_get_hiring_admin_course_overview_not_found(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.get_hiring_admin_course_overview(
            hiring_scenario.course_site.academics.auth.root,
            404,
        )
        pytest.fail()


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


def test_get_hiring_levels(hiring_svc: HiringService, hiring_scenario: HiringScenario):
    """Ensures that the admin can see all hiring levels."""
    levels = hiring_svc.get_hiring_levels(
        hiring_scenario.course_site.academics.auth.root
    )
    assert levels is not None
    assert len(levels) == 1


def test_get_hiring_level_checks_permission(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    """Ensures that nobody else is able see hiring levels."""
    with pytest.raises(UserPermissionException):
        hiring_svc.get_hiring_levels(
            hiring_scenario.course_site.academics.auth.ambassador
        )
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


def test_get_phd_applicants(hiring_svc: HiringService, hiring_scenario: HiringScenario):
    user = hiring_scenario.course_site.academics.auth.root
    term = hiring_scenario.course_site.academics.current_term
    applicants = hiring_svc.get_phd_applicants(user, term.id)
    assert len(applicants) > 0
    for applicant in applicants:
        assert applicant.program_pursued in {"PhD", "PhD (ABD)"}


def test_get_phd_applicants_includes_instructor_preferences(
    session, hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    session.add(
        ApplicationReviewEntity.from_model(
            ApplicationReview(
                application_id=hiring_scenario.application_five.id,
                course_site_id=hiring_scenario.course_site.comp_301_site.id,
                status=ApplicationReviewStatus.PREFERRED,
                preference=0,
                notes="",
            )
        )
    )
    session.commit()

    applicants = hiring_svc.get_phd_applicants(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.academics.current_term.id,
    )

    assert len(applicants) == 1
    assert applicants[0].instructor_preferences == ["(0) comp301.001"]


def test_get_hiring_summary(hiring_svc: HiringService, hiring_scenario: HiringScenario):
    summary = hiring_svc.get_hiring_summary_overview(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.academics.current_term.id,
        PaginationParams(page=0, page_size=10, order_by="id", filter="Stewie"),
    )

    assert summary.length == 1
    assert len(summary.items) == 1
    assert summary.items[0].user.id == hiring_scenario.application_one.user_id


def test_get_hiring_summary_rejects_invalid_pagination(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    with pytest.raises(ValueError):
        hiring_svc.get_hiring_summary_overview(
            hiring_scenario.course_site.academics.auth.root,
            hiring_scenario.course_site.academics.current_term.id,
            PaginationParams(page=-1, page_size=10, order_by="id", filter=""),
        )
        pytest.fail()


def test_get_hiring_summary_for_csv(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    rows = hiring_svc.get_hiring_summary_for_csv(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.academics.current_term.id,
    )

    assert len(rows) == 1
    assert rows[0].first_name == "Stewie"
    assert rows[0].last_name == "Student"


def test_get_course_site_hiring_status_csv(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    rows = hiring_svc.get_course_site_hiring_status_csv(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )

    assert len(rows) == 3
    assert rows[0].applicant_name == "Stewie Student"


def test_get_hiring_assignments_for_course_site(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    hiring_svc.update_hiring_assignment(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.updated_hiring_assignment,
    )

    assignments = hiring_svc.get_hiring_assignments_for_course_site(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
        PaginationParams(page=0, page_size=10, order_by="id", filter="UTA Full Time"),
    )

    assert assignments.length == 1
    assert len(assignments.items) == 1
    assert assignments.items[0].id == hiring_scenario.hiring_assignment.id


def test_get_assignment_summary_for_instructors_csv(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    hiring_svc.create_hiring_assignment(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.new_hiring_assignment,
    )

    rows = hiring_svc.get_assignment_summary_for_instructors_csv(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )

    assert len(rows) == 2


def test_conflict_check(hiring_svc: HiringService, hiring_scenario: HiringScenario):
    status = hiring_svc.get_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
    )
    status.not_preferred[0].status = ApplicationReviewStatus.PREFERRED
    status.not_preferred[0].preference = 1

    hiring_svc.update_status(
        hiring_scenario.course_site.academics.auth.instructor,
        hiring_scenario.course_site.comp_110_site.id,
        status,
    )

    conflict_check = hiring_svc.conflict_check(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.application_one.id,
    )

    assert conflict_check.application_id == hiring_scenario.application_one.id
    assert conflict_check.assignments == []
    assert len(conflict_check.priorities) == 1
    assert conflict_check.priorities[0].student_priority == 1
    assert conflict_check.priorities[0].instructor_priority == 1


def test_iter_applicants_for_term_csv(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    hiring_svc.update_hiring_assignment(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.updated_hiring_assignment,
    )
    rows = list(
        hiring_svc.iter_applicants_for_term_csv(
            hiring_scenario.course_site.academics.auth.root,
            hiring_scenario.course_site.academics.current_term.id,
        )
    )

    assert len(rows) == 5
    student_row = next(row for row in rows if row["first_name"] == "Stewie")
    assert "COMP110-001" in student_row["assignments"]
    assert "comp301.001" in student_row["preferred_sections"]


def test_get_course_site_hiring_status_csv_checks_permission_for_non_instructor(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    hiring_svc._permission = create_autospec(PermissionService)

    hiring_svc.get_course_site_hiring_status_csv(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.comp_110_site.id,
    )

    hiring_svc._permission.enforce.assert_called_with(
        hiring_scenario.course_site.academics.auth.root,
        "hiring.get_status",
        f"course_site/{hiring_scenario.course_site.comp_110_site.id}",
    )


def test_get_hiring_assignments_for_course_site_checks_permission_for_non_instructor(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    hiring_svc._permission = create_autospec(PermissionService)

    hiring_svc.get_hiring_assignments_for_course_site(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.comp_110_site.id,
        PaginationParams(page=0, page_size=10, order_by="id", filter=""),
    )

    hiring_svc._permission.enforce.assert_called_with(
        hiring_scenario.course_site.academics.auth.root,
        "hiring.get_assignments",
        f"course_site/{hiring_scenario.course_site.comp_110_site.id}",
    )


def test_get_assignment_summary_for_instructors_csv_checks_permission_for_non_instructor(
    hiring_svc: HiringService, hiring_scenario: HiringScenario
):
    hiring_svc._permission = create_autospec(PermissionService)

    hiring_svc.get_assignment_summary_for_instructors_csv(
        hiring_scenario.course_site.academics.auth.root,
        hiring_scenario.course_site.comp_110_site.id,
    )

    hiring_svc._permission.enforce.assert_called_with(
        hiring_scenario.course_site.academics.auth.root,
        "hiring.get_assignments",
        f"course_site/{hiring_scenario.course_site.comp_110_site.id}",
    )


def test_iter_applicants_for_term_csv_skips_missing_application():
    session = create_autospec(Session)
    session.scalars.return_value.all.return_value = [1]
    session.get.return_value = None
    permission = create_autospec(PermissionService)

    rows = list(
        HiringService(session, permission).iter_applicants_for_term_csv(
            object(), "Curr"
        )
    )

    assert rows == []


def test_iter_applicants_for_term_csv_skips_assignments_without_sections():
    session = create_autospec(Session)
    permission = create_autospec(PermissionService)
    user = SimpleNamespace(
        id=1,
        first_name="Test",
        last_name="User",
        pid=1,
        email="test@unc.edu",
        pronouns="they/them",
    )
    application = SimpleNamespace(
        user=user,
        term_id="Curr",
        type="new_uta",
        program_pursued=None,
        comp_227=None,
        intro_video_url=None,
        prior_experience=None,
        advisor=None,
    )
    assignment = SimpleNamespace(
        course_site=SimpleNamespace(sections=[]),
        hiring_level=SimpleNamespace(title="UTA", load=1.0),
    )
    session.scalars.side_effect = [
        SimpleNamespace(all=lambda: [1]),
        SimpleNamespace(unique=lambda: SimpleNamespace(all=lambda: [assignment])),
    ]
    session.get.return_value = application
    session.execute.side_effect = [
        SimpleNamespace(all=lambda: []),
        SimpleNamespace(
            unique=lambda: SimpleNamespace(
                scalars=lambda: SimpleNamespace(
                    all=lambda: [SimpleNamespace(course_site=None, preference=0)]
                )
            )
        ),
    ]

    rows = list(
        HiringService(session, permission).iter_applicants_for_term_csv(
            object(), "Curr"
        )
    )

    assert len(rows) == 1
    assert rows[0]["assignments"] == ""
    assert rows[0]["instructor_selections"] == ""
