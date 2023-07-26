"""Mock data for events."""

import pytest
import datetime
from sqlalchemy.orm import Session
from ...models.event import Event
from ...entities.event_entity import EventEntity

from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

cads_event = Event(
    id=1,
    name="Carolina Data Challenge",
    time=datetime.datetime.fromtimestamp(1680110861),
    location="Carolina Union",
    description="Datathon!",
    public=True,
    org_id=1,
)

cssg_event = Event(
    id=2,
    name="CS+Social Good",
    time=datetime.datetime.fromtimestamp(1880110861),
    location="Sitterson",
    description="Club meeting",
    public=True,
    org_id=2,
)

events = [cads_event, cssg_event]

to_add = EventEntity(
    id=3,
    name="CS+Social Good New Event",
    time=datetime.datetime.fromtimestamp(1880110865),
    location="Sitterson",
    description="Club meeting",
    public=True,
    org_id=2,
)

new_cads = Event(
    id=1,
    name="Carolina Data Challenge",
    time=datetime.datetime.fromtimestamp(1680110861),
    location="Geonome Science Building",
    description="Datathon!",
    public=True,
    org_id=1,
)

time_range = (
    datetime.datetime.fromtimestamp(1680110860),
    datetime.datetime.fromtimestamp(1680110862),
)


# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake event data into the test session."""

    global events

    # Create entities for test event data
    entities = []
    for event in events:
        entity = EventEntity.from_model(event)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, EventEntity, EventEntity.id, len(events) + 1)

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
