"""Explicit arrange helpers for course site service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ....entities.academics.course_entity import CourseEntity
from ....entities.academics.section_entity import SectionEntity
from ....entities.academics.section_member_entity import SectionMemberEntity
from ....entities.academics.term_entity import TermEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....entities.room_entity import RoomEntity
from ....entities.user_entity import UserEntity
from ....models.academics.course import Course
from ....models.academics.section import Section
from ....models.academics.section_member import SectionMemberDraft
from ....models.academics.term import Term
from ....models.office_hours.course_site import (
    CourseSite,
    NewCourseSite,
    UpdatedCourseSite,
)
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.office_hours import OfficeHours
from ....models.room_details import RoomDetails
from ....models.roster_role import RosterRole
from ....models.user import User
from ..reset_table_id_seq import reset_table_id_seq


@dataclass(frozen=True)
class CourseSiteAuthScenario:
    root: User
    ambassador: User
    user: User
    instructor: User
    uta: User
    student: User


@dataclass(frozen=True)
class CourseSiteAcademicsScenario:
    auth: CourseSiteAuthScenario
    previous_term: Term
    current_term: Term
    comp_101_001: Section
    comp_110_001_current_term: Section
    comp_110_002_current_term: Section
    comp_301_001_current_term: Section
    comp_301_002_current_term: Section
    comp_311_001_current_term: Section
    comp_311_002_current_term: Section


@dataclass
class CourseSiteScenario:
    academics: CourseSiteAcademicsScenario
    comp_110_site: CourseSite
    comp_301_site: CourseSite
    comp_110_current_office_hours: OfficeHours
    comp_110_future_office_hours: OfficeHours
    comp_110_past_office_hours: OfficeHours
    new_course_site: NewCourseSite
    new_course_site_term_mismatch: NewCourseSite
    new_course_site_term_nonmember: NewCourseSite
    new_course_site_term_noninstructor: NewCourseSite
    new_course_site_term_already_in_site: NewCourseSite
    updated_comp_110_site: UpdatedCourseSite
    updated_comp_110_site_term_mismatch: UpdatedCourseSite
    updated_course_site_term_nonmember: UpdatedCourseSite
    updated_course_does_not_exist: UpdatedCourseSite
    updated_course_site_term_noninstructor: UpdatedCourseSite
    updated_course_site_term_already_in_site: UpdatedCourseSite
    new_site_other_user: NewCourseSite


def build_course_site_auth_scenario() -> CourseSiteAuthScenario:
    return CourseSiteAuthScenario(
        root=User(
            id=1,
            pid=999999999,
            onyen="root",
            email="root@unc.edu",
            first_name="Rhonda",
            last_name="Root",
            pronouns="She / Her / Hers",
            accepted_community_agreement=True,
        ),
        ambassador=User(
            id=2,
            pid=888888888,
            onyen="xlstan",
            email="amam@unc.edu",
            first_name="Amy",
            last_name="Ambassador",
            pronouns="They / Them / Theirs",
            accepted_community_agreement=True,
        ),
        user=User(
            id=3,
            pid=111111111,
            onyen="user",
            email="user@unc.edu",
            first_name="Sally",
            last_name="Student",
            pronouns="She / They",
            accepted_community_agreement=True,
        ),
        instructor=User(
            id=4,
            pid=222222222,
            onyen="Ina",
            email="ina@unc.edu",
            first_name="Ina",
            last_name="Instructor",
            pronouns="They / Them / Theirs",
        ),
        uta=User(
            id=5,
            pid=333333333,
            onyen="uhlissa",
            email="uhlissa@unc.edu",
            first_name="Uhlissa",
            last_name="UTA",
            pronouns="They / Them / Theirs",
        ),
        student=User(
            id=6,
            pid=555555555,
            onyen="Stewie",
            email="stewie@unc.edu",
            first_name="Stewie",
            last_name="Student",
            pronouns="They / Them / Theirs",
        ),
    )


def arrange_course_site_scenario(session: Session) -> CourseSiteScenario:
    auth = build_course_site_auth_scenario()
    now = datetime.now().replace(microsecond=0)
    term_length = timedelta(weeks=17)
    term_gap = timedelta(weeks=1)

    previous_term = Term(
        id="Prev",
        name="Previous Term",
        start=now - term_gap - term_length,
        end=now - term_gap,
        applications_open=now - term_gap - term_length,
        applications_close=now - term_gap,
    )
    current_term = Term(
        id="Curr",
        name="Current Term",
        start=now,
        end=now + term_length,
        applications_open=now,
        applications_close=now + term_length,
    )

    courses = [
        Course(
            id="comp110",
            subject_code="COMP",
            number="110",
            title="Introduction to Programming and Data Science",
            description="Introduces students to programming and data science.",
            credit_hours=3,
        ),
        Course(
            id="comp301",
            subject_code="COMP",
            number="301",
            title="Foundations of Programming",
            description="Foundations of programming.",
            credit_hours=3,
        ),
        Course(
            id="comp311",
            subject_code="COMP",
            number="311",
            title="Computer Organization",
            description="Computer organization.",
            credit_hours=3,
        ),
    ]
    sections = {
        "comp_101_001": Section(
            id=1,
            course_id="comp110",
            number="001",
            term_id=previous_term.id,
            meeting_pattern="TTh 12:00PM - 1:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_110_001_current_term": Section(
            id=11,
            course_id="comp110",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 12:00PM - 1:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_110_002_current_term": Section(
            id=12,
            course_id="comp110",
            number="002",
            term_id=current_term.id,
            meeting_pattern="TTh 1:30PM - 2:45PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_301_001_current_term": Section(
            id=13,
            course_id="comp301",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 8:00AM - 9:15AM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_301_002_current_term": Section(
            id=14,
            course_id="comp301",
            number="002",
            term_id=current_term.id,
            meeting_pattern="TTh 5:00PM - 6:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_311_001_current_term": Section(
            id=15,
            course_id="comp311",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 5:00PM - 6:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_311_002_current_term": Section(
            id=16,
            course_id="comp311",
            number="002",
            term_id=current_term.id,
            meeting_pattern="TTh 5:00PM - 6:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
    }
    group_a = RoomDetails(
        id="SN135",
        building="Sitterson",
        room="135",
        nickname="Group A",
        capacity=4,
        reservable=True,
        seats=[],
    )

    session.add_all(UserEntity.from_model(user) for user in vars(auth).values())
    session.add_all(
        [TermEntity.from_model(previous_term), TermEntity.from_model(current_term)]
    )
    session.add_all(CourseEntity.from_model(course) for course in courses)
    session.add(RoomEntity.from_model(group_a))
    session.add_all(SectionEntity.from_model(section) for section in sections.values())
    session.flush()

    memberships = [
        SectionMemberDraft(
            id=1,
            user_id=auth.instructor.id,
            section_id=sections["comp_101_001"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=2,
            user_id=auth.instructor.id,
            section_id=sections["comp_110_001_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=3,
            user_id=auth.instructor.id,
            section_id=sections["comp_110_002_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=4,
            user_id=auth.uta.id,
            section_id=sections["comp_110_001_current_term"].id,
            member_role=RosterRole.UTA,
        ),
        SectionMemberDraft(
            id=5,
            user_id=auth.user.id,
            section_id=sections["comp_110_001_current_term"].id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=6,
            user_id=auth.student.id,
            section_id=sections["comp_110_001_current_term"].id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=7,
            user_id=auth.instructor.id,
            section_id=sections["comp_301_001_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=8,
            user_id=auth.instructor.id,
            section_id=sections["comp_301_002_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=9,
            user_id=auth.ambassador.id,
            section_id=sections["comp_301_001_current_term"].id,
            member_role=RosterRole.UTA,
        ),
        SectionMemberDraft(
            id=10,
            user_id=auth.student.id,
            section_id=sections["comp_301_001_current_term"].id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=11,
            user_id=auth.root.id,
            section_id=sections["comp_311_001_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=12,
            user_id=auth.instructor.id,
            section_id=sections["comp_311_001_current_term"].id,
            member_role=RosterRole.UTA,
        ),
    ]
    session.add_all(
        SectionMemberEntity.from_draft_model(member) for member in memberships
    )
    reset_table_id_seq(session, SectionMemberEntity, SectionMemberEntity.id, 20)

    academics = CourseSiteAcademicsScenario(
        auth=auth,
        previous_term=previous_term,
        current_term=current_term,
        comp_101_001=sections["comp_101_001"],
        comp_110_001_current_term=sections["comp_110_001_current_term"],
        comp_110_002_current_term=sections["comp_110_002_current_term"],
        comp_301_001_current_term=sections["comp_301_001_current_term"],
        comp_301_002_current_term=sections["comp_301_002_current_term"],
        comp_311_001_current_term=sections["comp_311_001_current_term"],
        comp_311_002_current_term=sections["comp_311_002_current_term"],
    )

    comp_110_site = CourseSite(
        id=1, title="COMP 110", term_id=academics.current_term.id
    )
    comp_301_site = CourseSite(
        id=2, title="COMP 301", term_id=academics.current_term.id
    )
    session.add_all(
        [
            CourseSiteEntity.from_model(comp_110_site),
            CourseSiteEntity.from_model(comp_301_site),
        ]
    )
    session.flush()

    for section_key, site_id in [
        ("comp_110_001_current_term", comp_110_site.id),
        ("comp_110_002_current_term", comp_110_site.id),
        ("comp_301_001_current_term", comp_301_site.id),
    ]:
        session.get(SectionEntity, sections[section_key].id).course_site_id = site_id

    office_hours = [
        OfficeHours(
            id=1,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Current COMP 110 office hours",
            location_description="Sitterson 135",
            start_time=now - timedelta(hours=2),
            end_time=now + timedelta(hours=1),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=2,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future COMP 110 office hours",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=3,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Past COMP 110 office hours",
            location_description="Sitterson 135",
            start_time=now - timedelta(days=1, hours=3),
            end_time=now - timedelta(days=1),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=4,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Current recurring office hours",
            location_description="Sitterson 135",
            start_time=now - timedelta(minutes=30),
            end_time=now + timedelta(hours=2),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=5,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 1",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=2),
            end_time=now + timedelta(days=2, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=6,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 2",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=3),
            end_time=now + timedelta(days=3, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=7,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 3",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=4),
            end_time=now + timedelta(days=4, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=8,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 4",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=5),
            end_time=now + timedelta(days=5, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=9,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 5",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=6),
            end_time=now + timedelta(days=6, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=10,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 6",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=3),
            course_site_id=comp_110_site.id,
            room_id=group_a.id,
            recurrence_pattern_id=None,
        ),
    ]
    session.add_all(OfficeHoursEntity.from_model(event) for event in office_hours)
    reset_table_id_seq(session, CourseSiteEntity, CourseSiteEntity.id, 3)
    reset_table_id_seq(session, OfficeHoursEntity, OfficeHoursEntity.id, 11)
    session.commit()

    return CourseSiteScenario(
        academics=academics,
        comp_110_site=comp_110_site,
        comp_301_site=comp_301_site,
        comp_110_current_office_hours=office_hours[0],
        comp_110_future_office_hours=office_hours[1],
        comp_110_past_office_hours=office_hours[2],
        new_course_site=NewCourseSite(
            title="Ina's COMP 301",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_301_002_current_term.id],
        ),
        new_course_site_term_mismatch=NewCourseSite(
            title="Ina's COMP 301",
            term_id=academics.previous_term.id,
            section_ids=[academics.comp_301_002_current_term.id],
        ),
        new_course_site_term_nonmember=NewCourseSite(
            title="Ina's COMP 3x1",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_002_current_term.id,
                academics.comp_311_001_current_term.id,
            ],
        ),
        new_course_site_term_noninstructor=NewCourseSite(
            title="Ina's COMP 3x1",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_002_current_term.id,
                academics.comp_311_002_current_term.id,
            ],
        ),
        new_course_site_term_already_in_site=NewCourseSite(
            title="Ina's COMP courses",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_002_current_term.id,
                academics.comp_110_001_current_term.id,
            ],
        ),
        updated_comp_110_site=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_110_001_current_term.id],
            utas=[],
            gtas=[],
        ),
        updated_comp_110_site_term_mismatch=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_110_001_current_term.id,
                academics.comp_101_001.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_site_term_nonmember=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_110_001_current_term.id,
                academics.comp_311_001_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_does_not_exist=UpdatedCourseSite(
            id=404,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_110_001_current_term.id,
                academics.comp_311_002_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_site_term_noninstructor=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_311_001_current_term.id,
                academics.comp_311_002_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_site_term_already_in_site=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_001_current_term.id,
                academics.comp_110_001_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        new_site_other_user=NewCourseSite(
            title="Rhonda",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_311_001_current_term.id],
        ),
    )
