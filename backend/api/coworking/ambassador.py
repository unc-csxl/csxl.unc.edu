"""Coworking Reservation API

This API is used to make and manage reservations."""

from typing import Sequence
from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService
from ...models import User
from ...models.coworking import Reservation, ReservationPartial, ReservationRequest, ReservationState

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


@api.post("/reservation", tags=["Coworking"])
def create_walkin_reservation(
    reservation_request: ReservationRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Create a walk-in reservation as an ambassador for a user showing up to the desk
    without having drafted/confirmed a reservation of their own ahead of time."""
    # TODO: The efficiency of this operation could be improved with a custom method, but since this
    # happens at the speed of an ambassador manually checking someone in (and is the sequence of steps
    # that normally take place otherwise), reusing existing methods here is fine for now.
    reservation_draft = reservation_svc.draft_reservation(subject, reservation_request)
    # Confirm the Draft Reservation
    reservation_partial = ReservationPartial(id=reservation_draft.id, state=ReservationState.CONFIRMED)
    reservation_confirmed = reservation_svc.change_reservation(subject, reservation_partial)
    # Check Reservation In
    return reservation_svc.staff_checkin_reservation(subject, reservation_confirmed)