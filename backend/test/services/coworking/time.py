"""Commonly used time constants for testing purposes."""

import pytest
from datetime import datetime, timedelta

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Durations
ZERO_TIME = timedelta(0)
TIME_EPSILON = timedelta(seconds=5)  # Used for testing tolerances
ONE_MINUTE = timedelta(minutes=1)
FIVE_MINUTES = timedelta(minutes=5)
TEN_MINUTES = timedelta(minutes=10)
THIRTY_MINUTES = timedelta(minutes=30)
ONE_HOUR = timedelta(hours=1)
ONE_DAY = timedelta(days=1)

# Constants are keys to the times fixture
NOW = "NOW"
MIDNIGHT_TODAY = "MIDNIGHT_TODAY"
# Past
A_WEEK_AGO = "A_WEEK_AGO"
AN_HOUR_AGO = "AN_HOUR_AGO"
THIRTY_MINUTES_AGO = "THIRTY_MINUTES_AGO"
# Future
MIDNIGHT_TOMORROW = "MIDNIGHT_TOMORROW"
IN_TEN_MINUTES = "IN_TEN_MINUTES"
IN_THIRTY_MINUTES = "IN_THIRTY_MINUTES"
TOMORROW = "TOMORROW"
IN_ONE_HOUR = "IN_ONE_HOUR"
IN_TWO_HOURS = "IN_TWO_HOURS"
IN_THREE_HOURS = "IN_THREE_HOURS"
IN_EIGHT_HOURS = "IN_EIGHT_HOURS"


@pytest.fixture()
def time() -> dict[str, datetime]:
    """This fixture returns a dictionary of string constants defined above mapped to corresponding date times.

    It is implemented as a fixture, rather than a static dictionary, because we'd like these datetimes to be generated
    at the moment each tests runs rather than at the start of running the test suite. This was a lesson learned the hard
    way. The simpler solution, simply defining these values as global constants, breaks down for much longer test runs
    which our application has begun to need for its whole test suite."""
    return time_data()


def time_data() -> dict[str, datetime]:
    """Separated out as a standalone function from its fixture such that it can be called during reset database script."""
    now = datetime.now()
    return {
        # Times
        NOW: now,
        MIDNIGHT_TODAY: now.replace(hour=0, minute=0, second=0, microsecond=0),
        # Past
        A_WEEK_AGO: now - 7 * ONE_DAY,
        AN_HOUR_AGO: now - ONE_HOUR,
        THIRTY_MINUTES_AGO: now - THIRTY_MINUTES,
        # Future
        MIDNIGHT_TOMORROW: (now + ONE_DAY).replace(
            hour=0, minute=0, second=0, microsecond=0
        ),
        IN_TEN_MINUTES: now + TEN_MINUTES,
        IN_THIRTY_MINUTES: now + THIRTY_MINUTES,
        TOMORROW: now + ONE_DAY,
        IN_ONE_HOUR: now + ONE_HOUR,
        IN_TWO_HOURS: now + 2 * ONE_HOUR,
        IN_THREE_HOURS: now + 3 * ONE_HOUR,
        IN_EIGHT_HOURS: now + 8 * ONE_HOUR,
    }


def assert_equal_times(expected: datetime, actual: datetime):
    assert ZERO_TIME <= abs(expected - actual) < TIME_EPSILON
