"""Tests for Section Member Service."""

import pytest

from fastapi import HTTPException

from ....models.office_hours.course_site_details import CourseSiteDetails
from ....models.academics.section_member import SectionMember
from ....models.roster_role import RosterRole
from ....models.pagination import PaginationParams

from ....services.academics.section_member import SectionMemberService
from ....services.exceptions import ResourceNotFoundException, CoursePermissionException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_member_svc
from .scenario import AcademicsScenario, arrange_academics_scenario

__authors__ = ["Ajay Gandecha", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def academics_scenario(session) -> AcademicsScenario:
    return arrange_academics_scenario(session)


def test_get_section_member_by_id(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    """Test case to retrieve a section member by ID."""
    section_member = section_member_svc.get_section_member_by_id(id=1)

    assert isinstance(section_member, SectionMember)
    assert section_member.id == academics_scenario.comp110_instructor.id


def test_get_section_member_by_id_exception_if_invalid_id(
    section_member_svc: SectionMemberService,
):
    """Test case to check if retrieving a section member by an invalid ID raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        section_member_svc.get_section_member_by_id(id=99)
        pytest.fail()


def test_create_from_csv(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    section_member_svc.import_users_from_csv(
        academics_scenario.auth.instructor,
        academics_scenario.comp_301_001_current_term.id,
        csv_data=academics_scenario.roster_csv,
    )


def test_create_from_csv_twice(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    section_member_svc.import_users_from_csv(
        academics_scenario.auth.instructor,
        academics_scenario.comp_301_001_current_term.id,
        csv_data=academics_scenario.roster_csv,
    )
    section_member_svc.import_users_from_csv(
        academics_scenario.auth.instructor,
        academics_scenario.comp_301_001_current_term.id,
        csv_data=academics_scenario.roster_csv,
    )


def test_create_from_csv_remove(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    section_member_svc.import_users_from_csv(
        academics_scenario.auth.instructor,
        academics_scenario.comp_301_001_current_term.id,
        csv_data=academics_scenario.roster_csv,
    )
    section_member_svc.import_users_from_csv(
        academics_scenario.auth.instructor,
        academics_scenario.comp_301_001_current_term.id,
        csv_data=academics_scenario.smaller_roster_csv,
    )
    section_member_svc.import_users_from_csv(
        academics_scenario.auth.instructor,
        academics_scenario.comp_301_001_current_term.id,
        csv_data=academics_scenario.extra_row_roster_csv,
    )


def test_create_from_csv_not_instructor(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    with pytest.raises(CoursePermissionException):
        section_member_svc.import_users_from_csv(
            academics_scenario.auth.student,
            academics_scenario.comp_301_001_current_term.id,
            csv_data=academics_scenario.roster_csv,
        )
        pytest.fail()


def test_create_from_csv_bad_formatting(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    with pytest.raises(HTTPException):
        section_member_svc.import_users_from_csv(
            academics_scenario.auth.instructor,
            academics_scenario.comp_301_001_current_term.id,
            csv_data=academics_scenario.bad_roster_csv,
        )
        pytest.fail()
