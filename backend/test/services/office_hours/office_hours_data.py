"""Test Data for Office Hours."""

import pytest
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

from ....entities.academics.section_entity import SectionEntity
from ...services.reset_table_id_seq import reset_table_id_seq

from ..academics import section_data

from ....entities.office_hours import user_created_tickets_table
from ....entities.office_hours.event_entity import OfficeHoursEventEntity
from ....entities.office_hours.section_entity import OfficeHoursSectionEntity
from ....entities.office_hours.ticket_entity import OfficeHoursTicketEntity

from ....models.office_hours.event import OfficeHoursEvent, OfficeHoursEventPartial
from ....models.office_hours.event_type import OfficeHoursEventType
from ....models.office_hours.section import (
    OfficeHoursSection,
)
from ....models.office_hours.ticket import OfficeHoursTicket
from ....models.office_hours.ticket_type import TicketType
from ....models.office_hours.ticket_state import TicketState
from ....models.room import Room


__authors__ = ["Madelyn Andrews", "Sadie Amato", "Bailey DeSouza", "Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Office Hours Section Data
comp_110_oh_section = OfficeHoursSection(
    id=1, title="COMP 110: Introduction to Programming"
)

comp_523_oh_section = OfficeHoursSection(
    id=2, title="COMP 523: Software Engineering Lab"
)

oh_sections = [comp_110_oh_section, comp_523_oh_section]

# Office Hours Event Data
comp_110_oh_event_1 = OfficeHoursEvent(
    id=1,
    oh_section=comp_110_oh_section,
    room=Room(id="SN156"),
    type=OfficeHoursEventType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now() - timedelta(hours=1),
    end_time=datetime.now() + timedelta(hours=1),
)

comp_110_oh_event_2 = OfficeHoursEvent(
    id=2,
    oh_section=comp_110_oh_section,
    room=Room(id="SN156"),
    type=OfficeHoursEventType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
)

comp_110_oh_event_3 = OfficeHoursEvent(
    id=3,
    oh_section=comp_110_oh_section,
    room=Room(id="SN156"),
    type=OfficeHoursEventType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now() - timedelta(days=1, hours=3),
    end_time=datetime.now() - timedelta(days=1),
)

comp_110_oh_events = [comp_110_oh_event_1, comp_110_oh_event_2, comp_110_oh_event_3]

# Ticket For An Event
pending_ticket = OfficeHoursTicket(
    id=1,
    oh_event=comp_110_oh_event_1,
    description="Assignment Part: ex04\nGoal: finishing up wordle!\nConcepts: reading Gradescope errors\nTried: I tried submitting what I thought was right based on my tests",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.QUEUED,
    created_at=datetime.now(),
)

called_ticket = OfficeHoursTicket(
    id=2,
    oh_event=comp_110_oh_event_1,
    description="Assignment Part: ex04\nGoal: finishing up wordle!\nConcepts: reading Gradescope errors\nTried: I tried submitting what I thought was right based on my tests",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CALLED,
    created_at=datetime.now() - timedelta(minutes=2),
)

closed_ticket = OfficeHoursTicket(
    id=3,
    oh_event=comp_110_oh_event_1,
    description="Assignment Part: ex04 Wordle \nGoal: I'm running into an infinite loop. My game will never end. \nConcepts: Loops and input function. \nTried: I tried using Trailhead to debug my function call but it is also stuck in an infitnite loop.",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=10),
    caller_id=section_data.comp110_uta.id,
    closed_at=datetime.now() - timedelta(minutes=1),
    have_concerns=False,
    caller_notes="Forgot to Return Function.",
)


cancelled_ticket = OfficeHoursTicket(
    id=4,
    oh_event=comp_110_oh_event_1,
    description="Assignment Part: ex04\nGoal: finishing up wordle!\nConcepts: reading Gradescope errors\nTried: I tried submitting what I thought was right based on my tests",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CANCELED,
    created_at=datetime.now() - timedelta(minutes=5),
)

comp110_tickets = [pending_ticket, called_ticket, closed_ticket, cancelled_ticket]


def insert_fake_data(session: Session):

    # Add Office Hours Sections
    for oh_section in oh_sections:
        entity = OfficeHoursSectionEntity.from_model(model=oh_section)
        session.add(entity)

    reset_table_id_seq(
        session,
        OfficeHoursSectionEntity,
        OfficeHoursSectionEntity.id,
        len(oh_sections) + 1,
    )

    # Associate Office Hours Section with Academic Section
    for comp_110_section in section_data.comp_110_sections:
        section = session.get(SectionEntity, comp_110_section.id)
        section.office_hours_id = comp_110_oh_section.id

    # Add Office Hours Event
    for event in comp_110_oh_events:
        event_entity = OfficeHoursEventEntity.from_model(event)
        session.add(event_entity)

    reset_table_id_seq(
        session,
        OfficeHoursEventEntity,
        OfficeHoursEventEntity.id,
        len(comp_110_oh_events) + 1,
    )

    # Add User Created Tickets
    for ticket in comp110_tickets:
        ticket_entity = OfficeHoursTicketEntity.from_model(ticket)
        session.add(ticket_entity)
        session.commit()

        # Associate with Ticket and User Create Tickets
        session.execute(
            user_created_tickets_table.insert().values(
                {
                    "ticket_id": ticket_entity.id,
                    "member_id": section_data.comp110_student.id,
                }
            )
        )

    # Update when Caller/UTA calls a ticket - Called and Closed Ticket Would have caller!
    session.query(OfficeHoursTicketEntity).filter(
        OfficeHoursTicketEntity.id.in_([called_ticket.id, closed_ticket.id])
    ).update({"caller_id": section_data.comp110_uta.id})

    reset_table_id_seq(
        session,
        OfficeHoursTicketEntity,
        OfficeHoursTicketEntity.id,
        len(comp110_tickets) + 1,
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
