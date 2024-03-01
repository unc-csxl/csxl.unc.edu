"""Course data for Office Hours."""

import time
import pytest
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.entities.office_hours import user_created_tickets_table
from backend.entities.office_hours.oh_event_entity import OfficeHoursEventEntity
from backend.entities.office_hours.oh_section_entity import OfficeHoursSectionEntity
from backend.entities.office_hours.oh_ticket_entity import OfficeHoursTicketEntity
from backend.models.office_hours.oh_event import OfficeHoursEvent

from backend.models.office_hours.oh_section import OfficeHoursSection
from backend.models.office_hours.oh_ticket import OfficeHoursTicket
from backend.models.office_hours.ticket_type import TicketType
from backend.models.office_hours.ticket_state import TicketState
from backend.models.office_hours.oh_type import OfficeHoursType
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
    office_hours_section_id=1,
    room_id="SN156",
    type=OfficeHoursType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now(),
    end_time=datetime.now(),
)

comp_110_oh_event_2 = OfficeHoursEvent(
    id=2,
    office_hours_section_id=1,
    room_id="SN156",
    type=OfficeHoursType.OFFICE_HOURS,
    description="Office Hours",
    location_description="In Person",
    event_date=date.today(),
    start_time=datetime.now(),
    end_time=datetime.now(),
)

comp_110_oh_events = [comp_110_oh_event_1, comp_110_oh_event_2]

# Ticket For An Event
pending_ticket = OfficeHoursTicket(
    office_hours_event_id=1,
    description="I need help",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.PENDING,
    created_at=datetime.now(),
)

called_ticket = OfficeHoursTicket(
    office_hours_event_id=1,
    description="I cannot debug this.",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CALLED,
    created_at=datetime.now(),
    caller_id=section_data.comp110_uta.id,
)

closed_ticket = OfficeHoursTicket(
    office_hours_event_id=1,
    description="Help me with Wordle.",
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now(),
    caller_id=section_data.comp110_uta.id,
    closed_at=datetime.now(),
    have_concerns=False,
    caller_notes="Forgot to Return Function.",
)

comp110_tickets = [pending_ticket, called_ticket, closed_ticket]


def insert_fake_data(session: Session):
    for oh_section in oh_sections:
        entity = OfficeHoursSectionEntity.from_model(oh_section)
        session.add(entity)

    for event in comp_110_oh_events:
        event_entity = OfficeHoursEventEntity.from_model(event)
        session.add(event_entity)

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


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
