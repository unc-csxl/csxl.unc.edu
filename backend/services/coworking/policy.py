"""Service that manages policies around the reservation system."""

from datetime import timedelta

from ...models import User

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023-24"
__license__ = "MIT"


class PolicyService:
    """Centralize duration and reservation-window policies.

    These methods may later vary policies for different groups of users.
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
