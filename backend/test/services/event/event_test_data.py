"""Contains mock data for the live demo of the evnts feature."""

import pytest
from sqlalchemy.orm import Session

from ....models.public_user import PublicUser
from ....models.event import EventDraft, EventOverview
from ....models.event_registration import NewEventRegistration
from ....models.registration_type import RegistrationType
from ....entities.event_entity import EventEntity
from ....entities.event_registration_entity import EventRegistrationEntity
from .event_demo_data import date_maker
from ..organization.organization_test_data import cads, cssg
from ..user_data import root, ambassador, user
from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects
# These sample entities will be used to generate the test data.

event_one = EventDraft(
    id=1,
    name="CS+SG Mixer",
    start=date_maker(days_in_future=1, hour=10, minutes=0),
    end=date_maker(days_in_future=1, hour=11, minutes=0),
    location="Sitterson Hall Lower Lobby",
    description="Mark your calendars for the 2023 Carolina Data Challenge (CDC)! CDC is UNC's weekend-long datathon that brings together hundreds of participants from across campus, numerous corporate sponsors, tons of free food as well as merch, and hundreds of dollars of prizes!",
    registration_limit=50,
    organization_slug=cssg.slug,
)

event_two = EventDraft(
    id=2,
    name="CS+SG Workshop",
    start=date_maker(days_in_future=2, hour=19, minutes=0),
    end=date_maker(days_in_future=2, hour=20, minutes=0),
    location="SN 014",
    description="This is a sample description.",
    public=True,
    registration_limit=50,
    organization_slug=cssg.slug,
)

event_three = EventDraft(
    id=3,
    name="Super Exclusive Meeting",
    start=date_maker(days_in_future=2, hour=19, minutes=0),
    end=date_maker(days_in_future=2, hour=20, minutes=0),
    location="SN 014",
    description="This is a sample description.",
    public=True,
    registration_limit=1,
    organization_slug=cssg.slug,
)

events = [event_one, event_two, event_three]
event_organization = {event_one: cssg, event_two: cssg, event_three: cssg}

to_add = EventDraft(
    name="Carolina Data Challenge",
    start=date_maker(days_in_future=2, hour=20, minutes=0),
    end=date_maker(days_in_future=2, hour=21, minutes=0),
    location="SN011",
    description="This is a sample description.",
    public=True,
    registration_limit=50,
    organization_slug=cads.slug,
    organizers=[
        PublicUser(
            id=root.id,
            onyen=root.onyen,
            first_name=root.first_name,
            last_name=root.last_name,
            pronouns=root.pronouns,
            email=root.email,
            linkedin=root.linkedin,
            website=root.website,
        )
    ],
)

invalid_event = EventDraft(
    id=4,
    name="Frontend Debugging Workshop",
    start=date_maker(days_in_future=1, hour=10, minutes=0),
    end=date_maker(days_in_future=1, hour=11, minutes=0),
    location="SN156",
    description="This is a sample description.",
    public=True,
    registration_limit=50,
    organization_slug=cssg.slug,
)

updated_event_one = EventDraft(
    id=1,
    name="Carolina Data Challenge",
    start=date_maker(days_in_future=1, hour=10, minutes=0),
    end=date_maker(days_in_future=1, hour=11, minutes=0),
    location="Fetzer Gym",
    description="Mark your calendars for the 2023 Carolina Data Challenge (CDC)! CDC is UNC's weekend-long datathon that brings together hundreds of participants from across campus, numerous corporate sponsors, tons of free food as well as merch, and hundreds of dollars of prizes!",
    public=True,
    registration_limit=50,
    organization_slug=cssg.slug,
    organizers=[
        PublicUser(
            id=user.id,
            onyen=user.onyen,
            first_name=user.first_name,
            last_name=user.last_name,
            pronouns=user.pronouns,
            email=user.email,
            linkedin=user.linkedin,
            website=user.website,
        ),
    ],
)

updated_event_one_organizers = EventDraft(
    id=1,
    name="Carolina Data Challenge",
    start=date_maker(days_in_future=1, hour=10, minutes=0),
    end=date_maker(days_in_future=1, hour=11, minutes=0),
    location="Fetzer Gym",
    description="Mark your calendars for the 2023 Carolina Data Challenge (CDC)! CDC is UNC's weekend-long datathon that brings together hundreds of participants from across campus, numerous corporate sponsors, tons of free food as well as merch, and hundreds of dollars of prizes!",
    public=True,
    registration_limit=50,
    organization_slug=cssg.slug,
    organizers=[
        PublicUser(
            id=user.id,
            onyen=user.onyen,
            first_name=user.first_name,
            last_name=user.last_name,
            pronouns=user.pronouns,
            email=user.email,
            linkedin=user.linkedin,
            website=user.website,
        ),
        PublicUser(
            id=ambassador.id,
            onyen=ambassador.onyen,
            first_name=ambassador.first_name,
            last_name=ambassador.last_name,
            pronouns=ambassador.pronouns,
            email=ambassador.email,
            linkedin=ambassador.linkedin,
            website=ambassador.website,
        ),
    ],
)

updated_event_two = EventDraft(
    id=2,
    name="CS+SG Workshop",
    start=date_maker(days_in_future=2, hour=19, minutes=0),
    end=date_maker(days_in_future=2, hour=20, minutes=0),
    location="SN 014",
    description="Come join us for a new workshop!",
    public=True,
    registration_limit=50,
    organization_slug=cssg.slug,
)

updated_event_three = EventDraft(
    id=3,
    name="Super Exclusive Meeting",
    start=date_maker(days_in_future=2, hour=19, minutes=0),
    end=date_maker(days_in_future=2, hour=20, minutes=0),
    location="SN 014",
    description="This is a sample description.",
    public=True,
    registration_limit=1,
    organization_slug=cssg.slug,
    organizers=[
        PublicUser(
            id=user.id,
            onyen=user.onyen,
            first_name=user.first_name,
            last_name=user.last_name,
            pronouns=user.pronouns,
            email=user.email,
            linkedin=user.linkedin,
            website=user.website,
        ),
        PublicUser(
            id=ambassador.id,
            onyen=user.onyen,
            first_name=ambassador.first_name,
            last_name=ambassador.last_name,
            pronouns=ambassador.pronouns,
            email=ambassador.email,
            linkedin=ambassador.linkedin,
            website=ambassador.website,
        ),
        PublicUser(
            id=root.id,
            onyen=user.onyen,
            first_name=root.first_name,
            last_name=root.last_name,
            pronouns=root.pronouns,
            email=root.email,
            linkedin=root.linkedin,
            website=root.website,
        ),
    ],
)

updated_event_three_remove_organizers = EventDraft(
    id=3,
    name="Super Exclusive Meeting",
    start=date_maker(days_in_future=2, hour=19, minutes=0),
    end=date_maker(days_in_future=2, hour=20, minutes=0),
    location="SN 014",
    description="This is a sample description.",
    public=True,
    registration_limit=1,
    organization_slug=cssg.slug,
    organizers=[
        PublicUser(
            id=user.id,
            onyen=user.onyen,
            first_name=user.first_name,
            last_name=user.last_name,
            pronouns=user.pronouns,
            email=user.email,
            linkedin=user.linkedin,
            website=user.website,
        ),
    ],
)


registration = NewEventRegistration(
    event_id=event_one.id,
    user_id=ambassador.id,
    registration_type=RegistrationType.ATTENDEE,
)

organizer_registration = NewEventRegistration(
    event_id=event_one.id,
    user_id=user.id,
    registration_type=RegistrationType.ORGANIZER,
)

registration_for_event_three = NewEventRegistration(
    event_id=event_three.id,
    user_id=ambassador.id,
    registration_type=RegistrationType.ATTENDEE,
)
registrations = [registration, organizer_registration, registration_for_event_three]

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake event data into the test session."""

    global events

    # Create entities for test event data
    entities = []
    for event in events:
        event_entity = EventEntity.from_draft_model(event, event_organization[event].id)
        session.add(event_entity)
        entities.append(event_entity)

    session.commit()

    for registration in registrations:
        registration_entity = EventRegistrationEntity.from_new_model(registration)
        session.add(registration_entity)

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
