"""Service that manages policies around the reservation system."""

from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from ...database import db_session
from ...models import User

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class PolicyService:
    """RoleService is the access layer to the role data model, its members, and permissions.

    We are carving out a simple service for looking up policies in anticipation of having different policies
    for different groups of users (e.g. majors, ambassadors, LAs, etc).
    """

    def __init__(self): ...

    def walkin_window(self, _subject: User) -> timedelta:
        """How far into the future can walkins be reserved?"""
        return timedelta(minutes=30)

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
    
    def non_reservable_rooms(self) -> list[str]:
        return ['SN151']

