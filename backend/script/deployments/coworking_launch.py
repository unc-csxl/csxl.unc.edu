"""Script to kick-off the CS XL coworking checkin system.

This is quick and dirty for getting some desk data loaded into the system.
"""

__author__ = "Kris Jordan <kris@cs.unc.edu>"


import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from ...database import engine
from ...env import getenv
from ... import entities
from ...entities.coworking import SeatEntity, OperatingHoursEntity, RoomEntity
from ...test.services.reset_table_id_seq import reset_table_id_seq

from ...test.services import role_data, user_data, permission_data, room_data
from ...test.services.coworking import (
    seat_data,
    operating_hours_data,
    time,
)
from ...models.coworking import SeatDetails
from ...test.services.coworking.reservation import reservation_data

if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


with Session(engine) as session:
    time = time.time_data()
    reservation_data.delete_future_data(session, time)
    seat_data.delete_all(session)
    operating_hours_data.delete_all(session)

    seats: list[SeatDetails] = []
    # Sit Desks w/ Monitor
    for i in range(12):
        seats.append(
            SeatDetails(
                id=i,
                title="Sitting Desk with Monitor",
                shorthand="Sit",
                reservable=False,
                has_monitor=True,
                sit_stand=False,
                x=0,
                y=0,
                room=room_data.the_xl.to_room(),
            )
        )

    # Sit/Stand Desks w/ Monitor
    for i in range(12, 18):
        seats.append(
            SeatDetails(
                id=i,
                title="Standing Desk with Monitor",
                shorthand="Stand",
                reservable=False,
                has_monitor=True,
                sit_stand=True,
                x=0,
                y=0,
                room=room_data.the_xl.to_room(),
            )
        )

    # Collab Area
    for i in range(18, 42):
        seats.append(
            SeatDetails(
                id=i,
                title="Communal Area Seat",
                shorthand="Communal",
                reservable=False,
                has_monitor=False,
                sit_stand=False,
                x=0,
                y=0,
                room=room_data.the_xl.to_room(),
            )
        )

    session.add(RoomEntity.from_model(room_data.the_xl))

    for seat in seats:
        entity = SeatEntity.from_model(seat)
        session.add(entity)
    reset_table_id_seq(session, SeatEntity, SeatEntity.id, len(seats) + 1)

    from datetime import datetime

    dates_as_strings = [
        "10/17/2023",
        "10/18/2023",
        "10/23/2023",
        "10/24/2023",
        "10/25/2023",
        "10/26/2023",
        "10/27/2023",
    ]
    date_list = [datetime.strptime(date, "%m/%d/%Y") for date in dates_as_strings]
    start_datetimes = [
        date.replace(hour=10, minute=0, second=0, microsecond=0) for date in date_list
    ]
    end_datetimes = [
        date.replace(hour=18, minute=0, second=0, microsecond=0) for date in date_list
    ]
    for start, end in zip(start_datetimes, end_datetimes):
        entity = OperatingHoursEntity(start=start, end=end)
        session.add(entity)

    session.commit()
