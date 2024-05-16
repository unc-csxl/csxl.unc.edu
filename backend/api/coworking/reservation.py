"""Coworking Client Reservation API

This API is used to make and manage reservations."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Sequence
from datetime import datetime

from backend.models.room import Room
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationException, ReservationService
from ...models import User
from ...models.coworking import (
    Reservation,
    ReservationRequest,
    ReservationPartial,
    ReservationState,
    ReservationMapDetails
)

__authors__ = ["Kris Jordan, Yuvraj Jain"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking")
openapi_tags = {
    "name": "Coworking",
    "description": "Coworking reservations, status, and XL Ambassador functionality.",
}


@api.post("/reservation", tags=["Coworking"])
def draft_reservation(
    reservation_request: ReservationRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Draft a reservation request."""
    return reservation_svc.draft_reservation(subject, reservation_request)


@api.get("/reservation/{id}", tags=["Coworking"])
def get_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    return reservation_svc.get_reservation(subject, id)


@api.get("/room-reservations/", tags=["Coworking"])
def get_all_reservations_by_state(
    state: ReservationState,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Sequence[Reservation]:
    try:
        return reservation_svc.get_current_reservations_for_user(
            subject=subject, focus=subject, state=state
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put("/reservation/{id}", tags=["Coworking"])
def update_reservation(
    reservation: ReservationPartial,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Modify a reservation."""
    return reservation_svc.change_reservation(subject, reservation)


@api.delete("/reservation/{id}", tags=["Coworking"])
def cancel_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Cancel a reservation."""
    return reservation_svc.change_reservation(
        subject, ReservationPartial(id=id, state=ReservationState.CANCELLED)
    )


@api.get("/room-reservation/", tags=["Coworking"])
def get_reservations_for_rooms_by_date(
    date: datetime,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> ReservationMapDetails:
    """See available rooms for any given day."""
    try:
        return reservation_svc.get_map_reserved_times_by_date(date, subject)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/user-reservations/", tags=["Coworking"])
def get_total_hours_study_room_reservations(
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> str:
    """Allows a user to know how many hours they have reserved in all study rooms (Excludes CSXL)."""
    return reservation_svc.get_total_time_user_reservations(subject)
