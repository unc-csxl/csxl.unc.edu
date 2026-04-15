from dataclasses import dataclass
import datetime

from sqlalchemy.orm import Session

from ....entities.event_entity import EventEntity
from ....entities.event_registration_entity import EventRegistrationEntity
from ....models.event import EventDraft
from ....models.event_registration import NewEventRegistration
from ....models.public_user import PublicUser
from ....models.registration_type import RegistrationType
from ..auth_scenario import AuthScenario, arrange_auth_scenario
from ..organization.scenario import OrganizationScenario, arrange_organization_scenario
from ..reset_table_id_seq import reset_table_id_seq


def date_maker(days_in_future: int, hour: int, minutes: int) -> datetime.datetime:
    now = datetime.datetime.now()
    current_day = datetime.datetime(now.year, now.month, now.day)
    return current_day + datetime.timedelta(
        days=days_in_future, hours=hour, minutes=minutes
    )


def public_user(user) -> PublicUser:
    return PublicUser(
        id=user.id,
        onyen=user.onyen,
        first_name=user.first_name,
        last_name=user.last_name,
        pronouns=user.pronouns,
        email=user.email,
        linkedin=user.linkedin,
        website=user.website,
    )


@dataclass(frozen=True)
class EventScenario:
    auth: AuthScenario
    organizations: OrganizationScenario
    event_one: EventDraft
    event_two: EventDraft
    event_three: EventDraft
    to_add: EventDraft
    invalid_event: EventDraft
    updated_event_one: EventDraft
    updated_event_one_organizers: EventDraft
    updated_event_two: EventDraft
    updated_event_three: EventDraft
    updated_event_three_remove_organizers: EventDraft
    registration: NewEventRegistration
    organizer_registration: NewEventRegistration
    registration_for_event_three: NewEventRegistration

    @property
    def events(self) -> list[EventDraft]:
        return [self.event_one, self.event_two, self.event_three]

    @property
    def registrations(self) -> list[NewEventRegistration]:
        return [
            self.registration,
            self.organizer_registration,
            self.registration_for_event_three,
        ]


def build_event_scenario(
    auth: AuthScenario, organizations: OrganizationScenario
) -> EventScenario:
    event_one = EventDraft(
        id=1,
        name="CS+SG Mixer",
        start=date_maker(days_in_future=1, hour=10, minutes=0),
        end=date_maker(days_in_future=1, hour=11, minutes=0),
        location="Sitterson Hall Lower Lobby",
        description="Mark your calendars for the 2023 Carolina Data Challenge (CDC)! CDC is UNC's weekend-long datathon that brings together hundreds of participants from across campus, numerous corporate sponsors, tons of free food as well as merch, and hundreds of dollars of prizes!",
        registration_limit=50,
        organization_slug=organizations.cssg.slug,
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
        organization_slug=organizations.cssg.slug,
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
        organization_slug=organizations.cssg.slug,
    )
    to_add = EventDraft(
        name="Carolina Data Challenge",
        start=date_maker(days_in_future=2, hour=20, minutes=0),
        end=date_maker(days_in_future=2, hour=21, minutes=0),
        location="SN011",
        description="This is a sample description.",
        public=True,
        registration_limit=50,
        organization_slug=organizations.cads.slug,
        organizers=[public_user(auth.root)],
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
        organization_slug=organizations.cssg.slug,
    )
    updated_event_one = EventDraft(
        id=1,
        name="Carolina Data Challenge",
        start=date_maker(days_in_future=1, hour=10, minutes=0),
        end=date_maker(days_in_future=1, hour=11, minutes=0),
        location="Fetzer Gym",
        description=event_one.description,
        public=True,
        registration_limit=50,
        organization_slug=organizations.cssg.slug,
        organizers=[public_user(auth.user)],
    )
    updated_event_one_organizers = EventDraft(
        id=1,
        name="Carolina Data Challenge",
        start=date_maker(days_in_future=1, hour=10, minutes=0),
        end=date_maker(days_in_future=1, hour=11, minutes=0),
        location="Fetzer Gym",
        description=event_one.description,
        public=True,
        registration_limit=50,
        organization_slug=organizations.cssg.slug,
        organizers=[public_user(auth.user), public_user(auth.ambassador)],
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
        organization_slug=organizations.cssg.slug,
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
        organization_slug=organizations.cssg.slug,
        organizers=[
            public_user(auth.user),
            public_user(auth.ambassador),
            public_user(auth.root),
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
        organization_slug=organizations.cssg.slug,
        organizers=[public_user(auth.user)],
    )
    registration = NewEventRegistration(
        event_id=event_one.id,
        user_id=auth.ambassador.id,
        registration_type=RegistrationType.ATTENDEE,
    )
    organizer_registration = NewEventRegistration(
        event_id=event_one.id,
        user_id=auth.user.id,
        registration_type=RegistrationType.ORGANIZER,
    )
    registration_for_event_three = NewEventRegistration(
        event_id=event_three.id,
        user_id=auth.ambassador.id,
        registration_type=RegistrationType.ATTENDEE,
    )

    return EventScenario(
        auth=auth,
        organizations=organizations,
        event_one=event_one,
        event_two=event_two,
        event_three=event_three,
        to_add=to_add,
        invalid_event=invalid_event,
        updated_event_one=updated_event_one,
        updated_event_one_organizers=updated_event_one_organizers,
        updated_event_two=updated_event_two,
        updated_event_three=updated_event_three,
        updated_event_three_remove_organizers=updated_event_three_remove_organizers,
        registration=registration,
        organizer_registration=organizer_registration,
        registration_for_event_three=registration_for_event_three,
    )


def arrange_event_scenario(session: Session) -> EventScenario:
    auth = arrange_auth_scenario(session)
    organizations = arrange_organization_scenario(session)
    scenario = build_event_scenario(auth, organizations)
    organizations_by_slug = {
        organization.slug: organization.id
        for organization in organizations.organizations
    }

    for event in scenario.events:
        session.add(
            EventEntity.from_draft_model(
                event, organizations_by_slug[event.organization_slug]
            )
        )

    session.commit()

    for registration in scenario.registrations:
        session.add(EventRegistrationEntity.from_new_model(registration))

    reset_table_id_seq(session, EventEntity, EventEntity.id, len(scenario.events) + 1)
    session.commit()
    return scenario
