"""Tests for Coworking Policy Service."""

from datetime import timedelta
from unittest.mock import create_autospec

from ....models import User
from ....services.coworking import PolicyService
from .fixtures import policy_svc  # noqa: F401

__authors__ = ["Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_subject_specific_duration_policies(policy_svc: PolicyService):  # noqa: F811
    subject = create_autospec(User)

    assert policy_svc.walkin_window(subject) == timedelta(minutes=10)
    assert policy_svc.walkin_initial_duration(subject) == timedelta(hours=2)
    assert policy_svc.reservation_window(subject) == timedelta(weeks=1)
    assert policy_svc.maximum_initial_reservation_duration(subject) == timedelta(
        hours=2
    )


def test_general_duration_policies(policy_svc: PolicyService):  # noqa: F811
    assert policy_svc.minimum_reservation_duration() == timedelta(minutes=10)
    assert policy_svc.reservation_draft_timeout() == timedelta(minutes=5)
    assert policy_svc.reservation_checkin_timeout() == timedelta(minutes=10)
    assert policy_svc.room_reservation_weekly_limit() == timedelta(hours=6)
