"""Tests for the PermissionService class."""

import pytest

from sqlalchemy.orm import Session
from ...models import Permission
from ...services import PermissionService

from .core_data import setup_insert_data_fixture

from .role_data import ambassador_role
from .user_data import root, ambassador, user
from .permission_data import ambassador_permission


@pytest.fixture()
def permission(test_session: Session):
    return PermissionService(test_session)


def test_no_permission(permission: PermissionService):
    """Tests that user initially has no permissions"""
    assert permission.check(user, "permission.grant", "permission") is False
    assert permission.check(user, "user.delete", "user/1") is False


def test_grant_role_permission(permission: PermissionService):
    """Tests that you can grant a permission to a user"""
    assert permission.check(ambassador, "checkin.delete", "checkin") is False
    p = Permission(action="checkin.delete", resource="*")
    permission.grant(root, ambassador_role, p)
    assert permission.check(ambassador, "checkin.delete", "checkin")


def test_revoke_role_permission(permission: PermissionService):
    """Tests that you can remove a permission from a user"""
    assert permission.check(ambassador, "checkin.create", "checkin")
    permission.revoke(root, ambassador_permission)
    assert permission.check(ambassador, "checkin.create", "checkin") is False


def test_root_resource_access(permission: PermissionService):
    """Tests the permissions for the root user"""
    assert permission.check(root, "access_control.grant", "access_control")
    assert permission.check(root, "user.delete", "user/1")


def test_check_catch_all_permission(permission: PermissionService):
    """Tests that you can create a user with all permissions"""
    p = Permission(action="*", resource="*")
    assert permission._check_permission(p, "permission.grant", "*")
    assert permission._check_permission(p, "permission.grant", "checkin")
    assert permission._check_permission(p, "permission.revoke", "checkin.*")
    assert permission._check_permission(p, "checkin.delete", "checkin/1")


def test_check_catch_all_resource_permission(permission: PermissionService):
    """Tests that that all resource permissions can be given to a user using *"""
    p = Permission(action="permission.grant", resource="*")
    assert permission._check_permission(p, "permission.grant", "*")
    assert permission._check_permission(p, "permission.grant", "checkin")
    assert permission._check_permission(p, "permission.revoke", "checkin.*") is False
    assert permission._check_permission(p, "checkin.delete", "checkin/1") is False


def test_check_specific_resource_permission(permission: PermissionService):
    """Tests giving a specific resource permission to a user"""
    p = Permission(action="permission.grant", resource="checkin*")
    assert permission._check_permission(p, "permission.grant", "*") is False
    assert permission._check_permission(p, "permission.grant", "checkin")
    assert permission._check_permission(p, "permission.revoke", "checkin.*") is False
    assert permission._check_permission(p, "checkin.delete", "checkin/1") is False


def test_check_specific_permission(permission: PermissionService):
    """Tests that you can create a user with a specific permission"""
    p = Permission(action="checkin.delete", resource="checkin/*")
    assert permission._check_permission(p, "checkin.delete", "checkin/1")
    assert permission._check_permission(p, "checkin.delete", "checkin/12")
    assert permission._check_permission(p, "checkin.create", "checkin/12") is False
    assert permission._check_permission(p, "permission.revoke", "checkin.*") is False
