"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    EventRegistrationException,
    UserPermissionException,
    ResourceNotFoundException,
)

# Time helpers
from ....models.coworking.time_range import TimeRange
from ..coworking.time import *

# Tested Dependencies
from ....models import Event, EventDetails
from ....services import EventService

# Injected Service Fixtures
from ..fixtures import user_svc_integration, event_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .event_test_data import (
    events,
    event_one,
    to_add,
    updated_event,
    registrations,
    event_three,
)
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
    assert len(created_event.registrations) == 1
    assert created_event.registrations[0].is_organizer == True
    assert created_event.registrations[0].user_id == root.id


def test_create_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


def test_get_events_by_organization(event_svc_integration: EventService):
    """Test that list of events can be retrieved based on specified organization."""
    fetched_events = event_svc_integration.get_events_by_organization("cssg")
    assert fetched_events is not None
    assert len(fetched_events) == 3


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


def test_get_registration_that_does_not_exist(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_registration = event_svc_integration.get_registration(
        root, root, event_details
    )
    assert event_registration is None


def test_is_user_an_organizer_organizer(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    assert event_svc_integration.is_user_an_organizer(user, event_details)


def test_is_user_an_organizer_attendee(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    assert not event_svc_integration.is_user_an_organizer(ambassador, event_details)


def test_is_user_an_organizer_non_attendee(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    assert not event_svc_integration.is_user_an_organizer(root, event_details)


def test_get_registrations_of_event_as_organizer(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_registrations = event_svc_integration.get_registrations_of_event(
        user, event_details
    )
    assert len(event_registrations) == 2


def test_get_registrations_of_event_non_organizer(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    with pytest.raises(UserPermissionException):
        event_svc_integration.get_registrations_of_event(ambassador, event_details)


def test_get_registrations_enforces_admin_auth(
    event_svc_integration: EventService,
):
    """Test that root is able to delete any registrations."""
    # Setup mock to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Ensure delete occurs
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_svc_integration.get_registrations_of_event(ambassador, event_details)

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        ambassador,
        "organization.events.manage",
        f"organization/{event_one.organization_id}",
    )


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


def test_unregister_for_event_as_registerer_is_idempotent(
    event_svc_integration: EventService,
):
    """Test that a user is able to unregister for an event."""
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    event_svc_integration.unregister(ambassador, ambassador, event_details)
    event_svc_integration.unregister(ambassador, ambassador, event_details)
    assert (
        event_svc_integration.get_registration(ambassador, ambassador, event_details)
        is None
    )


def test_unregister_for_event_as_wrong_user(
    event_svc_integration: EventService,
):
    """Test that any user is *unable* to delete a registration that is not for them."""
    event_details = event_svc_integration.get_by_id(event_one.id)  # type: ignore
    with pytest.raises(UserPermissionException):
        event_svc_integration.unregister(user, ambassador, event_details)


def test_unregister_for_event_enforces_admin_auth(
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


def test_get_registrations_of_user(
    event_svc_integration: EventService, time: dict[str, datetime]
):
    """Test that a user with a registration is able to query for it."""
    time_range = TimeRange(start=event_one.time - ONE_DAY, end=event_one.time + ONE_DAY)
    registrations = event_svc_integration.get_registrations_of_user(
        ambassador, ambassador, time_range
    )
    assert len(registrations) == 1


def test_get_registrations_of_user_outside_time_range(
    event_svc_integration: EventService, time: dict[str, datetime]
):
    """Test that a user with a registration is able to query for it."""
    # Test range after event
    time_range = TimeRange(
        start=event_one.time + ONE_DAY, end=event_one.time + 2 * ONE_DAY
    )
    registrations = event_svc_integration.get_registrations_of_user(
        ambassador, ambassador, time_range
    )
    assert len(registrations) == 0

    # Test range before event
    time_range = TimeRange(
        start=event_one.time - ONE_DAY * 2, end=event_one.time - ONE_DAY
    )
    registrations = event_svc_integration.get_registrations_of_user(
        ambassador, ambassador, time_range
    )
    assert len(registrations) == 0


def test_get_registrations_of_user_without_reservations(
    event_svc_integration: EventService, time: dict[str, datetime]
):
    """Test that a user without any registrations is able to query for it."""
    time_range = TimeRange(start=event_one.time - ONE_DAY, end=event_one.time + ONE_DAY)
    registrations = event_svc_integration.get_registrations_of_user(
        root, root, time_range
    )
    assert len(registrations) == 0


def test_get_registrations_of_user_admin_authorization(
    event_svc_integration: EventService,
):
    """Test that administrative permissions are enforced."""
    # Setup mock to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Ensure delete occurs
    time_range = TimeRange(start=event_one.time - ONE_DAY, end=event_one.time + ONE_DAY)
    event_svc_integration.get_registrations_of_user(root, ambassador, time_range)

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        root, "user.event_registrations", f"user/{ambassador.id}"
    )


def test_get_event_registration_status(
    event_svc_integration: EventService,
):
    """Tests that the service can successfully count events for an organization."""
    if event_one.id:
        status = event_svc_integration.get_event_registration_status(event_one.id)
        assert status.registration_count == 1


def test_register_to_full_event(
    event_svc_integration: EventService,
):
    """Tests that a user cannot register for an event that is full."""
    event_details = event_svc_integration.get_by_id(event_three.id)  # type: ignore

    with pytest.raises(EventRegistrationException):
        event_svc_integration.register(user, user, event_details)
