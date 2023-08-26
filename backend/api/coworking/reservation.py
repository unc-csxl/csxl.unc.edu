"""Coworking Reservation API

This API is used to make and manage reservations."""

from fastapi import APIRouter, Depends, HTTPException
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService, ReservationError
from ...models import User
from ...models.coworking import Reservation, ReservationRequest

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking")


@api.post("/reservation", tags=["Coworking"])
def draft_reservation(
    reservation_request: ReservationRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Draft a reservation request."""
    try:
        return reservation_svc.draft_reservation(subject, reservation_request)
    except ReservationError as e:
        raise HTTPException(status_code=422, detail=str(e))
