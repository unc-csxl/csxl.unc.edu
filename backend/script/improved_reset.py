# The purpose of this improved reset script is to make use of our conventions
# also built around unit and backend integration testing.

# Previously, we duplicated data between testing and this database reset.
# Moving forward, we'll aim to have some parity between tests and dev reset.
# This way, we both avoid duplication and make it easier to interact with
# the state of the system we are writing tests for.

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

from ..test.services.coworking import room_data, seat_data, reservation_data, operating_hours_data, user_data

if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)


with Session(engine) as session:
    user_data.insert_fake_data(session)
    operating_hours_data.insert_fake_data(session)
    room_data.insert_fake_data(session)
    seat_data.insert_fake_data(session)
    reservation_data.insert_fake_data(session)
    session.commit()