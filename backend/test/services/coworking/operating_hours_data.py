"""Data for operating hours tests.

Three days worth of operating hours are setup:

1. today
2. future (two days in the future)
3. tomorrow

Each opens one hour before the module evalues and ends one hour after.
"""

import pytest
from sqlalchemy import delete
from sqlalchemy.orm import Session
from ....entities.coworking import OperatingHoursEntity
from ....models.coworking import OperatingHours
from ..reset_table_id_seq import reset_table_id_seq
from .time import *

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

today: OperatingHours
tomorrow: OperatingHours
future: OperatingHours
three_days_from_today: OperatingHours
all: list[OperatingHours] = []


def insert_fake_data(session: Session, time: dict[str, datetime]):
    """Fake data insert factored out of the fixture for use in dev reset scripts."""

    # We're definining these values here so that they can depend on times generated per
    # test run.
    global today, future, tomorrow, three_days_from_today, all

    today = OperatingHours(id=1, start=time[AN_HOUR_AGO], end=time[IN_THREE_HOURS])

    future = OperatingHours(
        id=2,
        start=time[AN_HOUR_AGO] + 2 * ONE_DAY,
        end=time[IN_TWO_HOURS] + 2 * ONE_DAY,
    )
    # Intentionally mis-ordering the insertion ID of tomorrow vs. future to test orderings in API
    tomorrow = OperatingHours(
        id=3, start=time[AN_HOUR_AGO] + ONE_DAY, end=time[IN_TWO_HOURS] + ONE_DAY
    )

    three_days_from_today = OperatingHours(
        id=4, start=time[AN_HOUR_AGO] + 3 * ONE_DAY, end=time[IN_EIGHT_HOURS] + 3 * ONE_DAY
    )

    all = [today, future, tomorrow, three_days_from_today]


    for operating_hours in all:
        entity = OperatingHoursEntity.from_model(operating_hours)
        session.add(entity)

    reset_table_id_seq(
        session, OperatingHoursEntity, OperatingHoursEntity.id, len(all) + 1
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session, time: dict[str, datetime]):
    insert_fake_data(session, time)
    session.commit()
    yield


def delete_all(session: Session):
    session.execute(delete(OperatingHoursEntity))
