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

from backend.entities.coworking.operating_hours_recurrence_entity import (
    OperatingHoursRecurrenceEntity,
)
from backend.models.coworking.operating_hours import OperatingHoursRecurrence
from backend.services.coworking.operating_hours import OperatingHoursService
from backend.test.services.coworking.fixtures import operating_hours_svc
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
future_monday: OperatingHours
tuesday_recurring: OperatingHours
all: list[OperatingHours] = []


def insert_fake_data(
    session: Session,
    time: dict[str, datetime],
    operating_hours_svc: OperatingHoursService,
):
    """Fake data insert factored out of the fixture for use in dev reset scripts."""

    # We're definining these values here so that they can depend on times generated per
    # test run.
    global today, future, tomorrow, three_days_from_today, future_monday, tuesday_recurring, all

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
        id=4,
        start=time[AN_HOUR_AGO] + 3 * ONE_DAY,
        end=time[IN_EIGHT_HOURS] + 3 * ONE_DAY,
    )

    future_monday = OperatingHours(
        id=5,
        start=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        + timedelta(days=21 - datetime.now().weekday()),
        end=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
        + timedelta(days=21 - datetime.now().weekday()),
    )

    tuesday_recurring = OperatingHours(
        id=6,
        start=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        + timedelta(days=15 - datetime.now().weekday()),
        end=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
        + timedelta(days=15 - datetime.now().weekday()),
        recurrence=OperatingHoursRecurrence(
            end_date=datetime.now() + timedelta(days=50), recurs_on=0b00010
        ),
    )

    all = [
        today,
        future,
        tomorrow,
        three_days_from_today,
        future_monday,
        tuesday_recurring,
    ]

    for operating_hours in all:
        entity = OperatingHoursEntity.from_model(operating_hours)
        session.add(entity)

        if operating_hours.recurrence:
            operating_hours_svc._create_recurring_hours(
                operating_hours, entity.recurrence
            )

    reset_table_id_seq(
        session, OperatingHoursEntity, OperatingHoursEntity.id, len(all) + 1
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(
    session: Session,
    time: dict[str, datetime],
    operating_hours_svc: OperatingHoursService,
):
    insert_fake_data(session, time, operating_hours_svc)
    session.commit()
    yield


def delete_all(session: Session):
    session.execute(delete(OperatingHoursEntity))
    session.execute(delete(OperatingHoursRecurrenceEntity))
