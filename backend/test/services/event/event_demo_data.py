"""Contains mock data for the live demo of the evnts feature."""

import pytest
from sqlalchemy.orm import Session
from ....entities.event_entity import EventEntity
from ..organization.organization_demo_data import cads, cssg, hacknc

import datetime

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Helper functions to create sample dates based on the
# current day


def date_maker(days_in_future: int, hour: int, minutes: int) -> datetime.datetime:
    """
    Creates a new `datetime` object relative to the current day when the
    data is reset using a reset script.

    Parameters:
        days_in_future (int): Number of days in the future from the current day to set the date
        hour (int): Which hour of the day to set the `datetime`, using the 24 hour clock
        minutes (int): Which minute to set the `datetime`

    Returns:
        datetime: `datetime` object to use in events test data.
    """
    # Find the date and time at the moment the script is run
    now = datetime.datetime.now()
    # Set the date and time to 12:00AM of that day
    current_day = datetime.datetime(now.year, now.month, now.day)
    # Create a delta containing the offset for which to move the current date
    timedelta = datetime.timedelta(days=days_in_future, hours=hour, minutes=minutes)
    # Create the new date object offset by `timedelta`
    new_date = current_day + timedelta
    # Returns the new date
    return new_date


# Sample Data Objects
# These sample entities will be used to generate the demo data.

event_one = EventEntity(
    name="Carolina Data Challenge",
    time=date_maker(days_in_future=1, hour=10, minutes=0),
    endTime=date_maker(days_in_future=1, hour=11, minutes=0),
    location="Sitterson Hall",
    description="Mark your calendars for the 2023 Carolina Data Challenge (CDC)! CDC is UNC's weekend-long datathon that brings together hundreds of participants from across campus, numerous corporate sponsors, tons of free food as well as merch, and hundreds of dollars of prizes!",
    public=True,
    organization_id=cads.id,
)

event_two = EventEntity(
    name="CS+SG Workshop",
    time=date_maker(days_in_future=2, hour=19, minutes=0),
    endTime=date_maker(days_in_future=2, hour=20, minutes=0),
    location="SN 014",
    description="This is a sample description.",
    public=True,
    organization_id=cssg.id,
)

event_three = EventEntity(
    name="HackNC Hackathon",
    time=date_maker(days_in_future=10, hour=10, minutes=0),
    endTime=date_maker(days_in_future=10, hour=11, minutes=0),
    location="Fetzer Gym",
    description="HackNC is a weekend for students of all skill levels to broaden their talents. Your challenge is to make an awesome project in just 24 hours. You will have access to hands-on tech workshops, sponsor networking, as well as exciting talks about the awesome things happening right now with computer science and technology - not to mention all of the free food, shirts, stickers, and swag! We are the largest hackathon in the southeastern United States.",
    public=True,
    organization_id=hacknc.id,
)

event_four = EventEntity(
    name="Intro to Web Scraping Workshop",
    time=date_maker(days_in_future=12, hour=19, minutes=0),
    endTime=date_maker(days_in_future=12, hour=20, minutes=0),
    location="FB 009",
    description="If you are interested in web scraping, come out to learn!",
    public=True,
    organization_id=cads.id,
)

events = [event_one, event_two, event_three, event_four]

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
