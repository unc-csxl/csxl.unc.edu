"""Service that manages policies around the reservation system."""

from enum import Enum
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, time

from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.models.roster_role import RosterRole
from ...database import db_session
from ...models import User
from abc import ABC, abstractmethod
from pydantic import BaseModel

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

OH_HOURS = {
    MONDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [],
        "SN141": [(time(hour=9), time(hour=12)), ((time(hour=15), time(hour=18)))],
        "SN144": [],
        "SN146": [],
        "SN147": [(time(hour=0), time(hour=23))],
    },
    TUESDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [],
        "SN141": [],
        "SN144": [],
        "SN146": [],
        "SN147": [(time(hour=14), time(hour=16))],
    },
    WEDNESDAY: {
        "SN135": [(time(hour=12), time(hour=14))],
        "SN137": [(time(hour=11), time(hour=13))],
        "SN139": [],
        "SN141": [(time(hour=10), time(hour=12)), (time(hour=15), time(hour=18))],
        "SN144": [],
        "SN146": [],
        "SN147": [(time(hour=15), time(hour=17))],
    },
    THURSDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [],
        "SN141": [(time(hour=15), time(hour=17))],
        "SN144": [],
        "SN146": [],
        "SN147": [(time(hour=14), time(hour=16))],
    },
    FRIDAY: {
        "SN135": [(time(hour=15), time(hour=18))],
        "SN137": [(time(hour=15), time(hour=17))],
        "SN139": [],
        "SN141": [(time(hour=12), time(hour=14))],
        "SN144": [],
        "SN146": [],
        "SN147": [],
    },
    SATURDAY: {},
    SUNDAY: {},
}


class CoworkingPolicyType(Enum):
    """
    Determines the different types of coworking policies.

    These are mapped to numbers for comparison purposes to determine which policy to use
    if multiple policies match, with the greatest number taking the highest priority.
    """

    STUDENT = 0
    """Policy for regular users"""

    INSTRUCTOR = 1
    """Policy for regular instructors"""


class CoworkingPolicy(BaseModel):

    walkin_window: timedelta
    """How far into the future can walkins be reserved?"""

    walkin_initial_duration: timedelta
    """When making a walkin, this sets how long the initial reservation is for."""

    reservation_window: timedelta
    """Returns the number of days in advance the user can make reservations."""

    minimum_reservation_duration: timedelta
    """The minimum amount of time a reservation can be made for."""

    maximum_initial_reservation_duration: timedelta
    """The maximum amount of time a reservation can be made for before extending."""

    reservation_draft_timeout: timedelta

    reservation_checkin_timeout: timedelta

    room_reservation_weekly_limit: timedelta
    """The maximum amount of hours a student can reserve the study rooms outside of the csxl."""

    allow_overlapping_room_reservations: bool
    """Whether or not to allow the user to reserve two rooms at the same time (useful for instructors)"""


class PolicyService:
    """RoleService is the access layer to the role data model, its members, and permissions.

    We are carving out a simple service for looking up policies in anticipation of having different policies
    for different groups of users (e.g. majors, ambassadors, LAs, etc).
    """

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session
        # Set policies here
        self._policies: dict[CoworkingPolicyType, CoworkingPolicy] = {
            CoworkingPolicyType.STUDENT: CoworkingPolicy(
                walkin_window=timedelta(minutes=10),
                walkin_initial_duration=timedelta(hours=2),
                reservation_window=timedelta(weeks=1),
                minimum_reservation_duration=timedelta(minutes=10),
                maximum_initial_reservation_duration=timedelta(hours=2),
                reservation_draft_timeout=timedelta(minutes=5),
                reservation_checkin_timeout=timedelta(minutes=10),
                room_reservation_weekly_limit=timedelta(hours=6),
                allow_overlapping_room_reservations=False,
            ),
            CoworkingPolicyType.INSTRUCTOR: CoworkingPolicy(
                walkin_window=timedelta(minutes=10),
                walkin_initial_duration=timedelta(hours=2),
                reservation_window=timedelta(weeks=8),
                minimum_reservation_duration=timedelta(minutes=10),
                maximum_initial_reservation_duration=timedelta(hours=2),
                reservation_draft_timeout=timedelta(minutes=5),
                reservation_checkin_timeout=timedelta(minutes=10),
                room_reservation_weekly_limit=timedelta(hours=168),  # 24hrs * 7days
                allow_overlapping_room_reservations=True,
            ),
        }

    def default_policy(self) -> CoworkingPolicy:
        """Returns the default policy.
        NOTE: At some point, this likely should be phased out.
        """
        return self._policies[CoworkingPolicyType.STUDENT]

    def policy_for_user(self, _subject: User) -> CoworkingPolicy:
        """Determines the coworking policy to use for a given subject."""

        # Determine if the user is an instructor for a course.
        is_instructor_query = (
            select(func.count())
            .select_from(SectionMemberEntity)
            .where(
                SectionMemberEntity.user_id == _subject.id,
                SectionMemberEntity.member_role == RosterRole.INSTRUCTOR,
            )
        )
        is_instructor = self._session.execute(is_instructor_query).scalar() > 0
        if is_instructor:
            return self._policies[CoworkingPolicyType.INSTRUCTOR]

        # Otherwise, the user is a regular user.
        # NOTE: In the future, this can be extended easily to add extra policies
        # for ambassadors, etc.
        return self._policies[CoworkingPolicyType.STUDENT]

    # def walkin_window(self, policy: CoworkingPolicy) -> timedelta:
    #     """How far into the future can walkins be reserved?"""
    #     return self._policy(_subject).walkin_window

    # def walkin_initial_duration(self, _subject: User) -> timedelta:
    #     """When making a walkin, this sets how long the initial reservation is for."""
    #     return self._policy(_subject).walkin_initial_duration

    # def reservation_window(self, _subject: User) -> timedelta:
    #     """Returns the number of days in advance the user can make reservations."""
    #     return self._policy(_subject).reservation_window

    # def minimum_reservation_duration(self, _subject: User) -> timedelta:
    #     """The minimum amount of time a reservation can be made for."""
    #     return self._policy(_subject).minimum_reservation_duration

    # def maximum_initial_reservation_duration(self, _subject: User) -> timedelta:
    #     """The maximum amount of time a reservation can be made for before extending."""
    #     return self._policy(_subject).maximum_initial_reservation_duration

    # # Implement and involve in testing once extending a reservation functionality is added.
    # # def extend_window(self, _subject: User) -> timedelta:
    # #     """When no reservation follows a given reservation, within this period preceeding the end of a reservation the user is able to extend their reservation by an hour."""
    # #     return timedelta(minutes=15 * -1)

    # # def extend_duration(self, _subject: User) -> timedelta:
    # #     return timedelta(hours=1)

    # def reservation_draft_timeout(self, _subject: User) -> timedelta:
    #     return self._policy(_subject).reservation_draft_timeout

    # def reservation_checkin_timeout(self, _subject: User) -> timedelta:
    #     return self._policy(_subject).reservation_checkin_timeout

    # def room_reservation_weekly_limit(self, _subject: User) -> timedelta:
    #     """The maximum amount of hours a student can reserve the study rooms outside of the csxl."""
    #     return self._policy(_subject).room_reservation_weekly_limit

    def office_hours(self, date: datetime):
        day = date.weekday()
        return OH_HOURS[day]
