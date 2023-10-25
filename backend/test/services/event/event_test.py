"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import UserPermissionException, ResourceNotFoundException

# Tested Dependencies
from ....models import Event, EventDetails
from ....services import EventService

# Injected Service Fixtures
from ..fixtures import event_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .event_test_data import (
    events,
    event_one,
    to_add,
    updated_event
)
from ..user_data import root, user

# Test Functions


def test_get_all(event_svc_integration: EventService):
    """Test that all events can be retrieved."""
    fetched_events = event_svc_integration.all()
    assert fetched_events is not None
    assert len(fetched_events) == len(events)
    assert isinstance(fetched_events[0], EventDetails)


def test_get_from_id(event_svc_integration: EventService):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_from_id(1)
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
    assert event_svc_integration.get_from_id(1).location == "Fetzer Gym"


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
        event_svc_integration.get_from_id(1)


def test_delete_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to delete events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.delete(user, 1)
