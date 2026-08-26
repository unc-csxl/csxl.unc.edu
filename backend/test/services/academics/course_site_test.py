"""Tests for Course Site Service."""

import pytest

from sqlalchemy import event, select

from ....models.pagination import PaginationParams, Paginated
from ....models.academics.my_courses import (
    TermOverview,
    CourseMemberOverview,
    OfficeHoursOverview,
    CourseSiteOverview,
)
from ....models.office_hours.course_site import CourseSite, UpdatedCourseSite
from ....entities.academics.section_member_entity import SectionMemberEntity
from ....entities.user_entity import UserEntity
from ....models.roster_role import RosterRole
from ....models.user import User
from ....services.academics.course_site import CourseSiteService
from ....services.exceptions import CoursePermissionException, ResourceNotFoundException

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import course_site_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from .term_data import fake_data_fixture as insert_order_1
from .course_data import fake_data_fixture as insert_order_2
from .section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import user_data
from ..academics import term_data, section_data
from ..office_hours import office_hours_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_user_course_sites(course_site_svc: CourseSiteService):
    """Ensures that users are able to access term overviews."""
    term_overview = course_site_svc.get_user_course_sites(user_data.instructor)
    assert isinstance(term_overview, list)
    assert isinstance(term_overview[0], TermOverview)
    assert len(term_overview) == 2
    assert term_overview[-1].id == term_data.current_term.id
    assert len(term_overview[-1].sites) == 2


def test_get_course_site_roster(course_site_svc: CourseSiteService):
    """Ensures that instructors can access their course rosters."""
    pagination_params = PaginationParams()
    roster = course_site_svc.get_course_site_roster(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 4


def test_get_course_site_roster_order_by(course_site_svc: CourseSiteService):
    """Ensures that course roster ordering works with pagination."""
    pagination_params = PaginationParams(order_by="last_name")
    roster = course_site_svc.get_course_site_roster(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 4

    for i in range(len(roster.items) - 1):
        assert roster.items[i].last_name <= roster.items[i + 1].last_name


def test_get_course_site_roster_filter(course_site_svc: CourseSiteService):
    """Ensures that course roster filtering works with pagination."""
    filter = "Student"
    pagination_params = PaginationParams(filter=filter)
    roster = course_site_svc.get_course_site_roster(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(roster, Paginated)
    assert isinstance(roster.items[0], CourseMemberOverview)
    assert roster.length == 2

    for item in roster.items:
        assert item.last_name == filter


def test_get_course_site_roster_not_member(course_site_svc: CourseSiteService):
    """Ensures that non-members are unable to access course rosters."""
    pagination_params = PaginationParams()
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_course_site_roster(
            user_data.ambassador, office_hours_data.comp_110_site.id, pagination_params
        )
        pytest.fail()


def test_get_current_office_hour_events(course_site_svc: CourseSiteService):
    """Ensures that members are able to access current office hour events."""
    office_hours = course_site_svc.get_current_office_hour_events(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    assert len(office_hours) == 2
    assert isinstance(office_hours[0], OfficeHoursOverview)
    assert office_hours[0].id == office_hours_data.comp_110_current_office_hours.id


def test_get_current_office_hour_events_not_member(course_site_svc: CourseSiteService):
    """Ensures that non-members cannot access current office hour events."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_current_office_hour_events(
            user_data.ambassador, office_hours_data.comp_110_site.id
        )
        pytest.fail()


def test_get_future_office_hour_events(course_site_svc: CourseSiteService):
    """Ensures that members are able to access future office hour events."""
    pagination_params = PaginationParams()
    office_hours = course_site_svc.get_future_office_hour_events(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(office_hours, Paginated)
    assert office_hours.length == 7
    assert isinstance(office_hours.items[0], OfficeHoursOverview)
    assert office_hours.items[0].id == office_hours_data.comp_110_future_office_hours.id


def test_get_future_office_hour_events_not_member(course_site_svc: CourseSiteService):
    """Ensures that non-members cannot access future office hour events."""
    pagination_params = PaginationParams()
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_future_office_hour_events(
            user_data.ambassador, office_hours_data.comp_110_site.id, pagination_params
        )
        pytest.fail()


def test_get_past_office_hour_events(course_site_svc: CourseSiteService):
    """Ensures that members are able to access past office hour events."""
    pagination_params = PaginationParams()
    office_hours = course_site_svc.get_past_office_hour_events(
        user_data.instructor, office_hours_data.comp_110_site.id, pagination_params
    )
    assert isinstance(office_hours, Paginated)
    assert office_hours.length == 1
    assert isinstance(office_hours.items[0], OfficeHoursOverview)
    assert office_hours.items[0].id == office_hours_data.comp_110_past_office_hours.id


def test_get_past_office_hour_events_not_member(course_site_svc: CourseSiteService):
    """Ensures that non-members cannot access past office hour events."""
    pagination_params = PaginationParams()
    with pytest.raises(CoursePermissionException):
        course_site_svc.get_past_office_hour_events(
            user_data.ambassador, office_hours_data.comp_110_site.id, pagination_params
        )
        pytest.fail()


def test_create(course_site_svc: CourseSiteService):
    """Ensures that instructors can create course sites."""
    course_site = course_site_svc.create(
        user_data.instructor, office_hours_data.new_course_site
    )
    assert course_site is not None
    assert isinstance(course_site, CourseSite)
    assert course_site.term_id == office_hours_data.new_course_site.term_id


def test_create_term_mismatch(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be made with sections of different terms."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            user_data.instructor, office_hours_data.new_course_site_term_mismatch
        )
        pytest.fail()


def test_create_term_nonmember(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be made when user is not a member of a section."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            user_data.instructor, office_hours_data.new_course_site_term_nonmember
        )
        pytest.fail()


def test_create_term_noninstructor(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be made when user is not an instructor of a section."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            user_data.instructor, office_hours_data.new_course_site_term_noninstructor
        )
        pytest.fail()


def test_create_term_already_in_site(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be made when a section is already in another site."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.create(
            user_data.instructor, office_hours_data.new_course_site_term_already_in_site
        )
        pytest.fail()


def test_update(course_site_svc: CourseSiteService):
    """Ensures that instructors can update course sites."""
    course_site = course_site_svc.update(
        user_data.instructor, office_hours_data.updated_comp_110_site
    )
    assert course_site is not None
    assert isinstance(course_site, CourseSite)
    assert course_site.term_id == office_hours_data.updated_comp_110_site.term_id


def test_update_large_team_uses_bounded_queries(
    course_site_svc: CourseSiteService, session
):
    """The number of SELECTs must not grow with staff-section combinations."""
    staff_models = [
        User(
            id=100 + index,
            pid=444_000_000 + index,
            onyen=f"course_staff_{index}",
            email=f"course_staff_{index}@unc.edu",
            first_name="Course",
            last_name=f"Staff {index}",
            pronouns="They / Them / Theirs",
        )
        for index in range(24)
    ]
    staff_entities = [UserEntity.from_model(staff) for staff in staff_models]
    session.add_all(staff_entities)
    session.commit()
    staff_profiles = [staff.to_public_model() for staff in staff_entities]

    section_ids = [
        section_data.comp_110_001_current_term.id,
        section_data.comp_110_002_current_term.id,
    ]
    updated_site = UpdatedCourseSite(
        id=office_hours_data.comp_110_site.id,
        title="Large Team Course Site",
        term_id=term_data.current_term.id,
        section_ids=section_ids,
        gtas=staff_profiles[:12],
        utas=staff_profiles[12:],
    )

    select_count = 0

    def count_selects(*args):
        nonlocal select_count
        statement = args[2]
        if statement.lstrip().upper().startswith("SELECT"):
            select_count += 1

    event.listen(session.bind, "before_cursor_execute", count_selects)
    try:
        course_site_svc.update(user_data.instructor, updated_site)
    finally:
        event.remove(session.bind, "before_cursor_execute", count_selects)

    # Loading and updating the course, regardless of team size, requires only a
    # fixed set of SELECTs. The prior implementation added one per staff-section
    # pair on top of eagerly loading a quadratic roster join.
    assert select_count <= 8

    memberships = session.scalars(
        select(SectionMemberEntity).where(
            SectionMemberEntity.section_id.in_(section_ids),
            SectionMemberEntity.user_id.in_([staff.id for staff in staff_models]),
        )
    ).all()
    expected_memberships = {
        (section_id, staff.id, expected_role)
        for section_id in section_ids
        for staff, expected_role in [
            *[(staff, RosterRole.GTA) for staff in staff_models[:12]],
            *[(staff, RosterRole.UTA) for staff in staff_models[12:]],
        ]
    }
    assert {
        (membership.section_id, membership.user_id, membership.member_role)
        for membership in memberships
    } == expected_memberships


def test_update_term_mismatch(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be updated with sections of different terms."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            user_data.instructor, office_hours_data.updated_comp_110_site_term_mismatch
        )
        pytest.fail()


def test_update_term_does_not_exist(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be updated when user is not a member of a section."""
    with pytest.raises(ResourceNotFoundException):
        course_site_svc.update(
            user_data.instructor, office_hours_data.updated_course_does_not_exist
        )
        pytest.fail()


def test_update_term_nonmember(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be updated when user is not a member of a section."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            user_data.instructor, office_hours_data.updated_course_site_term_nonmember
        )
        pytest.fail()


def test_update_term_noninstructor(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be updated when user is not an instructor of a section."""
    new_site = course_site_svc.create(
        user_data.root, office_hours_data.new_site_other_user
    )
    updated = UpdatedCourseSite(
        id=new_site.id,
        title="Anything",
        term_id=term_data.current_term.id,
        section_ids=[],
        gtas=[],
        utas=[],
    )
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            user_data.instructor,
            updated,
        )
        pytest.fail()


def test_update_term_already_in_site(course_site_svc: CourseSiteService):
    """Ensures that a course site cannot be made when a section is already in another site."""
    course_site_svc.create(user_data.instructor, office_hours_data.new_course_site)
    with pytest.raises(CoursePermissionException):
        course_site_svc.update(
            user_data.instructor,
            office_hours_data.updated_course_site_term_already_in_site,
        )
        pytest.fail()


def test_get(course_site_svc: CourseSiteService):
    """Ensures that a member can access the overview of a course site."""
    overview = course_site_svc.get(
        user_data.instructor, office_hours_data.comp_110_site.id
    )
    assert overview is not None
    assert isinstance(overview, UpdatedCourseSite)
    assert overview.id == office_hours_data.comp_110_site.id


def test_get_no_access(course_site_svc: CourseSiteService):
    """Ensures that a member can access the overview of a course site."""
    with pytest.raises(CoursePermissionException):
        course_site_svc.get(user_data.user, office_hours_data.comp_110_site.id)
        pytest.fail()
