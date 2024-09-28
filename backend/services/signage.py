"""
Service to collect and organize the information for CSXL Signage
"""
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session

from datatime import datetime

from models import SignageOverviewFast, SignageOverviewSlow
from services import ReservationService, SeatService

__authors__ = ["Andrew Lockard", "Will Zahrt", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

class SignageService:
    """
    Service to collect and organize the information for CSXL Signage
    """
    def __init__(
        self, 
        reservation_svc: ReservationService = Depends(), 
        session: Session = Depends(db_session), 
        seat_svc: SeatService = Depends()
    ):
        self._reservation_svc = reservation_svc
        self._session = session
        self._seat_svc = seat_svc

    def get_fast_data(self) -> SignageOverviewFast:
        """
        Gets the data for the fast API route
        """
        # Seats
        walkin_window = TimeRange(
            start=now,
            end=now + timedelta(hours=6, minutes=10) # Makes sure open seats are available for 2hr walkin reservation
        )
        seats = self._seat_svc.list()  # All Seats are fair game for walkin purposes
        seat_availability = self._reservation_svc.seat_availability(
            seats, walkin_window
        )

        return SignageOverviewFast(
            seat_availability = seat_availability
        )