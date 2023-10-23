"""Tests for the PermissionService class."""

import pytest

# Tested Dependencies
from ...models import Permission, User
from ...services import PermissionService

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import permission_svc

# Data Models for Fake Data Inserted in Setup
from .role_data import ambassador_role
from .user_data import root, ambassador, user
from .permission_data import ambassador_permission

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_no_permission(permission_svc: PermissionService):
    """Tests that user initially has no permissions"""
    assert permission_svc.check(user, "permission.grant", "permission") is False
    assert permission_svc.check(user, "user.delete", "user/1") is False


def test_grant_role_permission(permission_svc: PermissionService):
    """Tests that you can grant a permission to a role"""
    assert permission_svc.check(ambassador, "checkin.delete", "checkin") is False
    p = Permission(action="checkin.delete", resource="*")
    permission_svc.grant(root, ambassador, p)
    assert permission_svc.check(ambassador, "checkin.delete", "checkin")


def test_grant_user_permission(permission_svc: PermissionService):
    """Tests that you can grant a permission to a user"""
    assert permission_svc.check(ambassador, "checkin.delete", "checkin") is False
    p = Permission(action="checkin.delete", resource="*")
    permission_svc.grant(root, ambassador_role, p)
    assert permission_svc.check(ambassador, "checkin.delete", "checkin")


def test_grant_none_exception(permission_svc: PermissionService):
    """Tests that a ValueError is raised if attempting to grant to an improper object"""
    with pytest.raises(ValueError):
        p = Permission(action="checkin.delete", resource="*")
        permission_svc.grant(root, None, p)  # type: ignore


def test_revoke_role_permission(permission_svc: PermissionService):
    """Tests that you can remove a permission from a user"""
    assert permission_svc.check(ambassador, "checkin.create", "checkin")
    permission_svc.revoke(root, ambassador_permission)
    assert permission_svc.check(ambassador, "checkin.create", "checkin") is False


def test_revoke_permission_without_id(permission_svc: PermissionService):
    """Tests that you can remove a permission from a user"""
    assert (
        permission_svc.revoke(
            root, Permission(id=None, action="checkin.create", resource="checkin")
        )
        is False
    )


def test_revoke_nonexistent_permission(permission_svc: PermissionService):
    """Tests that you can remove a permission from a user"""
    assert (
        permission_svc.revoke(
            root, Permission(id=423, action="checkin.create", resource="checkin")
        )
        is False
    )


def test_root_resource_access(permission_svc: PermissionService):
    """Tests the permissions for the root user"""
    assert permission_svc.check(root, "access_control.grant", "access_control")
    assert permission_svc.check(root, "user.delete", "user/1")


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
