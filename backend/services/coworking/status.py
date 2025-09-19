"""Reservation Service manages room and desk reservations for the XL."""

from fastapi import Depends
from datetime import datetime
from sqlalchemy.orm import Session
from ...database import db_session
from .reservation import ReservationService
from .operating_hours import OperatingHoursService
from .seat import SeatService
from ...models.coworking import Status, TimeRange
from ...models import User
from .policy import PolicyService

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class StatusService:
    """RoleService is the access layer to the role data model, its members, and permissions."""

    def __init__(
        self,
        policies_svc: PolicyService = Depends(),
        operating_hours_svc: OperatingHoursService = Depends(),
        seat_svc: SeatService = Depends(),
        reservation_svc: ReservationService = Depends(),
    ):
        self._policies_svc = policies_svc
        self._reservation_svc = reservation_svc
        self._operating_hours_svc = operating_hours_svc
        self._seat_svc = seat_svc

    def get_coworking_status(self, subject: User) -> Status:
        """All-in-one endpoint for a user to simultaneously get their own upcoming reservations and current status of the XL."""
        coworking_policy = self._policies_svc.policy_for_user(subject)

        my_reservations = self._reservation_svc.get_current_reservations_for_user(
            subject, subject
        )

        now = datetime.now()
        walkin_window = TimeRange(
            start=now,
            end=now
            + coworking_policy.walkin_window
            + 3 * coworking_policy.walkin_initial_duration,
            # We triple walkin duration for end bounds to find seats not pre-reserved later. If XL stays
            # relatively open, the walkin could then more likely be extended while it is not busy.
            # This also prioritizes _not_ placing walkins in reservable seats.
        )
        seats = self._seat_svc.list()  # All Seats are fair game for walkin purposes
        seat_availability = self._reservation_svc.seat_availability(
            seats, walkin_window
        )

        operating_hours = self._operating_hours_svc.schedule(
            TimeRange(start=now, end=now + coworking_policy.reservation_window)
        )

        return Status(
            my_reservations=my_reservations,
            seat_availability=seat_availability,
            operating_hours=operating_hours,
        )
