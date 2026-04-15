"""Explicit arrange helpers for academics service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ....entities.academics.course_entity import CourseEntity
from ....entities.academics.section_entity import SectionEntity
from ....entities.academics.section_member_entity import SectionMemberEntity
from ....entities.academics.section_room_entity import SectionRoomEntity
from ....entities.academics.term_entity import TermEntity
from ....entities.room_entity import RoomEntity
from ....models.academics.course import Course
from ....models.academics.section import EditedSection, Section
from ....models.academics.section_member import SectionMemberDraft
from ....models.academics.term import Term
from ....models.room_details import RoomDetails
from ....models.room_assignment_type import RoomAssignmentType
from ....models.roster_role import RosterRole
from ..auth_scenario import AuthScenario, arrange_auth_scenario
from ..reset_table_id_seq import reset_table_id_seq


@dataclass
class AcademicsScenario:
    auth: AuthScenario
    previous_term: Term
    current_term: Term
    future_term: Term
    virtual_room: RoomDetails
    comp_101_001: Section
    comp_101_002: Section
    comp_301_001: Section
    comp_523_001_current_term: Section
    comp_210_001_current_term: Section
    comp_110_001_current_term: Section
    comp_110_002_current_term: Section
    comp_301_001_current_term: Section
    comp_301_002_current_term: Section
    comp_311_001_current_term: Section
    comp_311_002_current_term: Section
    new_section: EditedSection
    new_section_with_lecture_room: EditedSection
    edited_comp_110: EditedSection
    edited_comp_110_with_room: EditedSection
    edited_comp_301_with_room: EditedSection
    comp110_instructor: SectionMemberDraft
    roster_csv: str
    smaller_roster_csv: str
    bad_roster_csv: str
    extra_row_roster_csv: str

    @property
    def current_term_sections(self) -> list[Section]:
        return [
            self.comp_523_001_current_term,
            self.comp_210_001_current_term,
            self.comp_110_001_current_term,
            self.comp_110_002_current_term,
            self.comp_301_001_current_term,
            self.comp_301_002_current_term,
            self.comp_311_001_current_term,
            self.comp_311_002_current_term,
        ]


def arrange_academics_scenario(session: Session) -> AcademicsScenario:
    auth = arrange_auth_scenario(session)

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
    future_term = Term(
        id="Future",
        name="Future Term",
        start=current_term.end + term_gap,
        end=current_term.end + term_gap + term_length,
        applications_open=current_term.applications_open + term_gap,
        applications_close=current_term.applications_close + term_gap + term_length,
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
            id="comp210",
            subject_code="COMP",
            number="210",
            title="Data Structures and Analysis",
            description="Data structures and analysis.",
            credit_hours=3,
        ),
        Course(
            id="comp211",
            subject_code="COMP",
            number="211",
            title="Systems Fundamentals",
            description="Systems fundamentals.",
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
        Course(
            id="comp523",
            subject_code="COMP",
            number="523",
            title="Software Engineering Laboratory",
            description="Software engineering laboratory.",
            credit_hours=4,
        ),
    ]
    virtual_room = RoomDetails(
        id="404",
        nickname="Virtual",
        building="Virtual",
        room="Virtual",
        capacity=999,
        reservable=False,
        seats=[],
    )

    comp_101_001 = Section(
        id=1,
        course_id="comp110",
        number="001",
        term_id=previous_term.id,
        meeting_pattern="TTh 12:00PM - 1:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_101_002 = Section(
        id=2,
        course_id="comp110",
        number="002",
        term_id=previous_term.id,
        meeting_pattern="TTh 1:30PM - 2:45PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_301_001 = Section(
        id=5,
        course_id="comp301",
        number="001",
        term_id=previous_term.id,
        meeting_pattern="TTh 8:00AM - 9:15AM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_523_001_current_term = Section(
        id=9,
        course_id="comp523",
        number="001",
        term_id=current_term.id,
        meeting_pattern="TTh 2:00PM - 3:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_210_001_current_term = Section(
        id=10,
        course_id="comp210",
        number="001",
        term_id=current_term.id,
        meeting_pattern="TTh 9:00AM - 10:15AM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_110_001_current_term = Section(
        id=11,
        course_id="comp110",
        number="001",
        term_id=current_term.id,
        meeting_pattern="TTh 12:00PM - 1:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_110_002_current_term = Section(
        id=12,
        course_id="comp110",
        number="002",
        term_id=current_term.id,
        meeting_pattern="TTh 1:30PM - 2:45PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_301_001_current_term = Section(
        id=13,
        course_id="comp301",
        number="001",
        term_id=current_term.id,
        meeting_pattern="TTh 8:00AM - 9:15AM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_301_002_current_term = Section(
        id=14,
        course_id="comp301",
        number="002",
        term_id=current_term.id,
        meeting_pattern="TTh 5:00PM - 6:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_311_001_current_term = Section(
        id=15,
        course_id="comp311",
        number="001",
        term_id=current_term.id,
        meeting_pattern="TTh 5:00PM - 6:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    comp_311_002_current_term = Section(
        id=16,
        course_id="comp311",
        number="002",
        term_id=current_term.id,
        meeting_pattern="TTh 5:00PM - 6:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )

    sections = [
        comp_101_001,
        comp_101_002,
        comp_301_001,
        comp_523_001_current_term,
        comp_210_001_current_term,
        comp_110_001_current_term,
        comp_110_002_current_term,
        comp_301_001_current_term,
        comp_301_002_current_term,
        comp_311_001_current_term,
        comp_311_002_current_term,
    ]

    new_section = EditedSection(
        id=7,
        course_id="comp110",
        number="003",
        term_id=previous_term.id,
        meeting_pattern="MW 1:30PM - 2:45PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
        instructors=[],
    )
    new_section_with_lecture_room = EditedSection(
        id=8,
        course_id="comp110",
        number="003",
        term_id=previous_term.id,
        meeting_pattern="MW 1:30PM - 2:45PM",
        override_title="",
        override_description="",
        lecture_room=virtual_room,
        enrolled=100,
        total_seats=200,
        instructors=[],
    )
    edited_comp_110 = EditedSection(
        id=2,
        course_id="comp110",
        number="002",
        term_id=previous_term.id,
        meeting_pattern="MW 1:30PM - 2:45PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
        instructors=[],
    )
    edited_comp_110_with_room = edited_comp_110.model_copy(
        update={"lecture_room": virtual_room}
    )
    edited_comp_301_with_room = EditedSection(
        id=5,
        course_id="comp301",
        number="001",
        term_id=previous_term.id,
        meeting_pattern="TTh 8:00AM - 9:15AM",
        override_title="",
        override_description="",
        lecture_room=virtual_room,
        enrolled=100,
        total_seats=200,
        instructors=[],
    )

    section_members = [
        SectionMemberDraft(
            id=11,
            user_id=auth.instructor.id,
            section_id=comp_101_001.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=12,
            user_id=auth.uta.id,
            section_id=comp_101_001.id,
            member_role=RosterRole.UTA,
        ),
        SectionMemberDraft(
            id=13,
            user_id=auth.user.id,
            section_id=comp_101_001.id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=14,
            user_id=auth.student.id,
            section_id=comp_101_001.id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=1,
            user_id=auth.instructor.id,
            section_id=comp_110_001_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=18,
            user_id=auth.instructor.id,
            section_id=comp_110_002_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=2,
            user_id=auth.uta.id,
            section_id=comp_110_001_current_term.id,
            member_role=RosterRole.UTA,
        ),
        SectionMemberDraft(
            id=4,
            user_id=auth.user.id,
            section_id=comp_110_001_current_term.id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=5,
            user_id=auth.student.id,
            section_id=comp_110_001_current_term.id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=6,
            user_id=auth.instructor.id,
            section_id=comp_301_001_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=15,
            user_id=auth.instructor.id,
            section_id=comp_301_002_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=7,
            user_id=auth.ambassador.id,
            section_id=comp_301_001_current_term.id,
            member_role=RosterRole.UTA,
        ),
        SectionMemberDraft(
            id=8,
            user_id=auth.student.id,
            section_id=comp_301_001_current_term.id,
            member_role=RosterRole.STUDENT,
        ),
        SectionMemberDraft(
            id=9,
            user_id=auth.instructor.id,
            section_id=comp_523_001_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=10,
            user_id=auth.instructor.id,
            section_id=comp_210_001_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=16,
            user_id=auth.root.id,
            section_id=comp_311_001_current_term.id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=17,
            user_id=auth.instructor.id,
            section_id=comp_311_001_current_term.id,
            member_role=RosterRole.UTA,
        ),
    ]
    comp110_instructor = section_members[4]

    session.add_all(
        [TermEntity.from_model(term) for term in [previous_term, current_term, future_term]]
    )
    session.add_all(CourseEntity.from_model(course) for course in courses)
    session.add(RoomEntity.from_model(virtual_room))
    session.add_all(SectionEntity.from_model(section) for section in sections)
    session.add_all(
        SectionMemberEntity.from_draft_model(member) for member in section_members
    )
    session.add_all(
        [
            SectionRoomEntity(
                section_id=comp_101_001.id,
                room_id=virtual_room.id,
                assignment_type=RoomAssignmentType.LECTURE_ROOM,
            ),
            SectionRoomEntity(
                section_id=comp_101_002.id,
                room_id=virtual_room.id,
                assignment_type=RoomAssignmentType.LECTURE_ROOM,
            ),
        ]
    )
    reset_table_id_seq(session, SectionMemberEntity, SectionMemberEntity.id, 20)
    reset_table_id_seq(session, SectionEntity, SectionEntity.id, 111)
    session.commit()

    roster_csv = """Student,ID,SIS User ID,SIS Login ID,Section,Assignments Current Points,Assignments Final Points,Assignments Current Score,Assignments Unposted Current Score,Assignments Final Score,Assignments Unposted Final Score,Current Points,Final Points,Current Score,Unposted Current Score,Final Score,Unposted Final Score,Current Grade,Unposted Current Grade,Final Grade,Unposted Final Grade
Points Possible,,,,,(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only)
\"Root, Rhonda\",0,999999999,rroot,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Student, Sally\",0,111111111,sstudent,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Student, New\",0,345345345,nstudent,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Jordan, Kris\",0,89898989,kjordan,COMP301.001.S224,,,,,,,,,,,,,,,,"""
    smaller_roster_csv = """Student,ID,SIS User ID,SIS Login ID,Section,Assignments Current Points,Assignments Final Points,Assignments Current Score,Assignments Unposted Current Score,Assignments Final Score,Assignments Unposted Final Score,Current Points,Final Points,Current Score,Unposted Current Score,Final Score,Unposted Final Score,Current Grade,Unposted Current Grade,Final Grade,Unposted Final Grade
Points Possible,,,,,(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only)
\"Root, Rhonda\",0,999999999,rroot,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Jordan, Kris\",0,89898989,kjordan,COMP301.001.S224,,,,,,,,,,,,,,,,"""
    bad_roster_csv = """Student,Assignments Current Points,Assignments Final Points,Assignments Current Score,Assignments Unposted Current Score,Assignments Final Score,Assignments Unposted Final Score,Current Points,Final Points,Current Score,Unposted Current Score,Final Score,Unposted Final Score,Current Grade,Unposted Current Grade,Final Grade,Unposted Final Grade
Points Possible,,,,,(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only)
\"Root, Rhonda\",0,999999999,,,,,,,,,,,,,,,,
\"Student, Sally\",0,sstudent,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Student, New\",0,345345345,nstudent,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Jordan, Kris\",0,89898989,kjordan,COMP301.001.S224,,,,,,,,,,,,,,,,"""
    extra_row_roster_csv = """Student,ID,SIS User ID,SIS Login ID,Section,Assignments Current Points,Assignments Final Points,Assignments Current Score,Assignments Unposted Current Score,Assignments Final Score,Assignments Unposted Final Score,Current Points,Final Points,Current Score,Unposted Current Score,Final Score,Unposted Final Score,Current Grade,Unposted Current Grade,Final Grade,Unposted Final Grade
Points Possible,,,,,(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only)
,,,,,,,,,,,,,,,,,,,,
\"Root, Rhonda\",0,999999999,rroot,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Student, Sally\",0,111111111,sstudent,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Student, New\",0,345345345,nstudent,COMP301.001.S224,,,,,,,,,,,,,,,,
\"Jordan, Kris\",0,89898989,kjordan,COMP301.001.S224,,,,,,,,,,,,,,,,"""

    return AcademicsScenario(
        auth=auth,
        previous_term=previous_term,
        current_term=current_term,
        future_term=future_term,
        virtual_room=virtual_room,
        comp_101_001=comp_101_001,
        comp_101_002=comp_101_002,
        comp_301_001=comp_301_001,
        comp_523_001_current_term=comp_523_001_current_term,
        comp_210_001_current_term=comp_210_001_current_term,
        comp_110_001_current_term=comp_110_001_current_term,
        comp_110_002_current_term=comp_110_002_current_term,
        comp_301_001_current_term=comp_301_001_current_term,
        comp_301_002_current_term=comp_301_002_current_term,
        comp_311_001_current_term=comp_311_001_current_term,
        comp_311_002_current_term=comp_311_002_current_term,
        new_section=new_section,
        new_section_with_lecture_room=new_section_with_lecture_room,
        edited_comp_110=edited_comp_110,
        edited_comp_110_with_room=edited_comp_110_with_room,
        edited_comp_301_with_room=edited_comp_301_with_room,
        comp110_instructor=comp110_instructor,
        roster_csv=roster_csv,
        smaller_roster_csv=smaller_roster_csv,
        bad_roster_csv=bad_roster_csv,
        extra_row_roster_csv=extra_row_roster_csv,
    )