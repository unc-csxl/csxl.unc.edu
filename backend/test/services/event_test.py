"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

# Tested Dependencies
from ...models import EventDetail
from ...services import EventService

# Injected Service Fixtures
from .fixtures import event_svc_integration

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .event_data import events, cads_event, time_range, to_add, new_cads

from .organization_data import cads_leader, cads

from .user_data import user

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `EventService.all()`


def test_get_all(event_svc_integration: EventService):
    """Test that all events can be retrieved."""
    fetched_events = event_svc_integration.all()
    assert fetched_events is not None
    assert len(fetched_events) == len(events)
    assert isinstance(fetched_events[0], EventDetail)


# Test `EventService.get_from_id()`


def test_get_from_id(event_svc_integration: EventService):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_from_id(cads_event.id)
    assert fetched_event is not None
    assert isinstance(fetched_event, EventDetail)
    assert fetched_event.id == cads_event.id


# Test `EventService.get_from_org_id()`


def test_get_from_org_id(event_svc_integration: EventService):
    """Test that events can be retrieved based on an organization ID."""
    fetched_events = event_svc_integration.get_from_org_id(cads.id)
    assert fetched_events is not None
    assert len(fetched_events) == 1
    assert isinstance(fetched_events[0], EventDetail)


# Test `EventService.get_from_time_range()`


def test_get_from_time_range(event_svc_integration: EventService):
    """Test that events can be retrieved based on a given time range."""
    fetched_events = event_svc_integration.get_from_time_range(
        time_range[0], time_range[1]
    )
    assert fetched_events is not None
    assert len(fetched_events) == 1
    assert isinstance(fetched_events[0], EventDetail)
    assert fetched_events[0].id == cads_event.id


# Test `EventService.create()`


def test_create_event_as_leader(event_svc_integration: EventService):
    """Test that the leader user is able to create new events."""
    created_event = event_svc_integration.create(cads_leader, to_add)
    assert created_event is not None
    assert created_event.id is not None


def test_create_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    try:
        event_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected


# Test `EventService.update()`


def test_update_event_as_leader(
    event_svc_integration: EventService,
):
    """Test that the leader user is able to create new events for their orgs.
    Note: Test data's location field is updated
    """
    updated_event = event_svc_integration.update(cads_leader, new_cads)
    assert updated_event is not None
    assert updated_event.id is not None
    assert updated_event.location == new_cads.location


def test_update_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    try:
        event_svc_integration.update(user, new_cads)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected


# Test `EventService.delete()`


def test_delete_event_as_leader(event_svc_integration: EventService):
    """Test that the leader user is able to delete events for their orgs."""
    event_svc_integration.delete(cads_leader, cads_event.id)

    try:
        event_svc_integration.get_from_id(cads_event.id)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because an error was thrown when we found no organization


def test_delete_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to delete events."""
    try:
        event_svc_integration.delete(user, cads_event.id)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected
