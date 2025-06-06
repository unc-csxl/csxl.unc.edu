"""Test coworking StatusService"""

from .fixtures import status_svc
from ....services.coworking.status import StatusService
from ....models.coworking.availability import SeatAvailability
from datetime import timedelta

from ..core_data import user_data
from . import operating_hours_data
from .reservation import reservation_data

# Since there are relationship dependencies between the entities, order matters.
from .time import *
from ..core_data import setup_insert_data_fixture as insert_order_0
from .operating_hours_data import fake_data_fixture as insert_order_1
from ..room_data import fake_data_fixture as insert_order_2
from .seat_data import fake_data_fixture as insert_order_3
from .reservation.reservation_data import fake_data_fixture as insert_order_4
from .fixtures import permission_svc, operating_hours_svc


def test_status_dispatch(status_svc: StatusService):
    # Hard-wire mock responses to all dispatched methods
    # We test these methods elsewhere
    status_svc._reservation_svc.get_current_reservations_for_user.return_value = [
        reservation_data.reservation_1
    ]
    status_svc._policies_svc.walkin_window.return_value = timedelta(minutes=15)
    status_svc._policies_svc.walkin_initial_duration.return_value = timedelta(hours=1)
    status_svc._policies_svc.reservation_window.return_value = timedelta(weeks=1)
    status_svc._seat_svc.list.return_value = []
    status_svc._operating_hours_svc.schedule.return_value = [operating_hours_data.today]

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
    status = status_svc.get_coworking_status(user_data.root)

    # Look for dependent methods to be called
    status_svc._reservation_svc.get_current_reservations_for_user.assert_called_once_with(
        user_data.root, user_data.root
    )
    status_svc._reservation_svc.seat_availability.assert_called_once()
    status_svc._operating_hours_svc.schedule.assert_called_once()

    # Look for expected RVs
    assert status.my_reservations == [reservation_data.reservation_1]
    assert status.seat_availability == seat_availability
    assert status.operating_hours == [operating_hours_data.today]
