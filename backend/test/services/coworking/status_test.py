"""Test coworking StatusService"""

from datetime import datetime, timedelta

from .fixtures import status_svc
from ....services.coworking.status import StatusService
from ....models import User
from ....models.coworking.availability import SeatAvailability
from ....models.coworking import OperatingHours, Reservation, ReservationState


def make_subject() -> User:
    return User(id=1, pid=1, onyen="root")


def make_reservation() -> Reservation:
    now = datetime.now()
    return Reservation(
        id=1,
        start=now,
        end=now + timedelta(hours=1),
        state=ReservationState.CONFIRMED,
        created_at=now,
        updated_at=now,
    )


def make_operating_hours() -> OperatingHours:
    now = datetime.now()
    return OperatingHours(id=1, start=now, end=now + timedelta(hours=3))


def test_status_dispatch(status_svc: StatusService):
    subject = make_subject()
    reservation = make_reservation()
    operating_hours = make_operating_hours()

    # Hard-wire mock responses to all dispatched methods
    # We test these methods elsewhere
    status_svc._reservation_svc.get_current_reservations_for_user.return_value = [
        reservation
    ]
    status_svc._policies_svc.walkin_window.return_value = timedelta(minutes=15)
    status_svc._policies_svc.walkin_initial_duration.return_value = timedelta(hours=1)
    status_svc._policies_svc.reservation_window.return_value = timedelta(weeks=1)
    status_svc._seat_svc.list.return_value = []
    status_svc._operating_hours_svc.schedule.return_value = [operating_hours]

    seat_availability = [
        SeatAvailability(
            id=0,
            availability=[],
            title="S1",
            shorthand="S1",
            reservable=True,
            has_monitor=False,
            sit_stand=False,
            x=0,
            y=0,
        )
    ]
    status_svc._reservation_svc.seat_availability.return_value = seat_availability

    # Call the method
    status = status_svc.get_coworking_status(subject)

    # Look for dependent methods to be called
    status_svc._reservation_svc.get_current_reservations_for_user.assert_called_once_with(
        subject, subject
    )
    status_svc._reservation_svc.seat_availability.assert_called_once()
    status_svc._operating_hours_svc.schedule.assert_called_once()

    # Look for expected RVs
    assert status.my_reservations == [reservation]
    assert status.seat_availability == seat_availability
    assert status.operating_hours == [operating_hours]
