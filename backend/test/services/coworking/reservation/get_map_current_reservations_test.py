"""Tests for ReservationService#get_map_reservations_for_date and helper functions."""

from backend.models.coworking.reservation import ReservationState
from datetime import date

from .....services.coworking import ReservationService

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (seat_svc) are required to be imported in the testing module.
from ..fixtures import (
    reservation_svc,
    permission_svc,
    seat_svc,
    policy_svc,
    operating_hours_svc,
)
from ..time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ...core_data import user_data
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..operating_hours_data import fake_data_fixture as insert_order_1
from ...room_data import fake_data_fixture as insert_order_2
from ..seat_data import fake_data_fixture as insert_order_3
from .reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import seat_data
from . import reservation_data

__authors__ = [
    "Nick Wherthey",
    "Yuvraj Jain",
]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_is_xl_closed(reservation_svc: ReservationService):
    """Test to check if XL is closed"""
    day = date(year=2024, month=2, day=28) # Because it's Kris's birthday :)
    assert reservation_svc._is_xl_closed(day) == False


def test_transform_date_map_for_unavailable_simple(reservation_svc: ReservationService):
    """
    Validates the transformation of the date map to indicate unavailable time slots.
    
    This test ensures that time slots are appropriately grayed out for all other rooms
    once a user has made a reservation. For example, if Sally Student reserves room SN135
    from 1 pm to 3 pm on February 29, she should be prevented from booking any other room
    during these hours. The function verifies that the data map returned by the endpoint
    accurately reflects these unavailable slots, enhancing the user experience by
    preventing double bookings.
    """
    
    sample_date_map_1 = {
        'SN135': [0, 0, 0, 0],
        'SN137': [0, 0, 4, 4],
        'SN139': [0, 0, 0, 0]
    }

    expected_transformed_date_map_1 = {
        'SN135': [0, 0, 3, 3],
        'SN137': [0, 0, 4, 4],
        'SN139': [0, 0, 3, 3]
    }

    reservation_svc._transform_date_map_for_unavailable(sample_date_map_1)
    assert sample_date_map_1 == expected_transformed_date_map_1


def test_transform_date_map_for_unavailable_complex(reservation_svc: ReservationService):    
    sample_date_map_2 = {
        'SN135': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        'SN137': [0, 0, 1, 1, 4, 4, 4, 4, 0, 0],
        'SN139': [0, 4, 4, 1, 1, 0, 0, 0, 0, 0]
    }

    expected_transformed_date_map_2 = {
        'SN135': [0, 3, 3, 0, 3, 3, 1, 1, 1, 1],
        'SN137': [0, 3, 1, 1, 4, 4, 4, 4, 0, 0],
        'SN139': [0, 4, 4, 1, 1, 3, 3, 3, 0, 0]
    }

    reservation_svc._transform_date_map_for_unavailable(sample_date_map_2)
    assert expected_transformed_date_map_2 == sample_date_map_2


def test_idx_calculation(reservation_svc: ReservationService):
    time_1 = datetime.now().replace(hour=10, minute=12)
    assert reservation_svc._idx_calculation(time_1) == 0

    time_2 = datetime.now().replace(hour=12, minute=30)
    assert reservation_svc._idx_calculation(time_2) == 5

    time_3 = datetime.now().replace(hour=13, minute=40)
    assert reservation_svc._idx_calculation(time_3) == 7


def test_query_confirmed_reservations_by_date(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Test getting all reservations for a particular date."""
    reservations = reservation_svc._query_confirmed_reservations_by_date(time[TOMORROW])
    assert len(reservations) == 2
    assert reservations[0].start >= time[MIDNIGHT_TOMORROW]
    assert reservations[0].start <= time[MIDNIGHT_TOMORROW] + timedelta(hours=24)

def test_get_reservable_rooms(reservation_svc: ReservationService):
    rooms = reservation_svc._get_reservable_rooms()
    assert rooms[0].id == 'SN135' and rooms[0].reservable is True
    assert rooms[1].id == 'SN137' and rooms[1].reservable is True
    assert rooms[2].id == 'SN139' and rooms[2].reservable is True
    assert rooms[3].id == 'SN141' and rooms[3].reservable is True

def test_get_map_reserved_times_by_date(
    reservation_svc: ReservationService, time: dict[str, datetime]
):
    """Test for getting a dictionary where keys are room ids and time slots array are values."""
    test_time = time[NOW].replace(year=2024, month=2, day=28, hour=11, minute=20)
    reserved_date_map = reservation_svc.get_map_reserved_times_by_date(
        test_time, user_data.user
    )
    assert reserved_date_map["SN135"][0] == 0

    reserved_date_map_root = reservation_svc.get_map_reserved_times_by_date(
        test_time, user_data.root
    )
    assert reserved_date_map_root["SN135"][0] == 0
