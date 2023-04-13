import pytest

from sqlalchemy.orm import Session
from ...models import EventSummary, Organization
from ...services import EventService, OrganizationService
import datetime

event1_updated = EventSummary(
    id=1, 
    name="HackNC", 
    time=datetime.datetime.fromtimestamp(1680110861), 
    location="Rams Gym", 
    description="HackNC is an annual, student-run hackathon hosted by the University of North Carolina at Chapel Hill.", 
    public=True, 
    org_id=12,
    )

event1 = EventSummary(
    name="HackNC", 
    time=datetime.datetime.fromtimestamp(1680110861), 
    location="Fetzer Gym", 
    description="HackNC is an annual, student-run hackathon hosted by the University of North Carolina at Chapel Hill.", 
    public=True, 
    org_id=1,
    )

event2 = EventSummary(
    name="CS+Social Good", 
    time=datetime.datetime.fromtimestamp(1880110861), 
    location="Sitterson", 
    description="Club meeting", 
    public=True, 
    org_id=2,
    )

event3 = EventSummary(
    name="HackNC", 
    time=datetime.datetime.fromtimestamp(1880110861), 
    location="Sitterson", 
    description="Club meeting", 
    public=True, 
    org_id=1,
    )

org1 = Organization(
    name="test", 
    logo="logo", 
    short_description="description", 
    long_description="description", 
    website="website", 
    email="email", 
    instagram="instagram", 
    linked_in="linkedin", 
    youtube="youtube", 
    heel_life="heellife")

org2 = Organization(
    name="test", 
    logo="logo", 
    short_description="description", 
    long_description="description", 
    website="website", 
    email="email", 
    instagram="instagram", 
    linked_in="linkedin", 
    youtube="youtube", 
    heel_life="heellife")

@pytest.fixture()
def event_service(test_session: Session):
    return EventService(test_session)

@pytest.fixture()
def organization(test_session: Session):
    return OrganizationService(test_session)

def test_no_events(event_service: EventService):
    assert len(event_service.all()) is 0

def test_create_event_and_get_by_id(event_service: EventService, organization: OrganizationService):
    organization.create(org1)
    event = event_service.create(event1)
    assert event_service.get_from_id(1).id == event.id

def test_get_all_events(event_service: EventService, organization: OrganizationService):
    organization.create(org1)
    organization.create(org2)
    event_service.create(event1)
    assert len(event_service.all()) is 1
    event_service.create(event2)
    assert len(event_service.all()) is 2
    assert event_service.all()[1].id is 2

def test_get_by_org_id(event_service: EventService, organization: OrganizationService):
    organization.create(org1)
    event_service.create(event1)
    event_service.create(event3)
    assert len(event_service.get_from_org_id(1)) == 2

def test_get_from_time_range(event_service: EventService, organization: OrganizationService):
    organization.create(org1)
    organization.create(org2)
    event_service.create(event1)
    event_service.create(event2)
    event_from_range1 = event_service.get_from_time_range(datetime.datetime.fromtimestamp(1680110860),datetime.datetime.fromtimestamp(1680110862))
    event_from_range2 = event_service.get_from_time_range(datetime.datetime.fromtimestamp(1880110860),datetime.datetime.fromtimestamp(1880110862))
    assert len(event_from_range1) == 1
    assert len(event_from_range2) == 1


def test_delete(event_service: EventService, organization: OrganizationService):
    organization.create(org1)
    event_service.create(event1)
    assert len(event_service.all()) is 1
    event_service.delete(1)
    assert len(event_service.all()) is 0


def test_update(event_service: EventService, organization: OrganizationService):
    organization.create(org1)
    event = event_service.create(event1)
    assert event_service.get_from_id(1).location == event.location
    new_event = event_service.update(event1_updated)
    assert event_service.get_from_id(1).location == new_event.location == event1_updated.location