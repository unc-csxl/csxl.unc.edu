"""Tests for the PermissionService class."""

import pytest
from sqlalchemy.orm import Session

# Tested Dependencies
from ...models import Permission, User
from ...services import PermissionService

from .auth_scenario import arrange_auth_scenario
from .fixtures import permission_svc

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_no_permission(session: Session, permission_svc: PermissionService):
    """Tests that user initially has no permissions"""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act / Assert
    assert permission_svc.check(scenario.user, "permission.grant", "permission") is False
    assert permission_svc.check(scenario.user, "user.delete", "user/1") is False


def test_grant_role_permission(session: Session, permission_svc: PermissionService):
    """Tests that you can grant a permission to a role"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    assert permission_svc.check(scenario.ambassador, "checkin.delete", "checkin") is False
    p = Permission(action="checkin.delete", resource="*")

    # Act
    permission_svc.grant(scenario.root, scenario.ambassador, p)

    # Assert
    assert permission_svc.check(scenario.ambassador, "checkin.delete", "checkin")


def test_grant_user_permission(session: Session, permission_svc: PermissionService):
    """Tests that you can grant a permission to a user"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    assert permission_svc.check(scenario.ambassador, "checkin.delete", "checkin") is False
    p = Permission(action="checkin.delete", resource="*")

    # Act
    permission_svc.grant(scenario.root, scenario.ambassador_role, p)

    # Assert
    assert permission_svc.check(scenario.ambassador, "checkin.delete", "checkin")


def test_grant_none_exception(session: Session, permission_svc: PermissionService):
    """Tests that a ValueError is raised if attempting to grant to an improper object"""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act / Assert
    with pytest.raises(ValueError):
        p = Permission(action="checkin.delete", resource="*")
        permission_svc.grant(scenario.root, None, p)  # type: ignore


def test_revoke_role_permission(session: Session, permission_svc: PermissionService):
    """Tests that you can remove a permission from a user"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    assert permission_svc.check(scenario.ambassador, "checkin.create", "checkin")

    # Act
    permission_svc.revoke(scenario.root, scenario.ambassador_permission)

    # Assert
    assert (
        permission_svc.check(scenario.ambassador, "checkin.create", "checkin")
        is False
    )


def test_revoke_permission_without_id(
    session: Session, permission_svc: PermissionService
):
    """Tests that you can remove a permission from a user"""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act / Assert
    assert (
        permission_svc.revoke(
            scenario.root,
            Permission(id=None, action="checkin.create", resource="checkin"),
        )
        is False
    )


def test_revoke_nonexistent_permission(
    session: Session, permission_svc: PermissionService
):
    """Tests that you can remove a permission from a user"""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act / Assert
    assert (
        permission_svc.revoke(
            scenario.root,
            Permission(id=423, action="checkin.create", resource="checkin"),
        )
        is False
    )


def test_root_resource_access(session: Session, permission_svc: PermissionService):
    """Tests the permissions for the root user"""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act / Assert
    assert permission_svc.check(
        scenario.root, "access_control.grant", "access_control"
    )
    assert permission_svc.check(scenario.root, "user.delete", "user/1")


def test_check_catch_all_permission(permission_svc: PermissionService):
    """Tests that you can create a user with all permissions"""
    p = Permission(action="*", resource="*")
    assert permission_svc._check_permission(p, "permission.grant", "*")
    assert permission_svc._check_permission(p, "permission.grant", "checkin")
    assert permission_svc._check_permission(p, "permission.revoke", "checkin.*")
    assert permission_svc._check_permission(p, "checkin.delete", "checkin/1")


def test_check_catch_all_resource_permission(permission_svc: PermissionService):
    """Tests that that all resource permissions can be given to a user using *"""
    p = Permission(action="permission.grant", resource="*")
    assert permission_svc._check_permission(p, "permission.grant", "*")
    assert permission_svc._check_permission(p, "permission.grant", "checkin")
    assert (
        permission_svc._check_permission(p, "permission.revoke", "checkin.*") is False
    )
    assert permission_svc._check_permission(p, "checkin.delete", "checkin/1") is False


def test_check_specific_resource_permission(permission_svc: PermissionService):
    """Tests giving a specific resource permission to a user"""
    p = Permission(action="permission.grant", resource="checkin*")
    assert permission_svc._check_permission(p, "permission.grant", "*") is False
    assert permission_svc._check_permission(p, "permission.grant", "checkin")
    assert (
        permission_svc._check_permission(p, "permission.revoke", "checkin.*") is False
    )
    assert permission_svc._check_permission(p, "checkin.delete", "checkin/1") is False


def test_check_specific_permission(permission_svc: PermissionService):
    """Tests that you can create a user with a specific permission"""
    p = Permission(action="checkin.delete", resource="checkin/*")
    assert permission_svc._check_permission(p, "checkin.delete", "checkin/1")
    assert permission_svc._check_permission(p, "checkin.delete", "checkin/12")
    assert permission_svc._check_permission(p, "checkin.create", "checkin/12") is False
    assert (
        permission_svc._check_permission(p, "permission.revoke", "checkin.*") is False
    )


def test_get_user_roles_permissions(permission_svc: PermissionService):
    """Test covers an edge case of _get_user_roles_permissions when user does not exist"""
    assert permission_svc._get_user_roles_permissions(User(id=423)) == []
