"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

# Tested Dependencies
from ...models import OrganizationDetail
from ...services import OrganizationService

# Injected Service Fixtures
from .fixtures import organization_svc_integration

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture
from .organization_data import fake_data_fixture

# Data Models for Fake Data Inserted in Setup
from .organization_data import (
    organizations,
    to_add,
    organization_names,
    cads_leader,
    cads,
    new_cads,
)
from .user_data import root, user

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `OrganizationService.get()`


def test_get_all(organization_svc_integration: OrganizationService):
    """Test that all organizations can be retrieved."""
    fetched_organizations = organization_svc_integration.all()
    assert fetched_organizations is not None
    assert len(fetched_organizations) == len(organizations)
    assert isinstance(fetched_organizations[0], OrganizationDetail)


# Test `OrganizationService.get_from_id()`


def test_get_from_id(organization_svc_integration: OrganizationService):
    """Test that organizations can be retrieved based on their name."""
    fetched_organization = organization_svc_integration.get_from_id(cads.id)
    assert fetched_organization is not None
    assert isinstance(fetched_organization, OrganizationDetail)
    assert fetched_organization.id == cads.id


# Test `OrganizationService.get_from_name()`


def test_get_from_name(organization_svc_integration: OrganizationService):
    """Test that organizations can be retrieved based on their name."""
    for name in organization_names:
        fetched_organization = organization_svc_integration.get_from_name(name)
        assert fetched_organization is not None
        assert isinstance(fetched_organization, OrganizationDetail)
        assert fetched_organization.name == name


# Test `OrganizationService.create()`


def test_create_enforces_permission(organization_svc_integration: OrganizationService):
    """Test that the service enforces permissions when attempting to create an organization."""

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    organization_svc_integration.create(root, to_add)
    organization_svc_integration._permission.enforce.assert_called_with(
        root, "organization.create", "organizations"
    )


def test_create_organization_as_root(organization_svc_integration: OrganizationService):
    """Test that the root user is able to create new organizations."""
    created_organization = organization_svc_integration.create(root, to_add)
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to create new organizations."""
    try:
        organization_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `PermissionError` was thrown as expected


# Test `OrganizationService.update()`


def test_update_organization_as_leader(
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to create new organizations.
    Note: Test data's website field is updated
    """
    updated_organization = organization_svc_integration.update(cads_leader, new_cads)
    assert updated_organization is not None
    assert updated_organization.id is not None
    assert updated_organization.website == new_cads.website


def test_update_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to create new organizations."""
    try:
        organization_svc_integration.update(user, new_cads)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `PermissionError` was thrown as expected


# Test `OrganizationService.delete()`


def test_delete_enforces_permission(organization_svc_integration: OrganizationService):
    """Test that the service enforces permissions when attempting to delete an organization."""

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    organization_svc_integration.delete(root, cads.id)
    organization_svc_integration._permission.enforce.assert_called_with(
        root, "organization.create", "organizations"
    )


def test_delete_organization_as_root(organization_svc_integration: OrganizationService):
    """Test that the root user is able to create new organizations."""
    organization_svc_integration.delete(root, cads.id)

    try:
        organization_svc_integration.get_from_id(cads.id)
        organization_svc_integration.get_from_name(cads.name)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because an error was thrown when we found no organization


def test_delete_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to create new organizations."""
    try:
        organization_svc_integration.delete(user, cads.id)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `PermissionError` was thrown as expected
