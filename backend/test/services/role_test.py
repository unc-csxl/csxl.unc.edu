"""Tests for the RoleService class."""

import pytest

from sqlalchemy.orm import Session
from unittest.mock import create_autospec
from ...models import User, Role, Permission
from ...entities import UserEntity, RoleEntity, PermissionEntity
from ...services import RoleService, PermissionService

# Mock Models
root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu')
root_role = Role(id=1, name='root')

ambassador = User(id=2, pid=888888888, onyen='ambassador',
                  email='ambassador@unc.edu')
ambassador_role = Role(id=2, name='ambassadors')
ambassador_permission: Permission

user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu')


@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    # Bootstrap root User and Role
    root_user_entity = UserEntity.from_model(root)
    test_session.add(root_user_entity)
    root_role_entity = RoleEntity.from_model(root_role)
    root_role_entity.users.append(root_user_entity)
    test_session.add(root_role_entity)
    root_permission_entity = PermissionEntity(
        action='*', resource='*', role=root_role_entity)
    test_session.add(root_permission_entity)

    # Bootstrap ambassador and role
    ambassador_entity = UserEntity.from_model(ambassador)
    test_session.add(ambassador_entity)
    ambassador_role_entity = RoleEntity.from_model(ambassador_role)
    ambassador_role_entity.users.append(ambassador_entity)
    test_session.add(ambassador_role_entity)
    ambassador_permission_entity = PermissionEntity(
        action='checkin.create', resource='checkin', role=ambassador_role_entity)
    test_session.add(ambassador_permission_entity)

    # Bootstrap user without any special perms
    user_entity = UserEntity.from_model(user)
    test_session.add(user_entity)

    test_session.commit()

    global ambassador_permission
    ambassador_permission = ambassador_permission_entity.to_model()
    yield

# Fixtures for dependency injection of the tests for dependent services

@pytest.fixture()
def permission_svc_mock():
    """This mocks the PermissionService class to avoid testing its implementation here."""
    return create_autospec(PermissionService)


@pytest.fixture()
def role_svc(test_session: Session, permission_svc_mock: PermissionService):
    return RoleService(test_session, permission_svc_mock)

# Tests of RoleService

def test_list(role_svc: RoleService):
    roles = role_svc.list(root)
    assert len(roles) == 2
    assert ambassador_role in roles
    assert root_role in roles


def test_list_enforces_permission(role_svc: RoleService, permission_svc_mock: PermissionService):
    roles = role_svc.list(root)
    permission_svc_mock.enforce.assert_called_once_with(
        root, 'role.list', 'role/')


def test_details(role_svc: RoleService):
    details = role_svc.details(root, ambassador_role.id)
    assert details.id == ambassador_role.id
    assert details.name == ambassador_role.name
    assert ambassador_permission in details.permissions


def test_details_enforces_permission(role_svc: RoleService, permission_svc_mock: PermissionService):
    role_svc.details(root, ambassador_role.id)
    permission_svc_mock.enforce.assert_called_once_with(
        root, 'role.details', f'role/{ambassador_role.id}')


def test_grant_permission(role_svc: RoleService, permission_svc_mock: PermissionService):
    perm = Permission(action='checkin.read', resource='checkin')
    role_svc.grant_permission(root, ambassador_role.id, perm)
    permission_svc_mock.grant.assert_called_once()


def test_grant_permission_enforces_permission(role_svc: RoleService, permission_svc_mock: PermissionService):
    perm = Permission(action='checkin.read', resource='checkin')
    role_svc.grant_permission(root, ambassador_role.id, perm)
    permission_svc_mock.enforce.assert_any_call(
        root, 'role.grant_permission', f'role/{ambassador_role.id}')


def test_revoke_permission(role_svc: RoleService, permission_svc_mock: PermissionService):
    role_svc.revoke_permission(
        root, ambassador_role.id, ambassador_permission.id)
    permission_svc_mock.revoke.assert_called_once()


def test_revoke_permission_enforces_permission(role_svc: RoleService, permission_svc_mock: PermissionService):
    role_svc.revoke_permission(
        root, ambassador_role.id, ambassador_permission.id)
    permission_svc_mock.enforce.assert_any_call(
        root, 'role.revoke_permission', f'role/{ambassador_role.id}')


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
