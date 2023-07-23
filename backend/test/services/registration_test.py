import pytest

from sqlalchemy.orm import Session
from ...models import Registration, UserDetails, Event, OrganizationDetail
from ...services import RegistrationService, UserService, EventService, OrganizationService
import datetime

# Mock Models
registration1 = Registration( 
    user_id=1, 
    event_id=1, 
    status=0
    )
registration2 = Registration(
    user_id=1, 
    event_id=2, 
    status=0
    )
registration_updated = Registration( 
    user_id=1, 
    event_id=1, 
    status=1
    )
root = UserDetails(pid=999999999, onyen='root', first_name="Super", last_name="User",
             email="root@cs.unc.edu", pronouns="they / them")
event1 = Event(
    name="HackNC", 
    time=datetime.datetime.fromtimestamp(1680110861), 
    location="Fetzer Gym", 
    description="HackNC is an annual, student-run hackathon hosted by the University of North Carolina at Chapel Hill.", 
    public=True, 
    org_id=1,
    )
event2 = Event(
    name="CS+Social Good", 
    time=datetime.datetime.fromtimestamp(1880110861), 
    location="Sitterson", 
    description="Club meeting", 
    public=True, 
    org_id=1,
    )

event3 = Event(
    name="HackNC", 
    time=datetime.datetime.fromtimestamp(1880110861), 
    location="Sitterson", 
    description="Club meeting", 
    public=True, 
    org_id=1,
    )

org1 = OrganizationDetail(
    name="test", 
    slug="HackNC",
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
def registration(test_session: Session):
    return RegistrationService(test_session)

@pytest.fixture()
def user_service(test_session: Session):
    return UserService(test_session)

@pytest.fixture()
def event_service(test_session: Session):
    return EventService(test_session)

@pytest.fixture()
def org_service(test_session: Session):
    return OrganizationService(test_session)

def test_no_registrations(registration: RegistrationService):
    """Tests that the test session initially contains no registrations"""
    assert len(registration.all()) is 0

def test_get_all_registrations(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests creating a new registration and checks that it was added to table successfully"""
    # user_service.create(root)
    org_service.create(root, org1)
    event_service.create(event1)
    event_service.create(event2)
    registration.create(registration1)
    assert len(registration.all()) is 1
    registration.create(registration2)
    assert len(registration.all()) is 2
    assert registration.all()[1].id is 2

def test_create_registration_and_get_by_user(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests that a newly added can be retrieved using the get_by_user() method"""
    # user_service.create(root)
    org_service.create(org1)
    event_service.create(event1)
    reg = registration.create(registration1)
    assert registration.get_by_user(1,0)[0].status == reg.status == 0

def test_get_all_registrations(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests creating two registrations and tests that the all() method retrieves both"""
    # user_service.create(root)
    org_service.create(org1)
    event_service.create(event1)
    event_service.create(event2)
    registration.create(registration1)
    assert len(registration.all()) is 1
    registration.create(registration2)
    assert len(registration.all()) is 2
    assert registration.all()[1].id is 2

def test_get_by_event(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests that you can retrive a registration by its event id using get_by_event()"""
    user_service.create(root)
    org_service.create(org1)
    event_service.create(event1)
    reg = registration.create(registration1)
    assert registration.get_by_event(1,0)[0].status == reg.status == 0

def test_delete_registration(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests that all() returns one less registration after calling delete_registration()"""
    user_service.create(root)
    org_service.create(org1)
    event_service.create(event1)
    registration.create(registration1)
    assert len(registration.all()) is 1
    registration.delete_registration(1)
    assert len(registration.all()) is 0

def test_clear_registrations(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests that calling clear_registration() will clear our multiple registrations"""
    user_service.create(root)
    org_service.create(org1)
    event_service.create(event1)
    event_service.create(event2)
    registration.create(registration1)
    registration.create(registration2)
    assert len(registration.all()) is 2
    registration.clear_registrations(1)
    registration.clear_registrations(2)
    assert len(registration.all()) is 0

def test_update_status(registration: RegistrationService, user_service: UserService, event_service: EventService, org_service: OrganizationService):
    """Tests that a registration can be updated after it is created using update_status()"""
    user_service.create(root)
    org_service.create(org1)
    event_service.create(event1)
    reg = registration.create(registration1)
    assert registration.get_by_user(1,0)[0].status == 0
    registration.update_status(reg)
    assert registration.get_by_user(1,1)[0].status == 1