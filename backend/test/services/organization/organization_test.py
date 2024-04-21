"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ....models import Organization
from ....services import OrganizationService

# Injected Service Fixtures
from ..fixtures import organization_svc_integration

# Import core data to ensure all data loads for the tests.
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .organization_test_data import (
    organizations,
    to_add,
    cads,
    new_cads,
    to_add_conflicting_id,
)
from ..user_data import root, user

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `OrganizationService.all()`


def test_get_all(organization_svc_integration: OrganizationService):
    """Test that all organizations can be retrieved."""
    fetched_organizations = organization_svc_integration.all()
    assert fetched_organizations is not None
    assert len(fetched_organizations) == len(organizations)
    assert isinstance(fetched_organizations[0], Organization)


# Test `OrganizationService.get_by_id()`


def test_get_by_slug(organization_svc_integration: OrganizationService):
    """Test that organizations can be retrieved based on their ID."""
    fetched_organization = organization_svc_integration.get_by_slug(cads.slug)
    assert fetched_organization is not None
    assert isinstance(fetched_organization, Organization)
    assert fetched_organization.slug == cads.slug


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
        root, "organization.create", "organization"
    )


def test_create_organization_as_root(organization_svc_integration: OrganizationService):
    """Test that the root user is able to create new organizations."""
    created_organization = organization_svc_integration.create(root, to_add)
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_id_already_exists(
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to create new organizations when an extraneous ID is provided."""
    created_organization = organization_svc_integration.create(
        root, to_add_conflicting_id
    )
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to create new organizations."""
    with pytest.raises(UserPermissionException):
        organization_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


# Test `OrganizationService.update()`
def test_update_organization_as_root(
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to update organizations.
    Note: Test data's website field is updated
    """
    organization_svc_integration.update(root, new_cads)
    assert (
        organization_svc_integration.get_by_slug("cads").website
        == "https://cads.cs.unc.edu/"
    )


def test_update_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to update new organizations."""
    with pytest.raises(UserPermissionException):
        organization_svc_integration.update(user, new_cads)


def test_update_organization_does_not_exist(
    organization_svc_integration: OrganizationService,
):
    """Test updating an organization that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.update(root, to_add)


def test_delete_enforces_permission(organization_svc_integration: OrganizationService):
    """Test that the service enforces permissions when attempting to delete an organization."""

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    organization_svc_integration.delete(root, cads.slug)
    organization_svc_integration._permission.enforce.assert_called_with(
        root, "organization.delete", "organization"
    )


def test_delete_organization_as_root(organization_svc_integration: OrganizationService):
    """Test that the root user is able to delete organizations."""
    organization_svc_integration.delete(root, cads.slug)
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.get_by_slug(cads.slug)


def test_delete_organization_as_user(organization_svc_integration: OrganizationService):
    """Test that any user is *unable* to delete organizations."""
    with pytest.raises(UserPermissionException):
        organization_svc_integration.delete(user, cads.slug)


def test_delete_organization_does_not_exist(
    organization_svc_integration: OrganizationService,
):
    """Test deleting an organization that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.delete(root, to_add.slug)
