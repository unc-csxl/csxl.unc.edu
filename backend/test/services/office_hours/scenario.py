"""Explicit arrange helpers for office hours service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ....entities.academics.course_entity import CourseEntity
from ....entities.academics.section_entity import SectionEntity
from ....entities.academics.section_member_entity import SectionMemberEntity
from ....entities.academics.term_entity import TermEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ....entities.room_entity import RoomEntity
from ....entities.user_entity import UserEntity
from ....models import RoomDetails, User
from ....models.academics.course import Course
from ....models.academics.section import Section
from ....models.academics.section_member import SectionMemberDraft
from ....models.academics.term import Term
from ....models.office_hours.course_site import CourseSite
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.office_hours import NewOfficeHours, OfficeHours
from ....models.office_hours.ticket import OfficeHoursTicket
from ....models.office_hours.ticket_state import TicketState
from ....models.office_hours.ticket_type import TicketType
from ....models.roster_role import RosterRole
from ....services.office_hours import OfficeHoursService
from ..reset_table_id_seq import reset_table_id_seq


@dataclass
class OfficeHoursScenario:
    instructor: User
    student: User
    ambassador: User
    root: User
    course_site: CourseSite
    section: Section
    instructor_membership: SectionMemberEntity
    student_membership: SectionMemberEntity
    current_office_hours: OfficeHours
    future_office_hours: OfficeHours
    updated_future_event: OfficeHours
    nonexistent_event: OfficeHours
    new_event: NewOfficeHours
    new_event_site_not_found: NewOfficeHours
    queued_ticket: OfficeHoursTicket
    called_ticket: OfficeHoursTicket
    closed_ticket: OfficeHoursTicket
    cancelled_ticket: OfficeHoursTicket


def make_office_hours_service(session: Session) -> OfficeHoursService:
    return OfficeHoursService(session)


def arrange_office_hours_scenario(session: Session) -> OfficeHoursScenario:
    now = datetime.now().replace(microsecond=0)

    term = Term(
        id="F26",
        name="Fall 2026",
        start=datetime(2026, 8, 17, 0, 0),
        end=datetime(2026, 12, 15, 23, 59),
    )
    course = Course(
        id="COMP110",
        subject_code="COMP",
        number="110",
        title="COMP 110",
        description="Intro to Programming",
        credit_hours=3,
    )
    room = RoomDetails(
        id="SN135",
        building="Sitterson",
        room="135",
        nickname="Group A",
        capacity=4,
        reservable=True,
        seats=[],
    )
    instructor = User(
        id=1,
        pid=1,
        onyen="instructor",
        first_name="Ina",
        last_name="Instructor",
        email="instructor@unc.edu",
    )
    student = User(
        id=2,
        pid=2,
        onyen="student",
        first_name="Stu",
        last_name="Student",
        email="student@unc.edu",
    )
    ambassador = User(
        id=3,
        pid=3,
        onyen="ambassador",
        first_name="Amy",
        last_name="Ambassador",
        email="ambassador@unc.edu",
    )
    root = User(
        id=4,
        pid=4,
        onyen="root",
        first_name="Rhonda",
        last_name="Root",
        email="root@unc.edu",
    )
    course_site = CourseSite(id=1, title="COMP 110", term_id=term.id)
    section = Section(
        id=1,
        course_id=course.id,
        number="001",
        term_id=term.id,
        meeting_pattern="MWF 10:00-10:50",
        override_title="",
        override_description="",
        enrolled=1,
        total_seats=30,
    )

    session.add(TermEntity.from_model(term))
    session.add(CourseEntity.from_model(course))
    session.add(RoomEntity.from_model(room))
    session.add_all(
        UserEntity.from_model(user) for user in [instructor, student, ambassador, root]
    )
    session.add(CourseSiteEntity.from_model(course_site))

    section_entity = SectionEntity.from_model(section)
    section_entity.course_site_id = course_site.id
    session.add(section_entity)
    session.flush()

    instructor_membership = SectionMemberEntity.from_draft_model(
        SectionMemberDraft(
            section_id=section.id,
            user_id=instructor.id,
            member_role=RosterRole.INSTRUCTOR,
        )
    )
    student_membership = SectionMemberEntity.from_draft_model(
        SectionMemberDraft(
            section_id=section.id,
            user_id=student.id,
            member_role=RosterRole.STUDENT,
        )
    )
    session.add_all([instructor_membership, student_membership])
    session.flush()

    current_office_hours = OfficeHours(
        id=1,
        type=OfficeHoursEventType.OFFICE_HOURS,
        mode=OfficeHoursEventModeType.IN_PERSON,
        description="Current COMP 110 office hours",
        location_description="Sitterson 135",
        start_time=now - timedelta(hours=2),
        end_time=now + timedelta(hours=1),
        course_site_id=course_site.id,
        room_id=room.id,
        recurrence_pattern_id=None,
    )
    future_office_hours = OfficeHours(
        id=2,
        type=OfficeHoursEventType.OFFICE_HOURS,
        mode=OfficeHoursEventModeType.IN_PERSON,
        description="Future COMP 110 office hours",
        location_description="Sitterson 135",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=3),
        course_site_id=course_site.id,
        room_id=room.id,
        recurrence_pattern_id=None,
    )
    session.add_all(
        [
            OfficeHoursEntity.from_model(current_office_hours),
            OfficeHoursEntity.from_model(future_office_hours),
        ]
    )
    session.flush()

    queued_ticket = OfficeHoursTicket(
        id=1,
        description="Queued ticket",
        type=TicketType.ASSIGNMENT_HELP,
        state=TicketState.QUEUED,
        created_at=now - timedelta(minutes=20),
        called_at=None,
        closed_at=None,
        have_concerns=False,
        caller_notes="",
        office_hours_id=current_office_hours.id,
        caller_id=None,
    )
    called_ticket = OfficeHoursTicket(
        id=2,
        description="Called ticket",
        type=TicketType.CONCEPTUAL_HELP,
        state=TicketState.CALLED,
        created_at=now - timedelta(minutes=25),
        called_at=now - timedelta(minutes=5),
        closed_at=None,
        have_concerns=False,
        caller_notes="Helping now",
        office_hours_id=current_office_hours.id,
        caller_id=instructor_membership.id,
    )
    closed_ticket = OfficeHoursTicket(
        id=3,
        description="Closed ticket",
        type=TicketType.ASSIGNMENT_HELP,
        state=TicketState.CLOSED,
        created_at=now - timedelta(minutes=40),
        called_at=now - timedelta(minutes=25),
        closed_at=now - timedelta(minutes=10),
        have_concerns=False,
        caller_notes="Resolved",
        office_hours_id=current_office_hours.id,
        caller_id=instructor_membership.id,
    )
    cancelled_ticket = OfficeHoursTicket(
        id=4,
        description="Cancelled ticket",
        type=TicketType.CONCEPTUAL_HELP,
        state=TicketState.CANCELED,
        created_at=now - timedelta(minutes=15),
        called_at=None,
        closed_at=None,
        have_concerns=False,
        caller_notes="",
        office_hours_id=current_office_hours.id,
        caller_id=None,
    )

    queued_ticket_entity = OfficeHoursTicketEntity.from_model(queued_ticket)
    queued_ticket_entity.creators = [student_membership]
    called_ticket_entity = OfficeHoursTicketEntity.from_model(called_ticket)
    called_ticket_entity.creators = [student_membership]
    called_ticket_entity.caller = instructor_membership
    closed_ticket_entity = OfficeHoursTicketEntity.from_model(closed_ticket)
    closed_ticket_entity.creators = [student_membership]
    closed_ticket_entity.caller = instructor_membership
    cancelled_ticket_entity = OfficeHoursTicketEntity.from_model(cancelled_ticket)
    cancelled_ticket_entity.creators = [student_membership]

    session.add_all(
        [
            queued_ticket_entity,
            called_ticket_entity,
            closed_ticket_entity,
            cancelled_ticket_entity,
        ]
    )
    reset_table_id_seq(
        session, CourseSiteEntity, CourseSiteEntity.id, course_site.id + 1
    )
    reset_table_id_seq(session, SectionEntity, SectionEntity.id, section.id + 1)
    reset_table_id_seq(
        session,
        SectionMemberEntity,
        SectionMemberEntity.id,
        student_membership.id + 1,
    )
    reset_table_id_seq(
        session,
        OfficeHoursEntity,
        OfficeHoursEntity.id,
        future_office_hours.id + 1,
    )
    reset_table_id_seq(
        session,
        OfficeHoursTicketEntity,
        OfficeHoursTicketEntity.id,
        cancelled_ticket.id + 1,
    )
    session.commit()

    updated_future_event = future_office_hours.model_copy(
        update={
            "description": "Updated future office hours",
            "location_description": "Updated location",
            "start_time": future_office_hours.start_time + timedelta(minutes=30),
            "end_time": future_office_hours.end_time + timedelta(minutes=30),
        }
    )
    nonexistent_event = future_office_hours.model_copy(update={"id": 404})
    new_event = NewOfficeHours(
        type=OfficeHoursEventType.OFFICE_HOURS,
        mode=OfficeHoursEventModeType.IN_PERSON,
        description="New office hours",
        location_description="Sitterson 135",
        start_time=now + timedelta(days=3),
        end_time=now + timedelta(days=3, hours=1),
        course_site_id=course_site.id,
        room_id=room.id,
        recurrence_pattern_id=None,
    )
    new_event_site_not_found = new_event.model_copy(update={"course_site_id": 404})

    return OfficeHoursScenario(
        instructor=instructor,
        student=student,
        ambassador=ambassador,
        root=root,
        course_site=course_site,
        section=section,
        instructor_membership=instructor_membership,
        student_membership=student_membership,
        current_office_hours=current_office_hours,
        future_office_hours=future_office_hours,
        updated_future_event=updated_future_event,
        nonexistent_event=nonexistent_event,
        new_event=new_event,
        new_event_site_not_found=new_event_site_not_found,
        queued_ticket=queued_ticket,
        called_ticket=called_ticket,
        closed_ticket=closed_ticket,
        cancelled_ticket=cancelled_ticket,
    )
