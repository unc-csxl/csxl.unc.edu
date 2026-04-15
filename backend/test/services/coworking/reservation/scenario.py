"""Shared explicit arrange helpers for reservation service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from unittest.mock import create_autospec

from sqlalchemy.orm import Session

from .....entities import RoomEntity, UserEntity
from .....entities.coworking import (
    OperatingHoursEntity,
    ReservationEntity,
    SeatEntity,
)
from .....models import RoomDetails, User
from .....models.coworking import (
    OperatingHours,
    Reservation,
    ReservationRequest,
    ReservationState,
    SeatDetails,
)
from .....models.coworking.seat import SeatIdentity
from .....models.user import UserIdentity
from .....services import PermissionService
from .....services.coworking import (
    OperatingHoursService,
    PolicyService,
    ReservationService,
    SeatService,
)
from ...reset_table_id_seq import reset_table_id_seq
from ..time import (
    AN_HOUR_AGO,
    IN_EIGHT_HOURS,
    IN_TEN_MINUTES,
    IN_THIRTY_MINUTES,
    IN_THREE_HOURS,
    IN_TWO_HOURS,
    NOW,
    ONE_DAY,
    ONE_HOUR,
    THIRTY_MINUTES,
    THIRTY_MINUTES_AGO,
)


@dataclass
class ReservationScenario:
    root: User
    ambassador: User
    user: User
    student: User
    xl_room: RoomDetails
    group_a: RoomDetails
    group_b: RoomDetails
    group_c: RoomDetails
    pair_a: RoomDetails
    monitor_seat_00: SeatDetails
    monitor_seat_01: SeatDetails
    monitor_seat_10: SeatDetails
    monitor_seat_11: SeatDetails
    seats: list[SeatDetails]
    reservable_seats: list[SeatDetails]
    unreservable_seats: list[SeatDetails]
    today: OperatingHours
    tomorrow: OperatingHours
    future: OperatingHours
    three_days_from_today: OperatingHours
    reservation_1: Reservation
    reservation_2: Reservation
    reservation_3: Reservation
    reservation_4: Reservation
    reservation_5: Reservation
    reservation_6: Reservation
    reservation_7: Reservation
    active_reservations: list[Reservation]
    confirmed_reservations: list[Reservation]
    draft_reservations: list[Reservation]
    room_reservations: list[Reservation]
    reservations: list[Reservation]


def make_reservation_service(
    session: Session,
    permission_svc: PermissionService | None = None,
    policy_svc: PolicyService | None = None,
) -> ReservationService:
    permission = (
        permission_svc
        if permission_svc is not None
        else create_autospec(PermissionService)
    )
    return ReservationService(
        session,
        permission,
        policy_svc if policy_svc is not None else PolicyService(),
        OperatingHoursService(session, create_autospec(PermissionService)),
        SeatService(session),
    )


def arrange_standard_reservation_scenario(
    session: Session, time: dict[str, datetime]
) -> ReservationScenario:
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
    student = User(
        id=6,
        pid=555555555,
        onyen="stewie",
        email="stewie@unc.edu",
        first_name="Stewie",
        last_name="Student",
        pronouns="They / Them / Theirs",
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
    seats = [monitor_seat_00, monitor_seat_01, monitor_seat_10, monitor_seat_11]
    reservable_seats = [seat for seat in seats if seat.reservable]
    unreservable_seats = [seat for seat in seats if not seat.reservable]

    today = OperatingHours(id=1, start=time[AN_HOUR_AGO], end=time[IN_THREE_HOURS])
    future = OperatingHours(
        id=2,
        start=time[AN_HOUR_AGO] + 2 * ONE_DAY,
        end=time[IN_TWO_HOURS] + 2 * ONE_DAY,
    )
    tomorrow = OperatingHours(
        id=3,
        start=time[AN_HOUR_AGO] + ONE_DAY,
        end=time[IN_TWO_HOURS] + ONE_DAY,
    )
    three_days_from_today = OperatingHours(
        id=4,
        start=time[AN_HOUR_AGO] + 3 * ONE_DAY,
        end=time[IN_EIGHT_HOURS] + 3 * ONE_DAY,
    )

    reservation_1 = Reservation(
        id=1,
        start=time[THIRTY_MINUTES_AGO],
        end=time[IN_TEN_MINUTES],
        created_at=time[THIRTY_MINUTES_AGO],
        updated_at=time[THIRTY_MINUTES_AGO],
        walkin=False,
        room=None,
        state=ReservationState.CHECKED_IN,
        users=[user],
        seats=[monitor_seat_00],
    )
    reservation_2 = Reservation(
        id=2,
        start=time[THIRTY_MINUTES_AGO],
        end=time[IN_THIRTY_MINUTES],
        created_at=time[THIRTY_MINUTES_AGO],
        updated_at=time[THIRTY_MINUTES_AGO],
        walkin=False,
        room=None,
        state=ReservationState.CHECKED_OUT,
        users=[ambassador],
        seats=[monitor_seat_01],
    )
    reservation_3 = Reservation(
        id=3,
        start=time[THIRTY_MINUTES_AGO],
        end=time[IN_THIRTY_MINUTES],
        created_at=time[THIRTY_MINUTES_AGO],
        updated_at=time[THIRTY_MINUTES_AGO],
        walkin=False,
        room=None,
        state=ReservationState.CANCELLED,
        users=[root],
        seats=[monitor_seat_10],
    )
    reservation_4 = Reservation(
        id=4,
        start=today.end - ONE_HOUR,
        end=today.end - THIRTY_MINUTES,
        created_at=time[NOW],
        updated_at=time[NOW],
        walkin=False,
        room=None,
        state=ReservationState.CONFIRMED,
        users=[root, ambassador],
        seats=[reservable_seats[0], reservable_seats[1]],
    )
    reservation_5 = Reservation(
        id=5,
        start=tomorrow.start,
        end=tomorrow.end,
        created_at=time[NOW],
        updated_at=time[NOW],
        walkin=False,
        room=None,
        state=ReservationState.DRAFT,
        users=[user],
        seats=[reservable_seats[0]],
    )
    reservation_6 = Reservation(
        id=6,
        start=tomorrow.start + timedelta(hours=25),
        end=tomorrow.start + timedelta(hours=26, minutes=30),
        created_at=time[NOW],
        updated_at=time[NOW],
        walkin=False,
        room=group_a,
        state=ReservationState.CONFIRMED,
        users=[user],
        seats=[],
    )
    reservation_7 = Reservation(
        id=7,
        start=today.start,
        end=today.start + timedelta(minutes=30),
        created_at=today.start,
        updated_at=today.start,
        walkin=False,
        room=group_a,
        state=ReservationState.CONFIRMED,
        users=[root],
        seats=[],
    )

    users = [root, ambassador, user, student]
    rooms = [xl_room, group_a, group_b, pair_a, group_c]
    operating_hours = [today, future, tomorrow, three_days_from_today]
    reservations = [
        reservation_1,
        reservation_2,
        reservation_3,
        reservation_4,
        reservation_5,
        reservation_6,
        reservation_7,
    ]

    session.add_all(UserEntity.from_model(model) for model in users)
    session.add_all(RoomEntity.from_model(model) for model in rooms)
    session.add_all(SeatEntity.from_model(model) for model in seats)
    session.add_all(OperatingHoursEntity.from_model(model) for model in operating_hours)
    session.flush()
    session.add_all(
        ReservationEntity.from_model(model, session) for model in reservations
    )
    reset_table_id_seq(session, SeatEntity, SeatEntity.id, len(seats) + 1)
    reset_table_id_seq(
        session, OperatingHoursEntity, OperatingHoursEntity.id, len(operating_hours) + 1
    )
    reset_table_id_seq(
        session, ReservationEntity, ReservationEntity.id, len(reservations) + 1
    )
    session.commit()

    return ReservationScenario(
        root=root,
        ambassador=ambassador,
        user=user,
        student=student,
        xl_room=xl_room,
        group_a=group_a,
        group_b=group_b,
        group_c=group_c,
        pair_a=pair_a,
        monitor_seat_00=monitor_seat_00,
        monitor_seat_01=monitor_seat_01,
        monitor_seat_10=monitor_seat_10,
        monitor_seat_11=monitor_seat_11,
        seats=seats,
        reservable_seats=reservable_seats,
        unreservable_seats=unreservable_seats,
        today=today,
        tomorrow=tomorrow,
        future=future,
        three_days_from_today=three_days_from_today,
        reservation_1=reservation_1,
        reservation_2=reservation_2,
        reservation_3=reservation_3,
        reservation_4=reservation_4,
        reservation_5=reservation_5,
        reservation_6=reservation_6,
        reservation_7=reservation_7,
        active_reservations=[reservation_1],
        confirmed_reservations=[reservation_4],
        draft_reservations=[reservation_5],
        room_reservations=[reservation_6],
        reservations=reservations,
    )


def make_test_request(
    scenario: ReservationScenario,
    overrides: dict | None = None,
) -> ReservationRequest:
    request_data = {
        "start": datetime.now(),
        "end": datetime.now() + THIRTY_MINUTES,
        "users": [UserIdentity(id=scenario.ambassador.id)],
        "seats": [SeatIdentity(id=scenario.monitor_seat_01.id)],
    }
    if overrides:
        request_data.update(overrides)
    return ReservationRequest(**request_data)
