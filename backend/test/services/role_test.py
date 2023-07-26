"""Tests for the RoleService class."""

import pytest

from sqlalchemy.orm import Session
from unittest.mock import create_autospec
from ...models import Permission
from ...services import RoleService, PermissionService

from .core_data import setup_insert_data_fixture
from .fixtures import role_svc, permission_svc_mock

from .role_data import root_role, ambassador_role
from .user_data import root, ambassador, user
from .permission_data import ambassador_permission


def test_list(role_svc: RoleService):
    roles = role_svc.list(root)
    assert len(roles) == 2
    assert ambassador_role in roles
    assert root_role in roles


def test_list_enforces_permission(
    role_svc: RoleService, permission_svc_mock: PermissionService
):
    roles = role_svc.list(root)
    permission_svc_mock.enforce.assert_called_once_with(root, "role.list", "role/")


def test_details(role_svc: RoleService):
    details = role_svc.details(root, ambassador_role.id)
    assert details.id == ambassador_role.id
    assert details.name == ambassador_role.name
    assert ambassador_permission in details.permissions


def test_details_enforces_permission(
    role_svc: RoleService, permission_svc_mock: PermissionService
):
    role_svc.details(root, ambassador_role.id)
    permission_svc_mock.enforce.assert_called_once_with(
        root, "role.details", f"role/{ambassador_role.id}"
    )


def test_grant_permission(
    role_svc: RoleService, permission_svc_mock: PermissionService
):
    perm = Permission(action="checkin.read", resource="checkin")
    role_svc.grant_permission(root, ambassador_role.id, perm)
    permission_svc_mock.grant.assert_called_once()


def test_grant_permission_enforces_permission(
    role_svc: RoleService, permission_svc_mock: PermissionService
):
    perm = Permission(action="checkin.read", resource="checkin")
    role_svc.grant_permission(root, ambassador_role.id, perm)
    permission_svc_mock.enforce.assert_any_call(
        root, "role.grant_permission", f"role/{ambassador_role.id}"
    )


def test_revoke_permission(
    role_svc: RoleService, permission_svc_mock: PermissionService
):
    role_svc.revoke_permission(root, ambassador_role.id, ambassador_permission.id)
    permission_svc_mock.revoke.assert_called_once()


def test_revoke_permission_enforces_permission(
    role_svc: RoleService, permission_svc_mock: PermissionService
):
    role_svc.revoke_permission(root, ambassador_role.id, ambassador_permission.id)
    permission_svc_mock.enforce.assert_any_call(
        root, "role.revoke_permission", f"role/{ambassador_role.id}"
    )


def test_is_member(role_svc: RoleService):
    assert role_svc.is_member(root, ambassador_role.id, ambassador.id)
    assert not role_svc.is_member(root, ambassador_role.id, user.id)


def test_add_member(role_svc: RoleService):
    assert not role_svc.is_member(root, ambassador_role.id, user.id)
    role_svc.add_member(root, ambassador_role.id, user)
    assert role_svc.is_member(root, ambassador_role.id, user.id)


def test_remove_member(role_svc: RoleService):
    assert role_svc.is_member(root, ambassador_role.id, ambassador.id)
    role_svc.remove_member(root, ambassador_role.id, ambassador.id)
    assert not role_svc.is_member(root, ambassador_role.id, ambassador.id)
