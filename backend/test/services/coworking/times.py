"""Commonly used time constants for testing purposes."""
from datetime import datetime, timedelta

# Durations
ZERO_TIME = timedelta(0)  # Used for testing tolerances
TIME_EPSILON = timedelta(seconds=5)  # Used for testing tolerances
ONE_MINUTE = timedelta(minutes=1)
FIVE_MINUTES = timedelta(minutes=5)
THIRTY_MINUTES = timedelta(minutes=30)
ONE_HOUR = timedelta(hours=1)
ONE_DAY = timedelta(days=1)

NOW = datetime.now()

# Past
A_WEEK_AGO = NOW - 7 * ONE_DAY
AN_HOUR_AGO = NOW - ONE_HOUR
THIRTY_MINUTES_AGO = NOW - THIRTY_MINUTES

# Future
IN_THIRTY_MINUTES = NOW + THIRTY_MINUTES
TOMORROW = NOW + ONE_DAY
IN_ONE_HOUR = NOW + ONE_HOUR
IN_TWO_HOURS = NOW + 2 * ONE_HOUR


def assert_equal_times(expected: datetime, actual: datetime):
    assert ZERO_TIME <= abs(expected - actual) < TIME_EPSILON
