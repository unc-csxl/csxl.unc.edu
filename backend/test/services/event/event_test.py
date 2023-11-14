"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ....models import Event, EventDetails
from ....services import EventService

# Injected Service Fixtures
from ..fixtures import user_svc_integration, event_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .event_test_data import events, event_one, to_add, updated_event, registration
from ..user_data import root, ambassador, user

# Test Functions


def test_get_all(event_svc_integration: EventService):
    """Test that all events can be retrieved."""
    fetched_events = event_svc_integration.all()
    assert fetched_events is not None
    assert len(fetched_events) == len(events)
    assert isinstance(fetched_events[0], EventDetails)


def test_get_by_id(event_svc_integration: EventService):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_by_id(1)
    assert fetched_event is not None
    assert isinstance(fetched_event, Event)
    assert fetched_event.id == event_one.id


def test_create_enforces_permission(event_svc_integration: EventService):
    """Test that the service enforces permissions when attempting to create an event."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.create(root, to_add)
    event_svc_integration._permission.enforce.assert_called_with(
        root, "organization.events.manage", f"organization/{to_add.organization_id}"
    )


def test_create_event_as_root(event_svc_integration: EventService):
    """Test that the root user is able to create new events."""
    created_event = event_svc_integration.create(root, to_add)
    assert created_event is not None
    assert created_event.id is not None


def test_create_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


def test_get_events_from_organization(event_svc_integration: EventService):
    """Test that list of events can be retrieved based on specified organization."""
    fetched_events = event_svc_integration.get_events_from_organization("cssg")
    assert fetched_events is not None
    assert len(fetched_events) == 2


def test_update_event_as_root(
    event_svc_integration: EventService,
):
    """Test that the root user is able to create new events.
    Note: Test data's website field is updated
    """
    event_svc_integration.update(root, updated_event)
    assert event_svc_integration.get_by_id(1).location == "Fetzer Gym"


def test_update_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.update(user, updated_event)


def test_delete_enforces_permission(event_svc_integration: EventService):
    """Test that the service enforces permissions when attempting to delete an event."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.delete(root, 1)
    event_svc_integration._permission.enforce.assert_called_with(
        root, "organization.events.manage", f"organization/{event_one.organization_id}"
    )


def test_delete_event_as_root(event_svc_integration: EventService):
    """Test that the root user is able to delete events."""
    event_svc_integration.delete(root, 1)
    with pytest.raises(ResourceNotFoundException):
        event_svc_integration.get_by_id(1)


def test_delete_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to delete events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.delete(user, 1)


def test_register_for_event_as_user(event_svc_integration: EventService):
    """Test that a user is able to register for an event."""
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    created_registration = event_svc_integration.register(user, user, event_details)  # type: ignore
    assert created_registration is not None
    assert created_registration.user_id == user.id
    assert created_registration.event_id == event_one.id


def test_register_for_event_as_user_twice(event_svc_integration: EventService):
    """Test that a user's second registration for an event is idempotent."""
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    created_registration_1 = event_svc_integration.register(user, user, event_details)  # type: ignore
    assert created_registration_1 is not None
    created_registration_2 = event_svc_integration.register(user, user, event_details)  # type: ignore
    assert created_registration_2 is not None
    assert created_registration_1.id == created_registration_2.id


def test_register_for_event_enforces_permission(event_svc_integration: EventService):
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_svc_integration.register(root, user, event_details)  # type: ignore
    event_svc_integration._permission.enforce.assert_called_with(
        root,
        "organization.events.manage",
        f"organization/{event_details.organization.id}",
    )


def test_get_registration(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_registration = event_svc_integration.get_registration(
        ambassador, ambassador, event_details
    )
    assert event_registration is not None
    assert event_registration.id is registration.id


def test_get_registration_that_does_not_exist(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_registration = event_svc_integration.get_registration(
        user, user, event_details
    )
    assert event_registration is None


def test_unregister_for_event_as_registerer(
    event_svc_integration: EventService,
):
    """Test that a user is able to unregister for an event."""
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    assert (
        event_svc_integration.get_registration(ambassador, ambassador, event_details)
        is not None
    )
    event_svc_integration.unregister(ambassador, ambassador, event_details)
    assert (
        event_svc_integration.get_registration(ambassador, ambassador, event_details)
        is None
    )


def test_delete_registration_for_event_as_wrong_user(
    event_svc_integration: EventService,
):
    """Test that any user is *unable* to delete a registration that is not for them."""
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    with pytest.raises(UserPermissionException):
        event_svc_integration.unregister(user, ambassador, event_details)


def test_delete_registration_for_event_as_root(
    event_svc_integration: EventService,
):
    """Test that root is able to delete any registrations."""
    # Setup mock to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Ensure delete occurs
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_svc_integration.unregister(root, ambassador, event_details)

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        root, "organization.events.manage", f"organization/{event_one.organization_id}"
    )
