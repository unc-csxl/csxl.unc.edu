"""Tests for the EventService class."""

# PyTest
import pytest
from unittest.mock import create_autospec
from backend.models.pagination import PaginationParams
from sqlalchemy.orm import Session

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
from ....models import EventDraft, EventOverview, EventPaginationParams
from ....services import EventService

# Injected Service Fixtures
from ..fixtures import event_svc_integration, user_svc_integration
from .scenario import EventScenario, arrange_event_scenario, date_maker


@pytest.fixture()
def event_scenario(session: Session) -> EventScenario:
    return arrange_event_scenario(session)

# Test Functions


def test_get_by_id(event_svc_integration: EventService, event_scenario: EventScenario):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_by_id(1, event_scenario.auth.ambassador)
    assert fetched_event is not None
    assert isinstance(fetched_event, EventOverview)
    assert fetched_event.id == event_scenario.event_one.id


def test_get_by_id_unauthenticated(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that events can be retrieved based on their ID."""
    fetched_event = event_svc_integration.get_by_id(1)
    assert fetched_event is not None
    assert isinstance(fetched_event, EventOverview)
    assert fetched_event.id == event_scenario.event_one.id


def test_list(event_svc_integration: EventService, event_scenario: EventScenario):
    """Test that a paginated list of events can be produced."""
    pagination_params = EventPaginationParams(
        order_by="id",
        range_start=date_maker(days_in_future=1, hour=10, minutes=0).isoformat(),
        range_end=date_maker(days_in_future=2, hour=10, minutes=0).isoformat(),
    )
    fetched_events = event_svc_integration.get_paginated_events(
        pagination_params, event_scenario.auth.ambassador
    )
    assert len(fetched_events.items) == 1


def test_list_filter(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that a paginated list of events can be produced."""
    pagination_params = EventPaginationParams(filter="Workshop")
    fetched_events = event_svc_integration.get_paginated_events(
        pagination_params, event_scenario.auth.ambassador
    )
    assert len(fetched_events.items) == 1


def test_create_enforces_permission(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that the service enforces permissions when attempting to create an event."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.create(event_scenario.auth.root, event_scenario.to_add)
    event_svc_integration._permission.enforce.assert_any_call(
        event_scenario.auth.root,
        "organization.events.create",
        f"organization/{event_scenario.organizations.cads.id}",
    )


def test_create_event_as_root(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that the root user is able to create new events."""
    created_event = event_svc_integration.create(
        event_scenario.auth.root, event_scenario.to_add
    )
    assert created_event is not None
    assert created_event.id is not None

    assert len(created_event.organizers) == 1
    assert created_event.organizers[0].id == event_scenario.auth.root.id


def test_create_event_as_user(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.create(event_scenario.auth.user, event_scenario.to_add)
        pytest.fail()  # Fail test if no error was thrown above


def test_update_event_as_root(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that the root user is able to update new events.
    Note: Test data's name and location field is updated
    """
    event_svc_integration.update(
        event_scenario.auth.root, event_scenario.updated_event_one
    )
    assert event_svc_integration.get_by_id(1).name == "Carolina Data Challenge"
    assert event_svc_integration.get_by_id(1).location == "Fetzer Gym"


def test_update_event_organizers_as_root(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that the root user is able to update new events.
    Note: Test data's name and location field is updated
    """
    event_svc_integration.update(
        event_scenario.auth.root, event_scenario.updated_event_three
    )
    updated_organizers = event_svc_integration.get_by_id(3).organizers
    assert len(updated_organizers) == 3

    event_svc_integration.update(
        event_scenario.auth.root,
        event_scenario.updated_event_three_remove_organizers,
    )
    updated_organizers = event_svc_integration.get_by_id(3).organizers
    assert len(updated_organizers) == 1

    event_svc_integration.update(
        event_scenario.auth.root, event_scenario.updated_event_three
    )
    updated_organizers = event_svc_integration.get_by_id(3).organizers
    assert len(updated_organizers) == 3


def test_update_event_organizers_as_user(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that the organizer user cannot update organizers.
    Note: Test data's name and location field is updated
    """
    with pytest.raises(UserPermissionException):
        event_svc_integration.update(
            event_scenario.auth.user, event_scenario.updated_event_three
        )


def test_update_event_as_organizer(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that an organizer user is able to update events"""
    event_svc_integration.update(
        event_scenario.auth.user, event_scenario.updated_event_one
    )
    assert event_svc_integration.get_by_id(1).name == "Carolina Data Challenge"
    assert event_svc_integration.get_by_id(1).location == "Fetzer Gym"


def test_update_event_as_user(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that any user is *unable* to create new events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.update(
            event_scenario.auth.user, event_scenario.updated_event_two
        )


def test_update_on_invalid_event(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that attempting to update a nonexistent event raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        event_svc_integration.update(
            event_scenario.auth.user, event_scenario.invalid_event
        )


def test_delete_enforces_permission(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that the service enforces permissions when attempting to delete an event."""

    # Setup to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    event_svc_integration.delete(event_scenario.auth.root, 1)
    event_svc_integration._permission.enforce.assert_called_with(
        event_scenario.auth.root,
        "organization.events.delete",
        f"organization/{event_scenario.organizations.cssg.id}",
    )


def test_delete_event_as_root(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that the root user is able to delete events."""
    event_svc_integration.delete(event_scenario.auth.root, 1)
    with pytest.raises(ResourceNotFoundException):
        event_svc_integration.get_by_id(1)


def test_delete_event_as_user(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that any user is *unable* to delete events."""
    with pytest.raises(UserPermissionException):
        event_svc_integration.delete(event_scenario.auth.user, 1)


def test_delete_on_invalid_event(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that attempting to delete a nonexistent event raises an exception."""
    with pytest.raises(ResourceNotFoundException):
        event_svc_integration.delete(
            event_scenario.auth.user, event_scenario.invalid_event.id
        )


def test_register_for_event_as_user(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that a user is able to register for an event."""
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.root
    )
    created_registration = event_svc_integration.register(
        event_scenario.auth.root,
        event_scenario.auth.root,
        event_details,
    )
    assert created_registration is not None


def test_register_for_event_as_user_twice(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Test that a user's second registration for an event is idempotent."""
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.root
    )
    created_registration_1 = event_svc_integration.register(
        event_scenario.auth.user,
        event_scenario.auth.user,
        event_details,
    )
    assert created_registration_1 is not None
    created_registration_2 = event_svc_integration.register(
        event_scenario.auth.user,
        event_scenario.auth.user,
        event_details,
    )
    assert created_registration_2 is not None
    assert created_registration_1 == created_registration_2


def test_register_for_event_enforces_permission(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.root
    )
    event_svc_integration.register(
        event_scenario.auth.root,
        event_scenario.auth.user,
        event_details,
    )
    event_svc_integration._permission.enforce.assert_any_call(
        event_scenario.auth.root,
        "organization.events.manage_registrations",
        f"organization/{event_scenario.organizations.cssg.id}",
    )


def test_get_registration(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.ambassador
    )
    event_registration = event_svc_integration.get_registration(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        event_details,
    )
    assert event_registration is not None


def test_get_registration_that_does_not_exist(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.root
    )
    event_registration = event_svc_integration.get_registration(
        event_scenario.auth.root,
        event_scenario.auth.root,
        event_details,
    )
    assert event_registration is None


def test_get_registrations_of_event_as_organizer(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.user
    )
    event_registrations = event_svc_integration.get_registrations_of_event(
        event_scenario.auth.user, event_details
    )
    assert len(event_registrations) == 2


def test_get_registrations_of_event_non_organizer(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.ambassador
    )
    with pytest.raises(UserPermissionException):
        event_svc_integration.get_registrations_of_event(
            event_scenario.auth.ambassador, event_details
        )


def test_get_registrations_enforces_admin_auth(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that root is able to delete any registrations."""
    # Setup mock to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Ensure delete occurs
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.ambassador
    )
    event_svc_integration.get_registrations_of_event(
        event_scenario.auth.ambassador, event_details
    )

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        event_scenario.auth.ambassador,
        "organization.events.manage_registrations",
        f"organization/{event_scenario.organizations.cssg.id}",
    )


def test_unregister_for_event_as_registerer(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that a user is able to unregister for an event."""
    event_details = event_svc_integration.get_by_id(event_scenario.event_one.id)
    assert (
        event_svc_integration.get_registration(
            event_scenario.auth.ambassador,
            event_scenario.auth.ambassador,
            event_details,
        )
        is not None
    )
    event_svc_integration.unregister(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        event_details,
    )
    assert (
        event_svc_integration.get_registration(
            event_scenario.auth.ambassador,
            event_scenario.auth.ambassador,
            event_details,
        )
        is None
    )


def test_unregister_for_event_as_registerer_is_idempotent(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that a user is able to unregister for an event."""
    event_details = event_svc_integration.get_by_id(event_scenario.event_one.id)
    event_svc_integration.unregister(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        event_details,
    )
    event_svc_integration.unregister(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        event_details,
    )
    assert (
        event_svc_integration.get_registration(
            event_scenario.auth.ambassador,
            event_scenario.auth.ambassador,
            event_details,
        )
        is None
    )


def test_unregister_for_event_as_wrong_user(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that any user is *unable* to delete a registration that is not for them."""
    event_details = event_svc_integration.get_by_id(event_scenario.event_one.id)
    with pytest.raises(UserPermissionException):
        event_svc_integration.unregister(
            event_scenario.auth.user,
            event_scenario.auth.ambassador,
            event_details,
        )


def test_unregister_for_event_enforces_admin_auth(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that root is able to delete any registrations."""
    # Setup mock to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Ensure delete occurs
    event_details = event_svc_integration.get_by_id(
        event_scenario.event_one.id, event_scenario.auth.root
    )
    event_svc_integration.unregister(
        event_scenario.auth.root,
        event_scenario.auth.ambassador,
        event_details,
    )

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        event_scenario.auth.root,
        "organization.events.manage_registrations",
        f"organization/{event_scenario.organizations.cssg.id}",
    )


def test_get_registrations_of_user(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
    time: dict[str, datetime],
):
    """Test that a user with a registration is able to query for it."""
    time_range = TimeRange(
        start=event_scenario.event_one.start - ONE_DAY,
        end=event_scenario.event_one.start + ONE_DAY,
    )
    registrations = event_svc_integration.get_registrations_of_user(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        time_range,
    )
    assert len(registrations) == 1


def test_get_registrations_of_user_outside_time_range(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
    time: dict[str, datetime],
):
    """Test that a user with a registration is able to query for it."""
    # Test range after event
    time_range = TimeRange(
        start=event_scenario.event_one.start + 2 * ONE_DAY,
        end=event_scenario.event_one.start + 3 * ONE_DAY,
    )
    registrations = event_svc_integration.get_registrations_of_user(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        time_range,
    )
    assert len(registrations) == 0

    # Test range before event
    time_range = TimeRange(
        start=event_scenario.event_one.start - ONE_DAY * 2,
        end=event_scenario.event_one.start - ONE_DAY,
    )
    registrations = event_svc_integration.get_registrations_of_user(
        event_scenario.auth.ambassador,
        event_scenario.auth.ambassador,
        time_range,
    )
    assert len(registrations) == 0


def test_get_registrations_of_user_without_reservations(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
    time: dict[str, datetime],
):
    """Test that a user without any registrations is able to query for it."""
    time_range = TimeRange(
        start=event_scenario.event_one.start - ONE_DAY,
        end=event_scenario.event_one.start + ONE_DAY,
    )
    registrations = event_svc_integration.get_registrations_of_user(
        event_scenario.auth.root,
        event_scenario.auth.root,
        time_range,
    )
    assert len(registrations) == 0


def test_get_registrations_of_user_admin_authorization(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Test that administrative permissions are enforced."""
    # Setup mock to test permission enforcement on the PermissionService.
    event_svc_integration._permission = create_autospec(
        event_svc_integration._permission
    )

    # Ensure delete occurs
    time_range = TimeRange(
        start=event_scenario.event_one.start - ONE_DAY,
        end=event_scenario.event_one.start + ONE_DAY,
    )
    event_svc_integration.get_registrations_of_user(
        event_scenario.auth.root,
        event_scenario.auth.ambassador,
        time_range,
    )

    # Ensure that the correct permission check is run
    event_svc_integration._permission.enforce.assert_called_with(
        event_scenario.auth.root,
        "user.event_registrations",
        f"user/{event_scenario.auth.ambassador.id}",
    )


def test_register_to_full_event(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Tests that a user cannot register for an event that is full."""
    event_details = event_svc_integration.get_by_id(event_scenario.event_three.id)

    with pytest.raises(EventRegistrationException):
        event_svc_integration.register(
            event_scenario.auth.user,
            event_scenario.auth.user,
            event_details,
        )


def test_get_registered_users_of_event(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Tests querying for registered users of events as a paginated list"""
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter=""
    )
    page = event_svc_integration.get_registered_users_of_event(
        event_scenario.auth.root,
        event_scenario.event_one.id,
        pagination_params,
    )

    assert len(page.items) == 1
    assert page.length == 1
    assert page.items[0].id == event_scenario.auth.ambassador.id


def test_organizer_get_registered_users_of_event(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    """Tests that organizers for an event can retrieve registered users"""
    # Setup to test permission enforcement on the PermissionService.
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter=""
    )
    page = event_svc_integration.get_registered_users_of_event(
        event_scenario.auth.user,
        event_scenario.event_one.id,
        pagination_params,
    )

    assert len(page.items) == 1
    assert page.length == 1
    assert page.items[0].id == event_scenario.auth.ambassador.id


def test_organizer_get_registered_users_of_event_filtered(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
):
    """Tests that organizers for an event can retrieve registered users"""
    # Setup to test permission enforcement on the PermissionService.
    pagination_params = PaginationParams(
        page=0, page_size=10, order_by="first_name", filter="Amy"
    )
    page = event_svc_integration.get_registered_users_of_event(
        event_scenario.auth.user,
        event_scenario.event_one.id,
        pagination_params,
    )

    assert len(page.items) == 1
    assert page.length == 1
    assert page.items[0].id == event_scenario.auth.ambassador.id


def test_get_registered_users_of_event_permissions(
    event_svc_integration: EventService, event_scenario: EventScenario
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
        event_scenario.auth.root,
        event_scenario.event_one.id,
        pagination_params,
    )
    event_svc_integration._permission.enforce.assert_called_with(
        event_scenario.auth.root,
        "organization.events.manage_registrations",
        f"organization/{event_scenario.organizations.cssg.id}",
    )


def test_get_registered_users_of_event_without_permissions(
    event_svc_integration: EventService,
    event_scenario: EventScenario,
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
        event_scenario.auth.user,
        event_scenario.event_two.id,
        pagination_params,
    )
    event_svc_integration._permission.enforce.assert_called_with(
        event_scenario.auth.user,
        "organization.events.manage_registrations",
        f"organization/{event_scenario.organizations.cssg.id}",
    )


def test_get_event_status(
    event_svc_integration: EventService, event_scenario: EventScenario
):
    status = event_svc_integration.get_event_status(event_scenario.auth.user)
    assert status is not None
    assert status.featured is not None
    assert len(status.registered) == 1
