"""Service that manages policies around the reservation system."""

from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, time
from ...database import db_session
from ...models import User

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
        "SN139": [(time(hour=15), time(hour=17))],
        "SN141": [(time(hour=13), time(hour=17))],
        "SN144": [(time(hour=13), time(hour=18))],
        "SN146": [],
        "SN147": [(time(hour=10), time(hour=15))],
    },
    TUESDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [],
        "SN141": [(time(hour=12), time(hour=18))],
        "SN144": [(time(hour=9), time(hour=11)), (time(hour=13), time(hour=17))],
        "SN146": [(time(hour=15), time(hour=17))],
        "SN147": [
            (time(hour=9), time(hour=13)),
            (time(hour=14), time(hour=16, minute=30)),
        ],
    },
    WEDNESDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [(time(hour=14), time(hour=15))],
        "SN141": [(time(hour=14), time(hour=17))],
        "SN144": [(time(hour=13), time(hour=17))],
        "SN146": [(time(hour=10, minute=30), time(hour=12, minute=30))],
        "SN147": [(time(hour=10), time(hour=13)), (time(hour=14), time(hour=16))],
    },
    THURSDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [(time(hour=16), time(hour=17))],
        "SN141": [(time(hour=15), time(hour=17))],
        "SN144": [(time(hour=9), time(hour=18))],
        "SN146": [(time(hour=15), time(hour=17))],
        "SN147": [
            (time(hour=9), time(hour=13)),
            (time(hour=15, minute=30), time(hour=16, minute=30)),
        ],
    },
    FRIDAY: {
        "SN135": [],
        "SN137": [],
        "SN139": [],
        "SN141": [(time(hour=13), time(hour=16))],
        "SN144": [(time(hour=9), time(hour=10)), (time(hour=12), time(hour=15))],
        "SN146": [(time(hour=13), time(hour=15))],
        "SN147": [(time(hour=12), time(hour=15))],
    },
    SATURDAY: {},
    SUNDAY: {},
}


class PolicyService:
    """RoleService is the access layer to the role data model, its members, and permissions.

    We are carving out a simple service for looking up policies in anticipation of having different policies
    for different groups of users (e.g. majors, ambassadors, LAs, etc).
    """

    def __init__(self): ...

    def walkin_window(self, _subject: User) -> timedelta:
        """How far into the future can walkins be reserved?"""
        return timedelta(minutes=10)

    def walkin_initial_duration(self, _subject: User) -> timedelta:
        """When making a walkin, this sets how long the initial reservation is for."""
        return timedelta(hours=2)

    def reservation_window(self, _subject: User) -> timedelta:
        """Returns the number of days in advance the user can make reservations."""
        return timedelta(weeks=1)

    def minimum_reservation_duration(self) -> timedelta:
        """The minimum amount of time a reservation can be made for."""
        return timedelta(minutes=10)

    def maximum_initial_reservation_duration(self, _subject: User) -> timedelta:
        """The maximum amount of time a reservation can be made for before extending."""
        return timedelta(hours=2)

    # Implement and involve in testing once extending a reservation functionality is added.
    # def extend_window(self, _subject: User) -> timedelta:
    #     """When no reservation follows a given reservation, within this period preceeding the end of a reservation the user is able to extend their reservation by an hour."""
    #     return timedelta(minutes=15 * -1)

    # def extend_duration(self, _subject: User) -> timedelta:
    #     return timedelta(hours=1)

    def reservation_draft_timeout(self) -> timedelta:
        return timedelta(minutes=5)

    def reservation_checkin_timeout(self) -> timedelta:
        return timedelta(minutes=10)

    def room_reservation_weekly_limit(self) -> timedelta:
        """The maximum amount of hours a student can reserve the study rooms outside of the csxl."""
        return timedelta(hours=6)

    def office_hours(self, date: datetime):
        day = date.weekday()
        if day == MONDAY:
            return OH_HOURS[MONDAY]
        elif day == TUESDAY:
            return OH_HOURS[TUESDAY]
        elif day == WEDNESDAY:
            return OH_HOURS[WEDNESDAY]
        elif day == THURSDAY:
            return OH_HOURS[THURSDAY]
        elif day == FRIDAY:
            return OH_HOURS[FRIDAY]
        elif day == SATURDAY:
            return OH_HOURS[SATURDAY]
        else:
            return OH_HOURS[SUNDAY]
