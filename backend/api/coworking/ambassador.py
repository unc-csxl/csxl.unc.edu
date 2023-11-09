"""Coworking Reservation API

This API is used to make and manage reservations."""

from typing import Sequence
from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService
from ...models import User
from ...models.coworking import Reservation, ReservationPartial

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking/ambassador")


@api.get("", tags=["Coworking"])
def active_and_upcoming_reservations(
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Sequence[Reservation]:
    """List active and upcoming reservations.

    This list drives the ambassador's checkin UI."""
    return reservation_svc.list_all_active_and_upcoming(subject)


@api.put("/checkin", tags=["Coworking"])
def checkin_reservation(
    reservation: ReservationPartial,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """CheckIn a confirmed reservation."""
    return reservation_svc.staff_checkin_reservation(subject, reservation)
