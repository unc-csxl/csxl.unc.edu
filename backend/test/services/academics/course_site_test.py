"""Tests for Course Site Service."""

import pytest

from ....entities.academics.section_member_entity import SectionMemberEntity
from ....models.pagination import PaginationParams, Paginated
from ....models.academics.my_courses import (
    TermOverview,
    CourseMemberOverview,
    OfficeHoursOverview,
    CourseSiteOverview,
)
from ....models.public_user import PublicUser
from ....models.office_hours.course_site import CourseSite, UpdatedCourseSite
from ....services.academics.course_site import CourseSiteService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import course_site_svc
from .course_site_scenario import CourseSiteScenario, arrange_course_site_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def course_site_scenario(session) -> CourseSiteScenario:
    return arrange_course_site_scenario(session)


def public_user_for(user) -> PublicUser:
    return PublicUser(
        id=user.id,
        onyen=user.onyen,
        first_name=user.first_name,
        last_name=user.last_name,
        pronouns=user.pronouns,
        email=user.email,
    )


def test_get_user_course_sites(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that users are able to access term overviews."""
    term_overview = course_site_svc.get_user_course_sites(
        course_site_scenario.academics.auth.instructor
    )
    assert isinstance(term_overview, list)
    assert isinstance(term_overview[0], TermOverview)
    assert len(term_overview) == 2
    assert term_overview[-1].id == course_site_scenario.academics.current_term.id
    assert len(term_overview[-1].sites) == 2


def test_get_course_site_roster(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that instructors can access their course rosters."""
    pagination_params = PaginationParams()
    roster = course_site_svc.get_course_site_roster(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
        pagination_params,
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 4


def test_get_course_site_roster_order_by(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that course roster ordering works with pagination."""
    pagination_params = PaginationParams(order_by="last_name")
    roster = course_site_svc.get_course_site_roster(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
        pagination_params,
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 4

    for i in range(len(roster.items) - 1):
        assert roster.items[i].last_name <= roster.items[i + 1].last_name


def test_get_course_site_roster_filter(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that course roster filtering works with pagination."""
    filter = "Student"
    pagination_params = PaginationParams(filter=filter)
    roster = course_site_svc.get_course_site_roster(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
        pagination_params,
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 2

    for item in roster.items:
        assert item.last_name == filter


def test_get_course_site_roster_not_member(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that non-members are unable to access course rosters."""
    pagination_params = PaginationParams()
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_course_site_roster(
            course_site_scenario.academics.auth.ambassador,
            course_site_scenario.comp_110_site.id,
            pagination_params,
        )
        pytest.fail()


def test_get_current_office_hour_events(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that members are able to access current office hour events."""
    office_hours = course_site_svc.get_current_office_hour_events(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
    )
    assert len(office_hours) == 2
    assert isinstance(office_hours[0], OfficeHoursOverview)
    assert office_hours[0].id == course_site_scenario.comp_110_current_office_hours.id


def test_get_current_office_hour_events_not_member(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that non-members cannot access current office hour events."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_current_office_hour_events(
            course_site_scenario.academics.auth.ambassador,
            course_site_scenario.comp_110_site.id,
        )
        pytest.fail()


def test_get_future_office_hour_events(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that members are able to access future office hour events."""
    pagination_params = PaginationParams()
    office_hours = course_site_svc.get_future_office_hour_events(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
        pagination_params,
    )
    assert isinstance(office_hours, Paginated)
    assert office_hours.length == 7
    assert isinstance(office_hours.items[0], OfficeHoursOverview)
    assert (
        office_hours.items[0].id == course_site_scenario.comp_110_future_office_hours.id
    )


def test_get_future_office_hour_events_not_member(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that non-members cannot access future office hour events."""
    pagination_params = PaginationParams()
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_future_office_hour_events(
            course_site_scenario.academics.auth.ambassador,
            course_site_scenario.comp_110_site.id,
            pagination_params,
        )
        pytest.fail()


def test_get_past_office_hour_events(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that members are able to access past office hour events."""
    pagination_params = PaginationParams()
    office_hours = course_site_svc.get_past_office_hour_events(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
        pagination_params,
    )
    assert isinstance(office_hours, Paginated)
    assert office_hours.length == 1
    assert isinstance(office_hours.items[0], OfficeHoursOverview)
    assert (
        office_hours.items[0].id == course_site_scenario.comp_110_past_office_hours.id
    )


def test_get_past_office_hour_events_not_member(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that non-members cannot access past office hour events."""
    pagination_params = PaginationParams()
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_past_office_hour_events(
            course_site_scenario.academics.auth.ambassador,
            course_site_scenario.comp_110_site.id,
            pagination_params,
        )
        pytest.fail()


def test_create(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that instructors can create course sites."""
    course_site = course_site_svc.create(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.new_course_site,
    )
    assert course_site is not None
    assert isinstance(course_site, CourseSite)
    assert course_site.term_id == course_site_scenario.new_course_site.term_id


def test_create_term_mismatch(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be made with sections of different terms."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.new_course_site_term_mismatch,
        )
        pytest.fail()


def test_create_term_nonmember(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be made when user is not a member of a section."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.new_course_site_term_nonmember,
        )
        pytest.fail()


def test_create_term_noninstructor(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be made when user is not an instructor of a section."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.new_course_site_term_noninstructor,
        )
        pytest.fail()


def test_create_term_already_in_site(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be made when a section is already in another site."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.new_course_site_term_already_in_site,
        )
        pytest.fail()


def test_update(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that instructors can update course sites."""
    course_site = course_site_svc.update(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.updated_comp_110_site.model_copy(deep=True),
    )
    assert course_site is not None
    assert isinstance(course_site, CourseSite)
    assert course_site.term_id == course_site_scenario.updated_comp_110_site.term_id


def test_update_term_mismatch(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be updated with sections of different terms."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.updated_comp_110_site_term_mismatch.model_copy(
                deep=True
            ),
        )
        pytest.fail()


def test_update_term_does_not_exist(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be updated when user is not a member of a section."""
    with pytest.raises(ResourceNotFoundException):
        course_site_svc.update(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.updated_course_does_not_exist.model_copy(deep=True),
        )
        pytest.fail()


def test_update_term_nonmember(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be updated when user is not a member of a section."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.updated_course_site_term_nonmember.model_copy(
                deep=True
            ),
        )
        pytest.fail()


def test_update_term_noninstructor(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be updated when user is not an instructor of a section."""
    new_site = course_site_svc.create(
        course_site_scenario.academics.auth.root,
        course_site_scenario.new_site_other_user,
    )
    updated = UpdatedCourseSite(
        id=new_site.id,
        title="Anything",
        term_id=course_site_scenario.academics.current_term.id,
        section_ids=[],
        gtas=[],
        utas=[],
    )
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            course_site_scenario.academics.auth.instructor,
            updated,
        )
        pytest.fail()


def test_update_term_already_in_site(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a course site cannot be made when a section is already in another site."""
    course_site_svc.create(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.new_course_site,
    )
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            course_site_scenario.academics.auth.instructor,
            course_site_scenario.updated_course_site_term_already_in_site.model_copy(
                deep=True
            ),
        )
        pytest.fail()


def test_get(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a member can access the overview of a course site."""
    overview = course_site_svc.get(
        course_site_scenario.academics.auth.instructor,
        course_site_scenario.comp_110_site.id,
    )
    assert overview is not None
    assert isinstance(overview, UpdatedCourseSite)
    assert overview.id == course_site_scenario.comp_110_site.id


def test_get_no_access(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    """Ensures that a member can access the overview of a course site."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.get(
            course_site_scenario.academics.auth.user,
            course_site_scenario.comp_110_site.id,
        )
        pytest.fail()


def test_get_requires_instructor_membership(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    with pytest.raises(CoursePermissionException):
        course_site_svc.get(
            course_site_scenario.academics.auth.uta,
            course_site_scenario.comp_110_site.id,
        )
        pytest.fail()


def test_get_not_found(
    course_site_svc: CourseSiteService, course_site_scenario: CourseSiteScenario
):
    with pytest.raises(CoursePermissionException):
        course_site_svc.get(course_site_scenario.academics.auth.instructor, 404)
        pytest.fail()


def test_update_reassigns_existing_uta_to_gta(
    session,
    course_site_svc: CourseSiteService,
    course_site_scenario: CourseSiteScenario,
):
    updated_site = course_site_scenario.updated_comp_110_site.model_copy(deep=True)
    updated_site.gtas = [public_user_for(course_site_scenario.academics.auth.uta)]
    updated_site.utas = []

    course_site_svc.update(
        course_site_scenario.academics.auth.instructor,
        updated_site,
    )

    membership = session.query(SectionMemberEntity).filter_by(
        section_id=course_site_scenario.academics.comp_110_001_current_term.id,
        user_id=course_site_scenario.academics.auth.uta.id,
    ).one()
    assert membership.member_role.name == "GTA"


def test_update_reassigns_existing_gta_to_uta(
    session,
    course_site_svc: CourseSiteService,
    course_site_scenario: CourseSiteScenario,
):
    membership = session.query(SectionMemberEntity).filter_by(
        section_id=course_site_scenario.academics.comp_110_001_current_term.id,
        user_id=course_site_scenario.academics.auth.uta.id,
    ).one()
    membership.member_role = membership.member_role.GTA
    session.commit()

    updated_site = course_site_scenario.updated_comp_110_site.model_copy(deep=True)
    updated_site.gtas = []
    updated_site.utas = [public_user_for(course_site_scenario.academics.auth.uta)]

    course_site_svc.update(
        course_site_scenario.academics.auth.instructor,
        updated_site,
    )

    refreshed_membership = session.query(SectionMemberEntity).filter_by(
        section_id=course_site_scenario.academics.comp_110_001_current_term.id,
        user_id=course_site_scenario.academics.auth.uta.id,
    ).one()
    assert refreshed_membership.member_role.name == "UTA"


def test_update_keeps_existing_gta_visible_to_uta_reassignment_path(
    session,
    course_site_svc: CourseSiteService,
    course_site_scenario: CourseSiteScenario,
):
    membership = session.query(SectionMemberEntity).filter_by(
        section_id=course_site_scenario.academics.comp_110_001_current_term.id,
        user_id=course_site_scenario.academics.auth.uta.id,
    ).one()
    membership.member_role = membership.member_role.GTA
    session.commit()

    updated_site = course_site_scenario.updated_comp_110_site.model_copy(deep=True)
    updated_site.gtas = [public_user_for(course_site_scenario.academics.auth.uta)]
    updated_site.utas = [public_user_for(course_site_scenario.academics.auth.uta)]

    course_site_svc.update(
        course_site_scenario.academics.auth.instructor,
        updated_site,
    )

    refreshed_membership = session.query(SectionMemberEntity).filter_by(
        section_id=course_site_scenario.academics.comp_110_001_current_term.id,
        user_id=course_site_scenario.academics.auth.uta.id,
    ).one()
    assert refreshed_membership.member_role.name == "UTA"
