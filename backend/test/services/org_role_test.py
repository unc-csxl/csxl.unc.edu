"""Tests for the OrgRoleService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

# Tested Dependencies
from ...models import OrgRoleDetail
from ...services import OrgRoleService

# Injected Service Fixtures
from .fixtures import org_role_svc_integration

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .org_role_data import org_roles, to_add, to_star, cads_leader_role

# from .event_data import events, cads_event, time_range, to_add, new_cads

from .organization_data import cads

from .user_data import root, user, cads_leader, ambassador

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `OrgRoleService.all()`


def test_get_all(org_role_svc_integration: OrgRoleService):
    """Test that all org roles can be retrieved."""
    fetched_org_roles = org_role_svc_integration.all()
    assert fetched_org_roles is not None
    assert len(fetched_org_roles) == len(org_roles)
    assert isinstance(fetched_org_roles[0], OrgRoleDetail)


# Test `OrgRoleService.get_from_userid()`


def test_get_from_userid(org_role_svc_integration: OrgRoleService):
    """Test that org roles can be retrieved based on a given user ID."""
    fetched_org_roles = org_role_svc_integration.get_from_userid(cads_leader.id)
    assert fetched_org_roles is not None
    assert len(fetched_org_roles) == 1
    assert isinstance(fetched_org_roles[0], OrgRoleDetail)
    assert fetched_org_roles[0].user_id == cads_leader.id


# Test `OrgRoleService.get_from_orgid()`


def test_get_from_orgid(org_role_svc_integration: OrgRoleService):
    """Test that org roles can be retrieved based on a given org ID."""
    fetched_org_roles = org_role_svc_integration.get_from_orgid(cads.id)
    assert fetched_org_roles is not None
    assert len(fetched_org_roles) == 1
    assert isinstance(fetched_org_roles[0], OrgRoleDetail)
    assert fetched_org_roles[0].org_id == cads.id


# Test `OrgRoleService.create()`


def test_create_enforces_permission(org_role_svc_integration: OrgRoleService):
    """Test that the service enforces permissions when attempting to create an org role."""

    # Setup to test permission enforcement on the PermissionService.
    org_role_svc_integration._permission = create_autospec(
        org_role_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    org_role_svc_integration.create(root, to_add)
    org_role_svc_integration._permission.enforce.assert_called_with(
        root, "admin.create_orgrole", "orgroles"
    )


def test_create_org_role_as_root_for_other_user(
    org_role_svc_integration: OrgRoleService,
):
    """Test that the root user is able to create new org roles for any user."""
    created_org_role = org_role_svc_integration.create(root, to_add)
    assert created_org_role is not None
    assert created_org_role.id is not None


def test_create_organization_as_user_for_other_user(
    org_role_svc_integration: OrgRoleService,
):
    """Test that any user is *unable* to create new org roles for users other than themself."""
    try:
        org_role_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected


def test_create_org_role_as_user_for_self_star(
    org_role_svc_integration: OrgRoleService,
):
    """Test that the root user is able to create new org roles for themself with val of 0 (starring an org)."""
    created_org_role = org_role_svc_integration.create(user, to_star)
    assert created_org_role is not None
    assert created_org_role.id is not None


def test_create_org_role_as_user_for_self_higher_than_star(
    org_role_svc_integration: OrgRoleService,
):
    """Test that the root user is *unable* to create new org roles for themself with val of 1+ (higher than star)."""
    try:
        org_role_svc_integration.create(ambassador, to_add)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected


# Test `OrgRoleService.delete()`


def test_delete_enforces_permission(org_role_svc_integration: OrgRoleService):
    """Test that the service enforces permissions when attempting to delete an org role."""

    # Setup to test permission enforcement on the PermissionService.
    org_role_svc_integration._permission = create_autospec(
        org_role_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    org_role_svc_integration.delete(root, cads_leader_role.id)
    org_role_svc_integration._permission.enforce.assert_called_with(
        root, "admin.delete_orgrole", f"orgroles/{cads_leader_role.id}"
    )


def test_delete_org_role_as_root(org_role_svc_integration: OrgRoleService):
    """Test that the root user is able to delete org roles."""
    org_role_svc_integration.delete(root, cads_leader_role.id)

    try:
        org_role_svc_integration.get_from_id(cads.id)
        org_role_svc_integration.get_from_name(cads.name)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because an error was thrown when we found no org role


def test_delete_org_role_as_user(org_role_svc_integration: OrgRoleService):
    """Test that any user is *unable* to delete org roles."""
    try:
        org_role_svc_integration.delete(user, cads_leader_role.id)
        pytest.fail()  # Fail test if no error was thrown above
    except:
        ...  # Test passes, because a `UserPermissionError` was thrown as expected
