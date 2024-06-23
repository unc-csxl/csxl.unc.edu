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


from ....models.office_hours.office_hours import OfficeHours
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.course_site import CourseSite
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

# Sections
comp_110_sections = (
    [
        section_data.comp_110_001_current_term,
        section_data.comp_110_002_current_term,
    ],
    comp_110_site.id,
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
sites = [comp_110_site]
section_pairings = [comp_110_sections]

office_hours = [
    comp_110_current_office_hours,
    comp_110_future_office_hours,
    comp_110_past_office_hours,
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

    for oh in office_hours:
        office_hours_entity = OfficeHoursEntity.from_model(oh)
        session.add(office_hours_entity)

    reset_table_id_seq(
        session,
        OfficeHoursEntity,
        OfficeHoursEntity.id,
        len(office_hours) + 1,
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
