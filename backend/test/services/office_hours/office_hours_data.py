"""Test Data for Office Hours."""

import pytest
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from ...services.reset_table_id_seq import reset_table_id_seq

from ....test.services import user_data, room_data
from ..academics import section_data
from ..academics import term_data

from ....entities.office_hours import user_created_tickets_table
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ....entities.academics.section_entity import SectionEntity
from ....entities.office_hours.office_hours_recurrence_pattern_entity import (
    OfficeHoursRecurrencePatternEntity,
)


from ....models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
    OfficeHoursRecurrencePattern,
)
from ....models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.course_site import (
    CourseSite,
    NewCourseSite,
    UpdatedCourseSite,
)
from ....models.office_hours.ticket import OfficeHoursTicket, NewOfficeHoursTicket
from ....models.office_hours.ticket_type import TicketType
from ....models.office_hours.ticket_state import TicketState

__authors__ = [
    "Ajay Gandecha",
    "Madelyn Andrews",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Course Site Data

# COMP 110:

# Site
comp_110_site = CourseSite(id=1, title="COMP 110", term_id=term_data.current_term.id)
comp_301_site = CourseSite(id=2, title="COMP 301", term_id=term_data.current_term.id)

# Sections
comp_110_sections = (
    [
        section_data.comp_110_001_current_term,
        section_data.comp_110_002_current_term,
    ],
    comp_110_site.id,
)
comp_301_sections = (
    [section_data.comp_301_001_current_term],
    comp_301_site.id,
)


# Office Hours
comp_110_current_office_hours = OfficeHours(
    id=1,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Current CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() - timedelta(hours=2),
    end_time=datetime.now() + timedelta(hours=1),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)
comp_110_future_office_hours = OfficeHours(
    id=2,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Future CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)
comp_110_past_office_hours = OfficeHours(
    id=3,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Past CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() - timedelta(days=1, hours=3),
    end_time=datetime.now() - timedelta(days=1),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

# Recurring Office Hours
recurrence_pattern = OfficeHoursRecurrencePattern(
    id=1,
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7),
    recur_monday=True,
    recur_tuesday=True,
    recur_wednesday=True,
    recur_thursday=True,
    recur_friday=True,
    recur_saturday=True,
    recur_sunday=True,
)
first_recurring_event = OfficeHours(
    id=4,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
second_recurring_event = OfficeHours(
    id=5,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
third_recurring_event = OfficeHours(
    id=6,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=2),
    end_time=datetime.now() + timedelta(days=2, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
fourth_recurring_event = OfficeHours(
    id=7,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=3),
    end_time=datetime.now() + timedelta(days=3, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
fifth_recurring_event = OfficeHours(
    id=8,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=4),
    end_time=datetime.now() + timedelta(days=4, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
sixth_recurring_event = OfficeHours(
    id=9,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=5),
    end_time=datetime.now() + timedelta(days=5, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
seventh_recurring_event = OfficeHours(
    id=10,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=6),
    end_time=datetime.now() + timedelta(days=6, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)

# Tickets
comp_110_queued_ticket = OfficeHoursTicket(
    id=1,
    description="My Docker container is crashing!! Pls help me I beg you..",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.QUEUED,
    created_at=datetime.now(),
    called_at=None,
    closed_at=None,
    have_concerns=False,
    caller_notes="",
    office_hours_id=comp_110_current_office_hours.id,
    caller_id=None,
)
comp_110_cancelled_ticket = OfficeHoursTicket(
    id=2,
    description="I don't need help, but I want to visit my friend.",
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CANCELED,
    created_at=datetime.now(),
    called_at=None,
    closed_at=None,
    have_concerns=False,
    caller_notes="",
    office_hours_id=comp_110_current_office_hours.id,
    caller_id=None,
)
comp_110_called_ticket = OfficeHoursTicket(
    id=3,
    description="I do not know how to exit vim. Do I need to burn my PC?",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CALLED,
    created_at=datetime.now() - timedelta(minutes=1),
    called_at=datetime.now(),
    closed_at=None,
    have_concerns=False,
    caller_notes="",
    office_hours_id=comp_110_current_office_hours.id,
    caller_id=section_data.comp110_instructor.id,
)
comp_110_closed_ticket = OfficeHoursTicket(
    id=4,
    description="How do I turn on my computer?",
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=2),
    called_at=datetime.now() - timedelta(minutes=1),
    closed_at=datetime.now(),
    have_concerns=True,
    caller_notes="Student could not find the power button on their laptop.",
    office_hours_id=comp_110_current_office_hours.id,
    caller_id=section_data.comp110_instructor.id,
)
comp_110_ticket_creators = [
    (comp_110_queued_ticket, [section_data.comp110_student_1.id]),
    (comp_110_cancelled_ticket, [section_data.comp110_student_1.id]),
    (comp_110_called_ticket, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket, [section_data.comp110_student_1.id]),
]

# All
sites = [comp_110_site, comp_301_site]
section_pairings = [comp_110_sections, comp_301_sections]

recurrence_patterns = [recurrence_pattern]

office_hours = [
    comp_110_current_office_hours,
    comp_110_future_office_hours,
    comp_110_past_office_hours,
    first_recurring_event,
    second_recurring_event,
    third_recurring_event,
    fourth_recurring_event,
    fifth_recurring_event,
    sixth_recurring_event,
    seventh_recurring_event,
]

oh_tickets = [
    comp_110_queued_ticket,
    comp_110_cancelled_ticket,
    comp_110_called_ticket,
    comp_110_closed_ticket,
]
ticket_user_pairings = [comp_110_ticket_creators]


def insert_fake_data(session: Session):

    # Step 1: Add sites to database

    for site in sites:
        entity = CourseSiteEntity.from_model(site)
        session.add(entity)

    reset_table_id_seq(
        session,
        CourseSiteEntity,
        CourseSiteEntity.id,
        len(sites) + 1,
    )

    session.commit()

    # Step 2: Add sections to course sites
    for sections, site_id in section_pairings:
        for section in sections:
            section_entity = session.get(SectionEntity, section.id)
            section_entity.course_site_id = site_id

    session.commit()

    # Step 3: Add office hours to database
    for pattern in recurrence_patterns:
        recurrence_pattern_entity = OfficeHoursRecurrencePatternEntity.from_model(
            pattern
        )
        session.add(recurrence_pattern_entity)

    for oh in office_hours:
        office_hours_entity = OfficeHoursEntity.from_model(oh)
        session.add(office_hours_entity)

    reset_table_id_seq(
        session,
        OfficeHoursEntity,
        OfficeHoursEntity.id,
        len(office_hours) + 1,
    )

    reset_table_id_seq(
        session,
        OfficeHoursRecurrencePatternEntity,
        OfficeHoursRecurrencePatternEntity.id,
        len(recurrence_patterns) + 1,
    )

    session.commit()

    # Step 4: Add tickets to database

    for ticket in oh_tickets:
        ticket_entity = OfficeHoursTicketEntity.from_model(ticket)
        session.add(ticket_entity)

    reset_table_id_seq(
        session,
        OfficeHoursTicketEntity,
        OfficeHoursTicketEntity.id,
        len(oh_tickets) + 1,
    )

    session.commit()

    # Step 5: Add users as ticket creators
    for pairing in ticket_user_pairings:
        for ticket, user_ids in pairing:
            for user_id in user_ids:
                session.execute(
                    user_created_tickets_table.insert().values(
                        {
                            "ticket_id": ticket.id,
                            "member_id": user_id,
                        }
                    )
                )

    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield


# Data objects for testing purposes

new_ticket = NewOfficeHoursTicket(
    description="Help me!",
    type=TicketType.ASSIGNMENT_HELP,
    office_hours_id=comp_110_current_office_hours.id,
)

new_course_site = NewCourseSite(
    title="Ina's COMP 301",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
    ],
)

new_course_site_term_mismatch = NewCourseSite(
    title="Ina's COMP 301",
    term_id=term_data.f_23.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
    ],
)


new_course_site_term_nonmember = NewCourseSite(
    title="Ina's COMP 3x1",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
        section_data.comp_311_001_current_term.id,
    ],
)
new_course_site_term_noninstructor = NewCourseSite(
    title="Ina's COMP 3x1",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
        section_data.comp_311_002_current_term.id,
    ],
)


new_course_site_term_already_in_site = NewCourseSite(
    title="Ina's COMP courses",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
        section_data.comp_110_001_current_term.id,
    ],
)

updated_comp_110_site = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[section_data.comp_110_001_current_term.id],
    utas=[],
    gtas=[],
)

updated_comp_110_site_term_mismatch = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_110_001_current_term.id,
        section_data.comp_101_001.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_site_term_nonmember = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_110_001_current_term.id,
        section_data.comp_311_001_current_term.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_does_not_exist = UpdatedCourseSite(
    id=404,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_110_001_current_term.id,
        section_data.comp_311_002_current_term.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_site_term_noninstructor = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_311_001_current_term.id,
        section_data.comp_311_002_current_term.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_site_term_already_in_site = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_001_current_term.id,
        section_data.comp_110_001_current_term.id,
    ],
    utas=[],
    gtas=[],
)

new_site_other_user = NewCourseSite(
    title="Rhonda",
    term_id=term_data.current_term.id,
    section_ids=[section_data.comp_311_001_current_term.id],
)

new_event = NewOfficeHours(
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Sample",
    location_description="Sample",
    start_time=datetime.now(),
    end_time=datetime.now(),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

new_recurrence_pattern = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    recur_monday=True,
    recur_tuesday=True,
    recur_wednesday=True,
    recur_thursday=True,
    recur_friday=True,
    recur_saturday=True,
    recur_sunday=True,
)

invalid_recurrence_pattern_days = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    recur_monday=False,
    recur_tuesday=False,
    recur_wednesday=False,
    recur_thursday=False,
    recur_friday=False,
    recur_saturday=False,
    recur_sunday=False,
)

invalid_recurrence_pattern_end = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now() - timedelta(days=14),
    end_date=datetime.now() - timedelta(days=13),
    recur_monday=True,
    recur_tuesday=False,
    recur_wednesday=False,
    recur_thursday=False,
    recur_friday=False,
    recur_saturday=False,
    recur_sunday=False,
)

new_event_site_not_found = NewOfficeHours(
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Sample",
    location_description="Sample",
    start_time=datetime.now(),
    end_time=datetime.now(),
    course_site_id=404,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

updated_future_event = OfficeHours(
    id=2,
    type=OfficeHoursEventType.REVIEW_SESSION,
    mode=OfficeHoursEventModeType.VIRTUAL_OUR_LINK,
    description="Future CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

nonexistent_event = OfficeHours(
    id=404,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Sample",
    location_description="Sample",
    start_time=datetime.now(),
    end_time=datetime.now(),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)
