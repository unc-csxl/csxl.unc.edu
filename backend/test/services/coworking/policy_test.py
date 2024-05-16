"""Tests for Coworking Policy Service."""

from ....services.coworking import PolicyService
from .fixtures import policy_svc


from ....services.coworking.policy import OH_HOURS, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
from datetime import datetime, timedelta

__authors__ = ["Yuvraj Jain"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

def test_office_hours_monday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_monday = (today.weekday() - 0) % 7
    monday = today - timedelta(days=days_to_monday)
    assert policy_svc.office_hours(monday) == OH_HOURS[MONDAY]


def test_office_hours_tuesday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_tuesday = (today.weekday() - 1) % 7
    tuesday = today - timedelta(days=days_to_tuesday)
    assert policy_svc.office_hours(tuesday) == OH_HOURS[TUESDAY]


def test_office_hours_wednesday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_wednesday = (today.weekday() - 2) % 7
    wednesday = today - timedelta(days=days_to_wednesday)
    assert policy_svc.office_hours(wednesday) == OH_HOURS[WEDNESDAY]


def test_office_hours_thursday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_thursday = (today.weekday() - 3) % 7
    thursday = today - timedelta(days=days_to_thursday)
    assert policy_svc.office_hours(thursday) == OH_HOURS[THURSDAY]


def test_office_hours_friday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_friday = (today.weekday() - 4) % 7
    friday = today - timedelta(days=days_to_friday)
    assert policy_svc.office_hours(friday) == OH_HOURS[FRIDAY]


def test_office_hours_saturday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_saturday = (today.weekday() - 5) % 7
    saturday = today - timedelta(days=days_to_saturday)
    assert policy_svc.office_hours(saturday) == OH_HOURS[SATURDAY]


def test_office_hours_sunday(policy_svc: PolicyService):
    today = datetime.now()
    days_to_sunday = (today.weekday() - 6) % 7
    sunday = today - timedelta(days=days_to_sunday)
    assert policy_svc.office_hours(sunday) == OH_HOURS[SATURDAY]