"""Explicit arrange helpers for signage service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ...entities import RoomEntity, UserEntity
from ...entities.academics.course_entity import CourseEntity
from ...entities.academics.section_entity import SectionEntity
from ...entities.academics.term_entity import TermEntity
from ...entities.article_entity import ArticleEntity, article_author_table
from ...entities.coworking import (
    OperatingHoursEntity,
    ReservationEntity,
    SeatEntity,
)
from ...entities.event_entity import EventEntity
from ...entities.office_hours.course_site_entity import CourseSiteEntity
from ...entities.office_hours.office_hours_entity import OfficeHoursEntity
from ...entities.organization_entity import OrganizationEntity
from ...models import RoomDetails, User
from ...models.academics.course import Course
from ...models.academics.section import Section
from ...models.academics.term import Term
from ...models.articles import ArticleDraft, ArticleState
from ...models.coworking import (
    OperatingHours as CoworkingOperatingHours,
    Reservation,
    ReservationState,
    SeatDetails,
)
from ...models.event import EventDraft
from ...models.office_hours.course_site import CourseSite
from ...models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ...models.office_hours.office_hours import OfficeHours
from ...models.organization import Organization
from ...models.public_user import PublicUser
from .reset_table_id_seq import reset_table_id_seq


@dataclass(frozen=True)
class SignageReservationScenario:
    root: User
    ambassador: User
    user: User
    group_a: RoomDetails
    pair_a: RoomDetails
    monitor_seat_01: SeatDetails
    monitor_seat_11: SeatDetails


@dataclass
class SignageScenario:
    reservation: SignageReservationScenario
    comp_110_current_office_hours: OfficeHours
    announcement: ArticleDraft
    article_one: ArticleDraft
    article_two: ArticleDraft


def _author(user) -> PublicUser:
    return PublicUser(
        id=user.id,
        onyen=user.onyen,
        first_name=user.first_name,
        last_name=user.last_name,
        pronouns=user.pronouns,
        email=user.email,
        github_avatar=user.github_avatar,
        github=user.github,
        bio=user.bio,
        linkedin=user.linkedin,
        website=user.website,
    )


def arrange_signage_reservation_scenario(
    session: Session, now: datetime
) -> SignageReservationScenario:
    root = User(
        id=1,
        pid=999999999,
        onyen="root",
        email="root@unc.edu",
        first_name="Rhonda",
        last_name="Root",
        pronouns="She / Her / Hers",
        accepted_community_agreement=True,
    )
    ambassador = User(
        id=2,
        pid=888888888,
        onyen="xlstan",
        email="amam@unc.edu",
        first_name="Amy",
        last_name="Ambassador",
        pronouns="They / Them / Theirs",
        accepted_community_agreement=True,
    )
    user = User(
        id=3,
        pid=111111111,
        onyen="user",
        email="user@unc.edu",
        first_name="Sally",
        last_name="Student",
        pronouns="She / They",
        accepted_community_agreement=True,
    )

    xl_room = RoomDetails(
        id="SN156",
        building="Sitterson",
        room="156",
        nickname="The XL",
        capacity=40,
        reservable=False,
        seats=[],
    )
    group_a = RoomDetails(
        id="SN135",
        building="Sitterson",
        room="135",
        nickname="Group A",
        capacity=4,
        reservable=True,
        seats=[],
    )
    group_b = RoomDetails(
        id="SN137",
        building="Sitterson",
        room="137",
        nickname="Group B",
        capacity=4,
        reservable=True,
        seats=[],
    )
    group_c = RoomDetails(
        id="SN141",
        building="Sitterson",
        room="141",
        nickname="Group C",
        capacity=6,
        reservable=True,
        seats=[],
    )
    pair_a = RoomDetails(
        id="SN139",
        building="Sitterson",
        room="139",
        nickname="Pair A",
        capacity=2,
        reservable=True,
        seats=[],
    )

    monitor_seat_00 = SeatDetails(
        id=1,
        title="Standing Monitor 00",
        shorthand="M00",
        reservable=True,
        has_monitor=True,
        sit_stand=True,
        x=0,
        y=0,
        room=xl_room.to_room(),
    )
    monitor_seat_01 = SeatDetails(
        id=2,
        title="Standing Monitor 01",
        shorthand="M01",
        reservable=False,
        has_monitor=True,
        sit_stand=True,
        x=0,
        y=1,
        room=xl_room.to_room(),
    )
    monitor_seat_10 = SeatDetails(
        id=3,
        title="Monitor 10",
        shorthand="M10",
        reservable=True,
        has_monitor=True,
        sit_stand=False,
        x=1,
        y=0,
        room=xl_room.to_room(),
    )
    monitor_seat_11 = SeatDetails(
        id=4,
        title="Monitor 11",
        shorthand="M11",
        reservable=False,
        has_monitor=True,
        sit_stand=False,
        x=1,
        y=1,
        room=xl_room.to_room(),
    )

    session.add_all(UserEntity.from_model(model) for model in [root, ambassador, user])
    session.add_all(
        RoomEntity.from_model(model)
        for model in [xl_room, group_a, group_b, group_c, pair_a]
    )
    session.add_all(
        SeatEntity.from_model(model)
        for model in [
            monitor_seat_00,
            monitor_seat_01,
            monitor_seat_10,
            monitor_seat_11,
        ]
    )
    session.add(
        OperatingHoursEntity.from_model(
            CoworkingOperatingHours(
                id=1,
                start=now - timedelta(hours=1),
                end=now + timedelta(hours=8),
            )
        )
    )
    session.flush()

    reservations = [
        Reservation(
            id=1,
            start=now - timedelta(hours=1),
            end=now + timedelta(hours=2),
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=1, minutes=30),
            walkin=False,
            room=pair_a,
            state=ReservationState.CHECKED_IN,
            users=[root],
            seats=[],
        ),
        Reservation(
            id=2,
            start=now - timedelta(hours=3),
            end=now - timedelta(hours=1),
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=1),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[ambassador],
            seats=[],
        ),
        Reservation(
            id=3,
            start=now - timedelta(hours=4),
            end=now - timedelta(hours=3),
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=3),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[ambassador],
            seats=[],
        ),
        Reservation(
            id=4,
            start=now - timedelta(hours=2),
            end=now - timedelta(hours=1),
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=1),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[root],
            seats=[],
        ),
        Reservation(
            id=5,
            start=now - timedelta(hours=4),
            end=now - timedelta(hours=3),
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=3),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[root],
            seats=[],
        ),
        Reservation(
            id=6,
            start=now - timedelta(hours=4),
            end=now - timedelta(hours=3),
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=3),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[user],
            seats=[],
        ),
    ]
    session.add_all(
        ReservationEntity.from_model(model, session) for model in reservations
    )
    reset_table_id_seq(session, SeatEntity, SeatEntity.id, 5)
    reset_table_id_seq(session, OperatingHoursEntity, OperatingHoursEntity.id, 2)
    reset_table_id_seq(session, ReservationEntity, ReservationEntity.id, 7)
    session.flush()

    return SignageReservationScenario(
        root=root,
        ambassador=ambassador,
        user=user,
        group_a=group_a,
        pair_a=pair_a,
        monitor_seat_01=monitor_seat_01,
        monitor_seat_11=monitor_seat_11,
    )


def arrange_signage_scenario(session: Session) -> SignageScenario:
    now = datetime.now().replace(microsecond=0)
    reservation = arrange_signage_reservation_scenario(session, now)

    term = Term(
        id="Curr",
        name="Current Term",
        start=now,
        end=now + timedelta(weeks=17),
    )
    course = Course(
        id="comp110",
        subject_code="COMP",
        number="110",
        title="Introduction to Programming and Data Science",
        description="Introduces students to programming and data science.",
        credit_hours=3,
    )
    section = Section(
        id=101,
        course_id=course.id,
        number="001",
        term_id=term.id,
        meeting_pattern="TTh 12:00PM - 1:15PM",
        override_title="",
        override_description="",
        enrolled=100,
        total_seats=200,
    )
    course_site = CourseSite(id=1, title="COMP 110", term_id=term.id)

    session.add(TermEntity.from_model(term))
    session.add(CourseEntity.from_model(course))
    session.add(CourseSiteEntity.from_model(course_site))
    section_entity = SectionEntity.from_model(section)
    section_entity.course_site_id = course_site.id
    session.add(section_entity)

    comp_110_current_office_hours = OfficeHours(
        id=1,
        type=OfficeHoursEventType.OFFICE_HOURS,
        mode=OfficeHoursEventModeType.IN_PERSON,
        description="Current COMP 110 office hours",
        location_description="Sitterson 135",
        start_time=now - timedelta(hours=2),
        end_time=now + timedelta(hours=1),
        course_site_id=course_site.id,
        room_id=reservation.group_a.id,
        recurrence_pattern_id=None,
    )
    second_current_office_hours = OfficeHours(
        id=2,
        type=OfficeHoursEventType.OFFICE_HOURS,
        mode=OfficeHoursEventModeType.IN_PERSON,
        description="Second current office hours",
        location_description="Sitterson 135",
        start_time=now - timedelta(minutes=30),
        end_time=now + timedelta(hours=2),
        course_site_id=course_site.id,
        room_id=reservation.group_a.id,
        recurrence_pattern_id=None,
    )
    session.add_all(
        [
            OfficeHoursEntity.from_model(comp_110_current_office_hours),
            OfficeHoursEntity.from_model(second_current_office_hours),
        ]
    )
    reset_table_id_seq(session, OfficeHoursEntity, OfficeHoursEntity.id, 3)

    announcement = ArticleDraft(
        id=1,
        slug="announcement",
        state=ArticleState.PUBLISHED,
        title="Sample Announcement",
        image_url="https://example.com/announcement.png",
        synopsis="Announcement synopsis",
        body="Announcement body",
        published=now - timedelta(days=2),
        last_modified=now - timedelta(days=2),
        is_announcement=True,
        organization_id=None,
        authors=[_author(reservation.root)],
    )
    article_one = ArticleDraft(
        id=2,
        slug="article-one",
        state=ArticleState.PUBLISHED,
        title="Article One",
        image_url="https://example.com/article-one.png",
        synopsis="Article one synopsis",
        body="Article one body",
        published=now - timedelta(days=1),
        last_modified=now - timedelta(days=1),
        is_announcement=False,
        organization_id=None,
        authors=[_author(reservation.root)],
    )
    article_two = ArticleDraft(
        id=3,
        slug="article-two",
        state=ArticleState.PUBLISHED,
        title="Article Two",
        image_url="https://example.com/article-two.png",
        synopsis="Article two synopsis",
        body="Article two body",
        published=now,
        last_modified=now,
        is_announcement=False,
        organization_id=None,
        authors=[_author(reservation.root)],
    )
    articles = [announcement, article_one, article_two]
    session.add_all(ArticleEntity.from_draft(article) for article in articles)
    reset_table_id_seq(session, ArticleEntity, ArticleEntity.id, 4)
    session.flush()
    for article in articles:
        for author in article.authors:
            session.execute(
                article_author_table.insert().values(
                    {"user_id": author.id, "article_id": article.id}
                )
            )

    organization = Organization(
        id=1,
        name="CSXL",
        shorthand="CSXL",
        slug="csxl",
        logo="logo.png",
        short_description="CSXL",
        long_description="CSXL Organization",
        website="https://csxl.unc.edu",
        email="hello@csxl.unc.edu",
        instagram="csxl",
        linked_in="csxl",
        youtube="csxl",
        heel_life="csxl",
        public=True,
    )
    session.add(OrganizationEntity.from_model(organization))
    event_drafts = [
        EventDraft(
            name="Event One",
            start=now + timedelta(days=1),
            end=now + timedelta(days=1, hours=1),
            location="CSXL",
            description="Event one",
            registration_limit=20,
            organization_slug=organization.slug,
            organizers=[],
        ),
        EventDraft(
            name="Event Two",
            start=now + timedelta(days=2),
            end=now + timedelta(days=2, hours=1),
            location="CSXL",
            description="Event two",
            registration_limit=20,
            organization_slug=organization.slug,
            organizers=[],
        ),
        EventDraft(
            name="Event Three",
            start=now + timedelta(days=3),
            end=now + timedelta(days=3, hours=1),
            location="CSXL",
            description="Event three",
            registration_limit=20,
            organization_slug=organization.slug,
            organizers=[],
        ),
    ]
    session.add_all(
        EventEntity.from_draft_model(event, organization.id) for event in event_drafts
    )
    reset_table_id_seq(session, EventEntity, EventEntity.id, 4)

    signage_reservations = [
        Reservation(
            id=8,
            start=now - timedelta(hours=1),
            end=now + timedelta(hours=2),
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=1, minutes=30),
            walkin=False,
            room=reservation.pair_a,
            state=ReservationState.CHECKED_IN,
            users=[reservation.root],
            seats=[],
        ),
        Reservation(
            id=9,
            start=now - timedelta(hours=2),
            end=now - timedelta(hours=1),
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=1),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[reservation.ambassador],
            seats=[],
        ),
        Reservation(
            id=10,
            start=now - timedelta(hours=4),
            end=now - timedelta(hours=3),
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=3),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[reservation.ambassador],
            seats=[],
        ),
        Reservation(
            id=11,
            start=now - timedelta(hours=2),
            end=now - timedelta(hours=1),
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=1),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[reservation.root],
            seats=[],
        ),
        Reservation(
            id=12,
            start=now - timedelta(hours=4),
            end=now - timedelta(hours=3),
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=3),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[reservation.root],
            seats=[],
        ),
        Reservation(
            id=13,
            start=now - timedelta(hours=4),
            end=now - timedelta(hours=3),
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=3),
            walkin=False,
            room=None,
            state=ReservationState.CHECKED_OUT,
            users=[reservation.user],
            seats=[],
        ),
    ]
    session.add_all(
        ReservationEntity.from_model(model, session) for model in signage_reservations
    )
    reset_table_id_seq(session, ReservationEntity, ReservationEntity.id, 14)
    session.commit()

    return SignageScenario(
        reservation=reservation,
        comp_110_current_office_hours=comp_110_current_office_hours,
        announcement=announcement,
        article_one=article_one,
        article_two=article_two,
    )
