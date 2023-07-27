"""Tests for the RegistrationService class."""

# PyTest
import pytest

# Tested Dependencies
from ...models import RegistrationDetail
from ...services import RegistrationService

# Injected Service Fixtures
from .fixtures import registration_svc_integration

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .registration_data import registrations, user_cdc_registration, to_add
from .event_data import cads_event
from .user_data import user, cads_leader, ambassador

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `RegistrationService.all()`


def test_get_all(registration_svc_integration: RegistrationService):
    """Test that all registrations can be retrieved."""
    fetched_registrations = registration_svc_integration.all()
    assert fetched_registrations is not None
    assert len(fetched_registrations) == len(registrations)
    assert isinstance(fetched_registrations[0], RegistrationDetail)


# Test `RegistrationService.get_by_user()`


def test_get_by_user(registration_svc_integration: RegistrationService):
    """Test that registrations can be retrieved based on a given user ID."""
    fetched_registrations = registration_svc_integration.get_by_user(user.id, 0)
    assert fetched_registrations is not None
    assert len(fetched_registrations) == 1
    assert isinstance(fetched_registrations[0], RegistrationDetail)
    assert fetched_registrations[0].user_id == user.id


# Test `RegistrationService.get_by_event()`


def test_get_by_event(registration_svc_integration: RegistrationService):
    """Test that registrations can be retrieved based on a given event ID."""
    fetched_registrations = registration_svc_integration.get_by_event(cads_event.id, 0)
    assert fetched_registrations is not None
    assert len(fetched_registrations) == 1
    assert isinstance(fetched_registrations[0], RegistrationDetail)
    assert fetched_registrations[0].user_id == user.id


# Test `RegistrationService.create()`


def test_create_registration_as_self(registration_svc_integration: RegistrationService):
    """Test that the user is able to create new registrations for themself."""
    created_registration = registration_svc_integration.create(user, to_add)
    assert created_registration is not None
    assert created_registration.id is not None


def test_create_registration_as_not_self(
    registration_svc_integration: RegistrationService,
):
    """Test that any user is *unable* to create new registrations for other people."""
    try:
        registration_svc_integration.create(ambassador, to_add)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected


# Test `RegistrationService.update_status()`


def test_update_registration_as_leader(
    registration_svc_integration: RegistrationService,
):
    """Test that an org leader is able to update the status of their orgs registrations."""
    original_registration = registration_svc_integration.get_by_user(user.id, 0)[0]
    updated_registration = registration_svc_integration.update_status(
        cads_leader, original_registration
    )
    assert updated_registration is not None
    assert updated_registration.id is not None
    assert updated_registration.status == 1


def test_update_registration_as_not_leader(
    registration_svc_integration: RegistrationService,
):
    """Test that any nobody except the leader can update the status of a registration."""
    try:
        original_registration = registration_svc_integration.get_by_user(user.id, 0)[0]
        registration_svc_integration.update_status(user, original_registration)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected


# Test `RegistrationService.delete()`


def test_delete_registration_as_self(registration_svc_integration: RegistrationService):
    """Test that the user is able to delete registrations for themself."""
    try:
        registration_svc_integration.delete_registration(user, user_cdc_registration.id)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because an error was thrown when we found no registration


def test_delete_registration_as_not_self(
    registration_svc_integration: RegistrationService,
):
    """Test that any user is *unable* to delete registrations for other people."""
    try:
        registration_svc_integration.delete_registration(
            ambassador, user_cdc_registration.id
        )
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected
