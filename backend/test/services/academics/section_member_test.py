"""Tests for Section Member Service."""

import pytest

from fastapi import HTTPException
from ....entities.academics.section_entity import SectionEntity

from ....models.office_hours.course_site_details import CourseSiteDetails
from ....models.office_hours.course_site import CourseSite
from ....models.academics.section_member import SectionMember
from ....models.roster_role import RosterRole
from ....models.pagination import PaginationParams

from ....services.academics.section_member import SectionMemberService
from ....services.exceptions import ResourceNotFoundException, CoursePermissionException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, section_member_svc
from .course_site_scenario import CourseSiteScenario, arrange_course_site_scenario
from .scenario import AcademicsScenario, arrange_academics_scenario

__authors__ = ["Ajay Gandecha", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def academics_scenario(session) -> AcademicsScenario:
    return arrange_academics_scenario(session)


@pytest.fixture()
def course_site_scenario(session) -> CourseSiteScenario:
    return arrange_course_site_scenario(session)


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


def test_create_from_csv_rejects_multiple_sections(
    section_member_svc: SectionMemberService, academics_scenario: AcademicsScenario
):
    roster_lines = academics_scenario.roster_csv.splitlines()
    roster_lines[-1] = roster_lines[-1].replace("COMP301.001.S224", "COMP301.002.S224")

    with pytest.raises(HTTPException):
        section_member_svc.import_users_from_csv(
            academics_scenario.auth.instructor,
            academics_scenario.comp_301_001_current_term.id,
            csv_data="\n".join(roster_lines),
        )
        pytest.fail()


def test_add_user_section_memberships_by_oh_sections(
    session,
    section_member_svc: SectionMemberService,
    course_site_scenario: CourseSiteScenario,
):
    section_entity = session.get(
        SectionEntity, course_site_scenario.academics.comp_301_002_current_term.id
    )
    section_entity.course_site_id = course_site_scenario.comp_110_site.id
    session.commit()

    memberships = section_member_svc.add_user_section_memberships_by_oh_sections(
        course_site_scenario.academics.auth.root,
        [course_site_scenario.comp_110_site],
    )

    assert len(memberships) == 1
    assert memberships[0].user_id == course_site_scenario.academics.auth.root.id


def test_add_user_section_memberships_by_oh_sections_rejects_duplicate_membership(
    session,
    section_member_svc: SectionMemberService,
    course_site_scenario: CourseSiteScenario,
):
    section_entity = session.get(
        SectionEntity, course_site_scenario.academics.comp_301_002_current_term.id
    )
    section_entity.course_site_id = course_site_scenario.comp_110_site.id
    session.commit()

    section_member_svc.add_user_section_memberships_by_oh_sections(
        course_site_scenario.academics.auth.root,
        [course_site_scenario.comp_110_site],
    )

    with pytest.raises(Exception):
        section_member_svc.add_user_section_memberships_by_oh_sections(
            course_site_scenario.academics.auth.root,
            [course_site_scenario.comp_110_site],
        )
        pytest.fail()


def test_add_user_section_memberships_by_oh_sections_requires_academic_section(
    section_member_svc: SectionMemberService,
    course_site_scenario: CourseSiteScenario,
):
    with pytest.raises(ResourceNotFoundException):
        section_member_svc.add_user_section_memberships_by_oh_sections(
            course_site_scenario.academics.auth.root,
            [CourseSite(id=999, title="Missing Site", term_id="Curr")],
        )
        pytest.fail()
