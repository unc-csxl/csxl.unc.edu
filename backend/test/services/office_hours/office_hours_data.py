"""Course data for Office Hours."""

import time
import pytest
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.entities.office_hours import user_created_tickets_table
from backend.entities.office_hours.event_entity import OfficeHoursEventEntity
from backend.entities.office_hours.section_entity import OfficeHoursSectionEntity
from backend.entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from backend.models.office_hours.event import OfficeHoursEvent, OfficeHoursEventPartial

from backend.models.office_hours.section import (
    OfficeHoursSection,
    OfficeHoursSectionPartial,
)
from backend.models.office_hours.ticket import OfficeHoursTicket
from backend.models.office_hours.ticket_type import TicketType
from backend.models.office_hours.ticket_state import TicketState
from backend.models.office_hours.event_type import OfficeHoursEventType
from backend.models.room import RoomPartial
from backend.test.services.coworking.time import *
from ..academics import section_data


__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
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
    oh_section=OfficeHoursSectionPartial(id=1),
    room=RoomPartial(id="SN156"),
    type=OfficeHoursEventType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now(),
    end_time=datetime.now(),
)

comp_110_oh_event_2 = OfficeHoursEvent(
    id=2,
    oh_section=OfficeHoursSectionPartial(id=1),
    room=RoomPartial(id="SN156"),
    type=OfficeHoursEventType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now(),
    end_time=datetime.now(),
)

comp_110_oh_events = [comp_110_oh_event_1, comp_110_oh_event_2]

# Ticket For An Event
pending_ticket = OfficeHoursTicket(
    id=1,
    oh_event=OfficeHoursEventPartial(id=1),
    description="I need help",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.QUEUED,
    created_at=datetime.now(),
)

called_ticket = OfficeHoursTicket(
    id=2,
    oh_event=OfficeHoursEventPartial(id=1),
    description="I cannot debug this.",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CALLED,
    created_at=datetime.now(),
)

closed_ticket = OfficeHoursTicket(
    id=3,
    oh_event=OfficeHoursEventPartial(id=1),
    description="Help me with Wordle.",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now(),
    caller_id=section_data.comp110_uta.id,
    closed_at=datetime.now(),
    have_concerns=False,
    caller_notes="Forgot to Return Function.",
)


cancelled_ticket = OfficeHoursTicket(
    id=4,
    oh_event=OfficeHoursEventPartial(id=1),
    description="I need help",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CANCELED,
    created_at=datetime.now(),
)

comp110_tickets = [pending_ticket, called_ticket, closed_ticket, cancelled_ticket]


def insert_fake_data(session: Session):

    # Add Office Hours Sections
    for oh_section in oh_sections:
        entity = OfficeHoursSectionEntity.from_model(oh_section)
        session.add(entity)

    # Add Office Hours Event
    for event in comp_110_oh_events:
        event_entity = OfficeHoursEventEntity.from_model(event)
        session.add(event_entity)

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


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
