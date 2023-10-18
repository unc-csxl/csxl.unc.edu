"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.organization import OrganizationNotFoundException
from backend.services.permission import UserPermissionException

# Tested Dependencies
from ....models import Event
from ....services import EventService

# Injected Service Fixtures
from ..fixtures import event_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .event_test_data import (
    events,
    event_one,
    event_two,
)
from ..user_data import root, user

# Test Functions

# Test `EventService.all()`
def test_get_all(event_svc_integration: EventService):
    """Test that all events can be retrieved."""
    fetched_events = event_svc_integration.all()
    assert fetched_events is not None
    assert len(fetched_events) == len(events)
    assert isinstance(fetched_events[0], Event)


# Test `EventService.get_from_id()`
def test_get_from_slug(event_svc_integration: EventService):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_from_id(event_one.id)
    assert fetched_event is not None
    assert isinstance(fetched_event, Event)
    assert fetched_event.id == event_one.id

# Test `EventService.create()`
def test_create_enforces_permission(event_svc_integration: EventService):
    """Test that the service enforces permissions when attempting to create an event."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.create(root, to_add)
    event_svc_integration._permission.enforce.assert_called_with(
        root, "organization.create", "organization"
    )


def test_create_organization_as_root(event_svc_integration: EventService):
    """Test that the root user is able to create new organizations."""
    created_organization = event_svc_integration.create(root, to_add)
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new organizations."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


# Test `EventService.update()`


# def test_update_organization_as_leader(
#     event_svc_integration: EventService,
# ):
#     """Test that the root user is able to create new organizations.
#     Note: Test data's website field is updated
#     """
#     cads = event_svc_integration.get_from_id(1)
#     cads.website = "https://cads.cs.unc.edu/"
#     updated_organization = event_svc_integration.update(cads_leader, cads)
#     assert updated_organization is not None
#     assert updated_organization.id is not None
#     assert updated_organization.website == "https://cads.cs.unc.edu/"


def test_update_organization_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new organizations."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.update(user, new_cads)


def test_delete_enforces_permission(event_svc_integration: EventService):
    """Test that the service enforces permissions when attempting to delete an organization."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.delete(root, cads.slug)
    event_svc_integration._permission.enforce.assert_called_with(
        root, "organization.create", "organization"
    )


def test_delete_organization_as_root(event_svc_integration: EventService):
    """Test that the root user is able to delete organizations."""
    event_svc_integration.delete(root, cads.slug)
    with pytest.raises(OrganizationNotFoundException):
        event_svc_integration.get_from_slug(cads.slug)


def test_delete_organization_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to delete organizations."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.delete(user, cads.slug)
