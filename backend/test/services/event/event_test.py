"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec
from backend.models.pagination import PaginationParams
from backend.models.registration_type import RegistrationType

from backend.services.exceptions import (
    EventRegistrationException,
    UserPermissionException,
    ResourceNotFoundException,
)
from backend.services.organization import OrganizationService

# Time helpers
from ....models.coworking.time_range import TimeRange
from ..coworking.time import *

# Tested Dependencies
from ....models import Event, EventDetails
from ....services import EventService

# Injected Service Fixtures
from ..fixtures import (
    user_svc_integration,
    event_svc_integration,
    organization_svc_integration,
)

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .event_test_data import (
    events,
    event_one,
    event_two,
    to_add,
    updated_event_one,
    updated_event_one_organizers,
    updated_event_two,
    updated_event_three,
    updated_event_three_remove_organizers,
    invalid_event,
    event_three,
)
from ..user_data import root, ambassador, user

# Test Functions


def test_get_all(event_svc_integration: EventService):
    """Test that all events can be retrieved."""
    fetched_events = event_svc_integration.all(ambassador)

    assert fetched_events is not None
    assert len(fetched_events) == len(events)
    assert isinstance(fetched_events[0], EventDetails)

    assert fetched_events[0].is_attendee == True
    assert fetched_events[1].is_attendee == False
    assert fetched_events[2].is_attendee == True


def test_get_all_unauthenticated(event_svc_integration: EventService):
    """Test that all events can be retrieved."""
    fetched_events = event_svc_integration.all()

    assert fetched_events is not None
    assert len(fetched_events) == len(events)
    assert isinstance(fetched_events[0], EventDetails)


def test_get_by_id(event_svc_integration: EventService):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_by_id(1, ambassador)
    assert fetched_event is not None
    assert isinstance(fetched_event, Event)
    assert fetched_event.id == event_one.id
    assert fetched_event.is_attendee == True


def test_get_by_id_unauthenticated(event_svc_integration: EventService):
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
    event_svc_integration._permission.enforce.assert_any_call(
        root, "organization.events.create", f"organization/{to_add.organization_id}"
    )


def test_create_event_as_root(event_svc_integration: EventService):
    """Test that the root user is able to create new events."""
    created_event = event_svc_integration.create(root, to_add)
    assert created_event is not None
    assert created_event.id is not None

    assert len(created_event.organizers) == 1
    assert created_event.organizers[0].id == root.id
    assert created_event.is_organizer == True

    assert len(created_event.attendees) == 0
    assert created_event.is_attendee == False


def test_create_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


def test_get_events_by_organization(
    event_svc_integration: EventService,
    organization_svc_integration: OrganizationService,
):
    """Test that list of events can be retrieved based on specified organization."""
    organization = organization_svc_integration.get_by_slug("cssg")
    fetched_events = event_svc_integration.get_events_by_organization(
        organization, ambassador
    )
    assert fetched_events is not None
    assert len(fetched_events) == 3
    assert fetched_events[0].is_attendee == True
    assert fetched_events[1].is_attendee == False
    assert fetched_events[2].is_attendee == True


def test_get_events_by_organization_organizer(
    event_svc_integration: EventService,
    organization_svc_integration: OrganizationService,
):
    """Test that list of events can be retrieved based on specified organization."""
    organization = organization_svc_integration.get_by_slug("cssg")
    fetched_events = event_svc_integration.get_events_by_organization(
        organization, user
    )
    assert fetched_events is not None
    assert len(fetched_events) == 3
    assert fetched_events[0].is_organizer == True
    assert fetched_events[1].is_organizer == False
    assert fetched_events[2].is_organizer == False


def test_get_events_by_organization_unauthenticated(
    event_svc_integration: EventService,
    organization_svc_integration: OrganizationService,
):
    """Test that list of events can be retrieved based on specified organization."""
    organization = organization_svc_integration.get_by_slug("cssg")
    fetched_events = event_svc_integration.get_events_by_organization(organization)
    assert fetched_events is not None
    assert len(fetched_events) == 3


def test_update_event_as_root(
    event_svc_integration: EventService,
):
    """Test that the root user is able to update new events.
    Note: Test data's name and location field is updated
    """
    event_svc_integration.update(root, updated_event_one)
    assert event_svc_integration.get_by_id(1).name == "Carolina Data Challenge"
    assert event_svc_integration.get_by_id(1).location == "Fetzer Gym"


def test_update_event_organizers_as_root(
    event_svc_integration: EventService,
):
    """Test that the root user is able to update new events.
    Note: Test data's name and location field is updated
    """
    event_svc_integration.update(root, updated_event_three)
    updated_organizers = event_svc_integration.get_by_id(3).organizers
    assert updated_organizers[0].id == ambassador.id
    assert updated_organizers[1].id == user.id
    assert updated_organizers[2].id == root.id

    event_svc_integration.update(root, updated_event_three_remove_organizers)
    updated_organizers = event_svc_integration.get_by_id(3).organizers
    assert len(updated_organizers) == 1
    assert updated_organizers[0].id == user.id

    event_svc_integration.update(root, updated_event_three)
    updated_organizers = event_svc_integration.get_by_id(3).organizers
    assert updated_organizers[0].id == user.id
    assert updated_organizers[1].id == ambassador.id


def test_update_event_organizers_as_user(
    event_svc_integration: EventService,
):
    """Test that the organizer user cannot update organizers.
    Note: Test data's name and location field is updated
    """
    with pytest.raises(UserPermissionException):
        event_svc_integration.update(user, updated_event_three)


def test_update_event_as_organizer(event_svc_integration: EventService):
    """Test that an organizer user is able to update events"""
    event_svc_integration.update(user, updated_event_one)
    assert event_svc_integration.get_by_id(1).name == "Carolina Data Challenge"
    assert event_svc_integration.get_by_id(1).location == "Fetzer Gym"


def test_update_event_as_user(event_svc_integration: EventService):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.update(user, updated_event_two)


def test_update_on_invalid_event(event_svc_integration: EventService):
    """Test that attempting to update a nonexistent event raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        event_svc_integration.update(user, invalid_event)


def test_delete_enforces_permission(event_svc_integration: EventService):
    """Test that the service enforces permissions when attempting to delete an event."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.delete(root, 1)
    event_svc_integration._permission.enforce.assert_called_with(
        root, "organization.events.delete", f"organization/{event_one.organization_id}"
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


def test_delete_on_invalid_event(event_svc_integration: EventService):
    """Test that attempting to delete a nonexistent event raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        event_svc_integration.delete(user, invalid_event.id)


def test_register_for_event_as_user(event_svc_integration: EventService):
    """Test that a user is able to register for an event."""
    event_details = event_svc_integration.get_by_id(event_one.id, root)  # type: ignore
    created_registration = event_svc_integration.register(root, root, event_details)  # type: ignore
    assert created_registration is not None
    assert created_registration.registration_type == RegistrationType.ATTENDEE


def test_register_for_event_as_user_twice(event_svc_integration: EventService):
    """Test that a user's second registration for an event is idempotent."""
    event_details = event_svc_integration.get_by_id(event_one.id, root)  # type: ignore
    created_registration_1 = event_svc_integration.register(user, user, event_details)  # type: ignore
    assert created_registration_1 is not None
    created_registration_2 = event_svc_integration.register(user, user, event_details)  # type: ignore
    assert created_registration_2 is not None
    assert created_registration_1 == created_registration_2


def test_register_for_event_enforces_permission(event_svc_integration: EventService):
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )
    event_details = event_svc_integration.get_by_id(event_one.id, root)  # type: ignore
    event_svc_integration.register(root, user, event_details)  # type: ignore
    event_svc_integration._permission.enforce.assert_any_call(
        root,
        "organization.events.manage_registrations",
        f"organization/{event_details.organization.id}",
    )


def test_get_registration(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id, ambassador)  # type: ignore
    event_registration = event_svc_integration.get_registration(
        ambassador, ambassador, event_details
    )
    assert event_registration is not None


def test_get_registration_that_does_not_exist(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id, root)  # type: ignore
    event_registration = event_svc_integration.get_registration(
        root, root, event_details
    )
    assert event_registration is None


def test_get_registrations_of_event_as_organizer(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id, user)  # type: ignore
    event_registrations = event_svc_integration.get_registrations_of_event(
        user, event_details
    )
    assert len(event_registrations) == 2


def test_get_registrations_of_event_non_organizer(event_svc_integration: EventService):
    event_details = event_svc_integration.get_by_id(event_one.id, ambassador)  # type: ignore
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
    event_details = event_svc_integration.get_by_id(event_one.id, ambassador)  # type: ignore
    event_svc_integration.get_registrations_of_event(ambassador, event_details)

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        ambassador,
        "organization.events.manage_registrations",
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
    event_details = event_svc_integration.get_by_id(event_one.id, root)  # type: ignore
    event_svc_integration.unregister(root, ambassador, event_details)

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        root,
        "organization.events.manage_registrations",
        f"organization/{event_one.organization_id}",
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
        start=event_one.time + 2 * ONE_DAY, end=event_one.time + 3 * ONE_DAY
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


def test_register_to_full_event(
    event_svc_integration: EventService,
):
    """Tests that a user cannot register for an event that is full."""
    event_details = event_svc_integration.get_by_id(event_three.id)  # type: ignore

    with pytest.raises(EventRegistrationException):
        event_svc_integration.register(user, user, event_details)


def test_get_registered_users_of_event(event_svc_integration: EventService):
    """Tests querying for registered users of events as a paginated list"""
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter=""
    )
    page = event_svc_integration.get_registered_users_of_event(
        root, event_one.id, pagination_params
    )

    assert len(page.items) == 2
    assert page.length == 2
    assert page.items[0].id == ambassador.id
    assert page.items[1].id == user.id


def test_organizer_get_registered_users_of_event(event_svc_integration: EventService):
    """Tests that organizers for an event can retrieve registered users"""
    # Setup to test permission enforcement on the PermissionService.
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter=""
    )
    page = event_svc_integration.get_registered_users_of_event(
        user, event_one.id, pagination_params
    )

    assert len(page.items) == 2
    assert page.length == 2
    assert page.items[0].id == ambassador.id
    assert page.items[1].id == user.id


def test_organizer_get_registered_users_of_event_filtered(
    event_svc_integration: EventService,
):
    """Tests that organizers for an event can retrieve registered users"""
    # Setup to test permission enforcement on the PermissionService.
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter="Amy"
    )
    page = event_svc_integration.get_registered_users_of_event(
        user, event_one.id, pagination_params
    )

    assert len(page.items) == 1
    assert page.length == 1
    assert page.items[0].id == ambassador.id


def test_get_registered_users_of_event_permissions(event_svc_integration: EventService):
    """Tests that the service method for retrieving registered users of an event enforces permissions"""
    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter=""
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.get_registered_users_of_event(
        root, event_one.id, pagination_params
    )
    event_svc_integration._permission.enforce.assert_called_with(
        root,
        "organization.events.manage_registrations",
        f"organization/{event_one.organization_id}",
    )


def test_get_registered_users_of_event_without_permissions(
    event_svc_integration: EventService,
):
    """Tests that the service method for retrieving registered users of an event enforces permissions"""
    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter=""
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.get_registered_users_of_event(
        user, event_two.id, pagination_params
    )
    event_svc_integration._permission.enforce.assert_called_with(
        user,
        "organization.events.manage_registrations",
        f"organization/{event_one.organization_id}",
    )
