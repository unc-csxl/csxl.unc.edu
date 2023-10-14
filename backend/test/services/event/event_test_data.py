"""Contains mock data for the live demo of the evnts feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.event import Event
from ....entities.event_entity import EventEntity
from ..organization.organization_demo_data import cads, cssg
from .event_demo_data import date_maker
import datetime

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects
# These sample entities will be used to generate the test data.

event_one = EventEntity(
    name="Carolina Data Challenge",
    time=date_maker(days_in_future=1, hour=10, minutes=0),
    location="Sitterson Hall Lower Lobby",
    description="Mark your calendars for the 2023 Carolina Data Challenge (CDC)! CDC is UNC's weekend-long datathon that brings together hundreds of participants from across campus, numerous corporate sponsors, tons of free food as well as merch, and hundreds of dollars of prizes!",
    public=True,
    organization_id=cads.id
)

event_two = EventEntity(
    name="CS+SG Workshop",
    time=date_maker(days_in_future=2, hour=19, minutes=0),
    location = "SN 014",
    description="This is a sample description.",
    public=True,
    organization_id=cssg.id
)

events = [event_one, event_two]

# Data Functions

def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global events

    # Create entities for test organization data
    entities = []
    for event_entity in events:
        session.add(event_entity)
        entities.append(event_entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, EventEntity, EventEntity.id, len(events) + 1
    )

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield