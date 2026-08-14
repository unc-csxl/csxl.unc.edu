"""Tests for the HiringService class."""

# PyTest
import pytest
from unittest.mock import create_autospec
from sqlalchemy import select
from sqlalchemy.orm import Session

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
from .....models.comp_227 import Comp227
from .....models.roster_role import RosterRole
from .....entities.application_entity import ApplicationEntity
from .....entities.section_application_table import section_application_table
from .....entities.academics.section_member_entity import SectionMemberEntity
from .....entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)
from .....services.academics import HiringService
from .....services.application import ApplicationService
from .....services.academics.course_site import CourseSiteService

# Injected Service Fixtures
from .fixtures import hiring_svc
from ..course_site_test import course_site_svc

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
    with pytest.raises(UserPermissionException):
        hiring_svc.get_status(user_data.ambassador, office_hours_data.comp_110_site.id)
        pytest.fail()


def test_get_status_with_permission(hiring_svc: HiringService):
    """Ensures that hiring information can only be viwed by instructors."""
    status = hiring_svc.get_status(user_data.root, office_hours_data.comp_110_site.id)
    assert status is not None


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
    with pytest.raises(UserPermissionException):
        hiring_svc.update_status(
            user_data.ambassador, office_hours_data.comp_110_site.id, status
        )
        pytest.fail()


def test_update_status_administrator(hiring_svc: HiringService):
    status = hiring_svc.get_status(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    hiring_svc.update_status(user_data.root, office_hours_data.comp_110_site.id, status)
    assert True


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


def test_create_hiring_assignment(hiring_svc: HiringService):
    """Ensures that the admin can create hiring assignments."""
    assignment = hiring_svc.create_hiring_assignment(
        user_data.root, hiring_data.new_hiring_assignment
    )
    assert assignment is not None


def test_create_hiring_assignment_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.create_hiring_assignment(
            user_data.ambassador, hiring_data.new_hiring_assignment
        )
        pytest.fail()


def test_update_hiring_assignment(hiring_svc: HiringService):
    """Ensures that the admin can update hiring assignments."""
    assignment = hiring_svc.update_hiring_assignment(
        user_data.root, hiring_data.updated_hiring_assignment
    )
    assert assignment is not None
    assert assignment.id == hiring_data.updated_hiring_assignment.id


def test_update_hiring_assignment_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.update_hiring_assignment(
            user_data.ambassador, hiring_data.updated_hiring_assignment
        )
        pytest.fail()


def test_update_hiring_assignment_not_found(hiring_svc: HiringService):
    """Ensures that hiring data cannot be updated if it does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.update_hiring_assignment(
            user_data.root, hiring_data.new_hiring_assignment
        )
        pytest.fail()


def test_delete_hiring_assignment(hiring_svc: HiringService):
    """Ensures that the admin can delete hiring assignments."""
    hiring_svc.delete_hiring_assignment(
        user_data.root, hiring_data.hiring_assignment.id
    )


def test_delete_hiring_assignment_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.delete_hiring_assignment(
            user_data.ambassador, hiring_data.hiring_assignment.id
        )
        pytest.fail()


def test_delete_hiring_assignment_not_found(hiring_svc: HiringService):
    """Ensures that hiring data cannot be deleted if it does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.delete_hiring_assignment(
            user_data.root, hiring_data.new_hiring_assignment.id
        )
        pytest.fail()


def test_get_hiring_levels(hiring_svc: HiringService):
    """Ensures that the admin can see all hiring levels."""
    levels = hiring_svc.get_hiring_levels(user_data.root)
    assert levels is not None
    assert len(levels) == 1


def test_get_hiring_level_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able see hiring levels."""
    with pytest.raises(UserPermissionException):
        hiring_svc.get_hiring_levels(user_data.ambassador)
        pytest.fail()


def test_create_hiring_level(hiring_svc: HiringService):
    """Ensures that the admin can create hiring levels."""
    level = hiring_svc.create_hiring_level(user_data.root, hiring_data.new_level)
    assert level is not None


def test_create_hiring_level_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.create_hiring_level(user_data.ambassador, hiring_data.new_level)
        pytest.fail()


def test_update_hiring_level(hiring_svc: HiringService):
    """Ensures that the admin can update hiring levels."""
    level = hiring_svc.update_hiring_level(
        user_data.root, hiring_data.updated_uta_level
    )
    assert level is not None
    assert level.id == hiring_data.updated_uta_level.id


def test_update_hiring_level_checks_permission(hiring_svc: HiringService):
    """Ensures that nobody else is able to modify hiring data."""
    with pytest.raises(UserPermissionException):
        hiring_svc.update_hiring_level(
            user_data.ambassador, hiring_data.updated_uta_level
        )
        pytest.fail()


def test_update_hiring_level_not_found(hiring_svc: HiringService):
    """Ensures that hiring data cannot be deleted if it does not exist."""
    with pytest.raises(ResourceNotFoundException):
        hiring_svc.update_hiring_level(user_data.root, hiring_data.new_level)
        pytest.fail()


def test_create_missing_course_sites_for_term(
    hiring_svc: HiringService, course_site_svc: CourseSiteService
):
    user = user_data.root
    term = term_data.current_term
    overview_pre = hiring_svc.get_hiring_admin_overview(user, term.id)
    hiring_svc.create_missing_course_sites_for_term(user, term.id)
    overview_post = hiring_svc.get_hiring_admin_overview(user, term.id)
    assert len(overview_post.sites) > len(overview_pre.sites)


def test_get_phd_applicants(hiring_svc: HiringService):
    user = user_data.root
    term = term_data.current_term
    applicants = hiring_svc.get_phd_applicants(user, term.id)
    assert len(applicants) > 0
    for applicant in applicants:
        assert applicant.program_pursued in {"PhD", "PhD (ABD)"}


def test_iter_comp_227_matches_for_term_csv(hiring_svc: HiringService):
    """Exports only the seeded eligible match with the agreed six columns."""
    rows = list(
        hiring_svc.iter_comp_227_matches_for_term_csv(
            user_data.root, term_data.current_term.id
        )
    )

    assert rows == [
        {
            "student_name": "Sally Student",
            "pid": "111111111",
            "email": "user@unc.edu",
            "matching_course": "COMP 110",
            "matching_instructor": "Ina Instructor",
            "comp_227_preference": Comp227.EITHER.value,
        }
    ]


def test_iter_comp_227_matches_uses_student_preference_and_deduplicates(
    hiring_svc: HiringService, session: Session
):
    """Student rank wins conflicts and duplicate site data remains one CSV row."""
    application = session.get(ApplicationEntity, hiring_data.application_one.id)
    assert application is not None
    application.comp_227 = Comp227.CREDIT

    comp_110_review = session.scalar(
        select(ApplicationReviewEntity).where(
            ApplicationReviewEntity.application_id == application.id,
            ApplicationReviewEntity.course_site_id
            == office_hours_data.comp_110_site.id,
        )
    )
    assert comp_110_review is not None
    comp_110_review.status = ApplicationReviewStatus.PREFERRED
    comp_110_review.preference = 50

    session.add_all(
        [
            ApplicationReviewEntity(
                application_id=application.id,
                course_site_id=office_hours_data.comp_301_site.id,
                status=ApplicationReviewStatus.PREFERRED,
                preference=0,
                notes="",
            ),
            ApplicationReviewEntity(
                application_id=application.id,
                course_site_id=office_hours_data.comp_110_site.id,
                status=ApplicationReviewStatus.PREFERRED,
                preference=51,
                notes="",
            ),
            SectionMemberEntity(
                section_id=section_data.comp_110_001_current_term.id,
                user_id=user_data.root.id,
                member_role=RosterRole.INSTRUCTOR,
            ),
        ]
    )

    session.execute(
        section_application_table.update()
        .where(
            section_application_table.c.application_id == application.id,
            section_application_table.c.section_id
            == section_data.comp_301_001_current_term.id,
        )
        .values(preference=1)
    )
    session.execute(
        section_application_table.update()
        .where(
            section_application_table.c.application_id == application.id,
            section_application_table.c.section_id
            == section_data.comp_110_001_current_term.id,
        )
        .values(preference=2)
    )
    session.execute(
        section_application_table.update()
        .where(
            section_application_table.c.application_id == application.id,
            section_application_table.c.section_id
            == section_data.comp_110_002_current_term.id,
        )
        .values(preference=0)
    )
    session.commit()

    rows = list(
        hiring_svc.iter_comp_227_matches_for_term_csv(
            user_data.root, term_data.current_term.id
        )
    )

    assert len(rows) == 2
    assert rows[0] == {
        "student_name": "Stewie Student",
        "pid": "555555555",
        "email": "stewie@unc.edu",
        "matching_course": "COMP 110",
        "matching_instructor": "Ina Instructor, Rhonda Root",
        "comp_227_preference": Comp227.CREDIT.value,
    }
    assert rows[1]["comp_227_preference"] == Comp227.EITHER.value


def test_iter_comp_227_matches_filters_ineligible_applications(
    hiring_svc: HiringService, session: Session
):
    """Compensation-only, GTA, wrong-term, and unpreferred rows are excluded."""
    compensation_application = session.get(
        ApplicationEntity, hiring_data.application_three.id
    )
    wrong_term_application = session.get(
        ApplicationEntity, hiring_data.application_four.id
    )
    assert compensation_application is not None
    assert wrong_term_application is not None
    compensation_application.comp_227 = Comp227.COMPENSATION
    wrong_term_application.term_id = term_data.previous_term.id

    compensation_review = session.scalar(
        select(ApplicationReviewEntity).where(
            ApplicationReviewEntity.application_id == compensation_application.id
        )
    )
    assert compensation_review is not None
    compensation_review.status = ApplicationReviewStatus.PREFERRED

    session.add_all(
        [
            ApplicationReviewEntity(
                application_id=wrong_term_application.id,
                course_site_id=office_hours_data.comp_110_site.id,
                status=ApplicationReviewStatus.PREFERRED,
                preference=0,
                notes="",
            ),
            ApplicationReviewEntity(
                application_id=hiring_data.application_five.id,
                course_site_id=office_hours_data.comp_301_site.id,
                status=ApplicationReviewStatus.PREFERRED,
                preference=0,
                notes="",
            ),
        ]
    )
    session.commit()

    rows = list(
        hiring_svc.iter_comp_227_matches_for_term_csv(
            user_data.root, term_data.current_term.id
        )
    )

    assert [row["student_name"] for row in rows] == ["Sally Student"]


def test_iter_comp_227_matches_for_term_csv_empty(
    hiring_svc: HiringService, session: Session
):
    """A term without a preferred eligible application yields no service rows."""
    preferred_review = session.scalar(
        select(ApplicationReviewEntity).where(
            ApplicationReviewEntity.application_id == hiring_data.application_two.id
        )
    )
    assert preferred_review is not None
    preferred_review.status = ApplicationReviewStatus.NOT_PREFERRED
    session.commit()

    assert (
        list(
            hiring_svc.iter_comp_227_matches_for_term_csv(
                user_data.root, term_data.current_term.id
            )
        )
        == []
    )


def test_iter_comp_227_matches_for_term_csv_checks_permission(
    hiring_svc: HiringService,
):
    """Only hiring administrators may export COMP 227 matches."""
    with pytest.raises(UserPermissionException):
        hiring_svc.iter_comp_227_matches_for_term_csv(
            user_data.ambassador, term_data.current_term.id
        )
