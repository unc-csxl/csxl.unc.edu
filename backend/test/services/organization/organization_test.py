"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ....models import Organization
from ....services import OrganizationService

# Injected Service Fixtures
from ..fixtures import organization_svc_integration

from ..auth_scenario import arrange_auth_scenario
from .scenario import arrange_organization_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `OrganizationService.all()`


def test_get_all(session: Session, organization_svc_integration: OrganizationService):
    """Test that all organizations can be retrieved."""
    # Arrange
    scenario = arrange_organization_scenario(session)

    # Act
    fetched_organizations = organization_svc_integration.all()

    # Assert
    assert fetched_organizations is not None
    assert len(fetched_organizations) == len(scenario.organizations)
    assert isinstance(fetched_organizations[0], Organization)


# Test `OrganizationService.get_by_id()`


def test_get_by_slug(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that organizations can be retrieved based on their ID."""
    # Arrange
    scenario = arrange_organization_scenario(session)

    # Act
    fetched_organization = organization_svc_integration.get_by_slug(scenario.cads.slug)

    # Assert
    assert fetched_organization is not None
    assert isinstance(fetched_organization, Organization)
    assert fetched_organization.slug == scenario.cads.slug


# Test `OrganizationService.create()`


def test_create_enforces_permission(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that the service enforces permissions when attempting to create an organization."""
    # Arrange
    auth = arrange_auth_scenario(session)

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    organization_scenario = arrange_organization_scenario(session)

    # Act
    organization_svc_integration.create(auth.root, organization_scenario.to_add)

    # Assert
    organization_svc_integration._permission.enforce.assert_called_with(
        auth.root, "organization.create", "organization"
    )


def test_create_organization_as_root(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that the root user is able to create new organizations."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act
    created_organization = organization_svc_integration.create(
        auth.root, scenario.to_add
    )

    # Assert
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_id_already_exists(
    session: Session,
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to create new organizations when an extraneous ID is provided."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act
    created_organization = organization_svc_integration.create(
        auth.root, scenario.to_add_conflicting_id
    )

    # Assert
    assert created_organization is not None
    assert created_organization.id is not None


def test_create_organization_as_user(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that any user is *unable* to create new organizations."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        organization_svc_integration.create(auth.user, scenario.to_add)
        pytest.fail()  # Fail test if no error was thrown above


# Test `OrganizationService.update()`
def test_update_organization_as_root(
    session: Session,
    organization_svc_integration: OrganizationService,
):
    """Test that the root user is able to update organizations.
    Note: Test data's website field is updated
    """
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act
    organization_svc_integration.update(auth.root, scenario.new_cads)

    # Assert
    assert (
        organization_svc_integration.get_by_slug("cads").website
        == "https://cads.cs.unc.edu/"
    )


def test_update_organization_as_user(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that any user is *unable* to update new organizations."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        organization_svc_integration.update(auth.user, scenario.new_cads)


def test_update_organization_does_not_exist(
    session: Session,
    organization_svc_integration: OrganizationService,
):
    """Test updating an organization that does not exist."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.update(auth.root, scenario.to_add)


def test_delete_enforces_permission(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that the service enforces permissions when attempting to delete an organization."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Setup to test permission enforcement on the PermissionService.
    organization_svc_integration._permission = create_autospec(
        organization_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    # Act
    organization_svc_integration.delete(auth.root, scenario.cads.slug)

    # Assert
    organization_svc_integration._permission.enforce.assert_called_with(
        auth.root, "organization.delete", "organization"
    )


def test_delete_organization_as_root(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that the root user is able to delete organizations."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act
    organization_svc_integration.delete(auth.root, scenario.cads.slug)

    # Assert
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.get_by_slug(scenario.cads.slug)


def test_delete_organization_as_user(
    session: Session, organization_svc_integration: OrganizationService
):
    """Test that any user is *unable* to delete organizations."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        organization_svc_integration.delete(auth.user, scenario.cads.slug)


def test_delete_organization_does_not_exist(
    session: Session,
    organization_svc_integration: OrganizationService,
):
    """Test deleting an organization that does not exist."""
    # Arrange
    auth = arrange_auth_scenario(session)
    scenario = arrange_organization_scenario(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        organization_svc_integration.delete(auth.root, scenario.to_add.slug)
