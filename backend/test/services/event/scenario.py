from dataclasses import dataclass
import datetime

from sqlalchemy.orm import Session

from ....entities.event_entity import EventEntity
from ....entities.event_registration_entity import EventRegistrationEntity
from ....entities.organization_entity import OrganizationEntity
from ....entities.permission_entity import PermissionEntity
from ....entities.role_entity import RoleEntity
from ....entities.user_entity import UserEntity
from ....entities.user_role_table import user_role_table
from ....models.event import EventDraft
from ....models.event_registration import NewEventRegistration
from ....models import Permission, Role
from ....models.organization import Organization
from ....models.public_user import PublicUser
from ....models.registration_type import RegistrationType
from ....models.user import User
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
class EventAuthScenario:
    root_role: Role
    root_permission: Permission
    root: User
    ambassador: User
    user: User


@dataclass(frozen=True)
class EventOrganizations:
    cads: Organization
    cssg: Organization

    @property
    def organizations(self) -> list[Organization]:
        return [self.cads, self.cssg]


@dataclass(frozen=True)
class EventScenario:
    auth: EventAuthScenario
    organizations: EventOrganizations
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
    auth: EventAuthScenario, organizations: EventOrganizations
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


def build_event_organizations() -> EventOrganizations:
    return EventOrganizations(
        cads=Organization(
            id=1,
            name="Carolina Analytics & Data Science Club",
            shorthand="CADS",
            slug="cads",
            logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
            short_description="Provides students interested in Data Science opportunities to grow.",
            long_description="CADS provides students interested in Data Science opportunities to grow personally, intellectually, professionally, and socially among a support network of students, professors, and career professionals.",
            website="https://carolinadata.unc.edu/",
            email="carolinadatascience@gmail.com",
            instagram="https://www.instagram.com/carolinadatascience/",
            linked_in="https://www.linkedin.com/company/carolina-data/",
            youtube="https://www.youtube.com/channel/UCO44Yjhjuo5-TLUCAaP0-cQ",
            heel_life="https://heellife.unc.edu/organization/carolinadatascience",
            public=True,
        ),
        cssg=Organization(
            id=2,
            name="CS+Social Good",
            shorthand="CSSG",
            slug="cssg",
            logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cssg.png",
            short_description="We build apps for nonprofits and organizations for social good.",
            long_description="We partner with organizations for social good and build technology solutions for their needs.",
            website="https://cssgunc.org/",
            email="cssgunc@gmail.com",
            instagram="https://www.instagram.com/unc_cssg/",
            linked_in="",
            youtube="",
            heel_life="https://heellife.unc.edu/organization/cssg",
            public=False,
        ),
    )


def build_event_auth_scenario() -> EventAuthScenario:
    return EventAuthScenario(
        root_role=Role(id=1, name="root"),
        root_permission=Permission(id=1, action="*", resource="*"),
        root=User(
            id=1,
            pid=999999999,
            onyen="root",
            email="root@unc.edu",
            first_name="Rhonda",
            last_name="Root",
            pronouns="She / Her / Hers",
            accepted_community_agreement=True,
        ),
        ambassador=User(
            id=2,
            pid=888888888,
            onyen="xlstan",
            email="amam@unc.edu",
            first_name="Amy",
            last_name="Ambassador",
            pronouns="They / Them / Theirs",
            accepted_community_agreement=True,
        ),
        user=User(
            id=3,
            pid=111111111,
            onyen="user",
            email="user@unc.edu",
            first_name="Sally",
            last_name="Student",
            pronouns="She / They",
            accepted_community_agreement=True,
        ),
    )


def arrange_event_scenario(session: Session) -> EventScenario:
    auth = build_event_auth_scenario()
    organizations = build_event_organizations()
    scenario = build_event_scenario(auth, organizations)
    session.add(RoleEntity.from_model(auth.root_role))
    session.add_all(
        [
            UserEntity.from_model(auth.root),
            UserEntity.from_model(auth.ambassador),
            UserEntity.from_model(auth.user),
        ]
    )
    session.flush()
    session.execute(
        user_role_table.insert().values(
            {"role_id": auth.root_role.id, "user_id": auth.root.id}
        )
    )
    session.add(
        PermissionEntity(
            id=auth.root_permission.id,
            role_id=auth.root_role.id,
            action=auth.root_permission.action,
            resource=auth.root_permission.resource,
        )
    )
    reset_table_id_seq(session, RoleEntity, RoleEntity.id, auth.root_role.id + 1)
    reset_table_id_seq(session, UserEntity, UserEntity.id, auth.user.id + 1)
    reset_table_id_seq(
        session,
        PermissionEntity,
        PermissionEntity.id,
        auth.root_permission.id + 1,
    )
    session.add_all(
        OrganizationEntity.from_model(organization)
        for organization in organizations.organizations
    )
    reset_table_id_seq(
        session,
        OrganizationEntity,
        OrganizationEntity.id,
        len(organizations.organizations) + 1,
    )
    session.flush()
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
