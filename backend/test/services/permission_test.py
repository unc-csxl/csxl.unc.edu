import pytest

from sqlalchemy.orm import Session
from ...models import User, Role, Permission
from ...entities import UserEntity, RoleEntity, PermissionEntity
from ...services import PermissionService

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


@pytest.fixture()
def permission(test_session: Session):
    return PermissionService(test_session)


def test_no_permission(permission: PermissionService):
    assert permission.check(user, 'permission.grant',
                            'permission') is False
    assert permission.check(user, 'user.delete', 'user/1') is False


def test_grant_role_permission(permission: PermissionService):
    assert permission.check(ambassador, 'checkin.delete', 'checkin') is False
    p = Permission(action='checkin.delete', resource='*')
    permission.grant(root, ambassador_role, p)
    assert permission.check(ambassador, 'checkin.delete', 'checkin')


def test_revoke_role_permission(permission: PermissionService):
    assert permission.check(ambassador, 'checkin.create', 'checkin')
    permission.revoke(root, ambassador_permission)
    assert permission.check(ambassador, 'checkin.create', 'checkin') is False


def test_root_resource_access(permission: PermissionService):
    assert permission.check(root, 'access_control.grant', 'access_control')
    assert permission.check(root, 'user.delete', 'user/1')


def test_check_catch_all_permission(permission: PermissionService):
    p = Permission(action='*', resource='*')
    assert permission._check_permission(p, 'permission.grant', '*')
    assert permission._check_permission(p, 'permission.grant', 'checkin')
    assert permission._check_permission(p, 'permission.revoke', 'checkin.*')
    assert permission._check_permission(p, 'checkin.delete', 'checkin/1')


def test_check_catch_all_resource_permission(permission: PermissionService):
    p = Permission(action='permission.grant', resource='*')
    assert permission._check_permission(p, 'permission.grant', '*')
    assert permission._check_permission(p, 'permission.grant', 'checkin')
    assert permission._check_permission(
        p, 'permission.revoke', 'checkin.*') is False
    assert permission._check_permission(
        p, 'checkin.delete', 'checkin/1') is False


def test_check_specific_resource_permission(permission: PermissionService):
    p = Permission(action='permission.grant', resource='checkin*')
    assert permission._check_permission(p, 'permission.grant', '*') is False
    assert permission._check_permission(p, 'permission.grant', 'checkin')
    assert permission._check_permission(
        p, 'permission.revoke', 'checkin.*') is False
    assert permission._check_permission(
        p, 'checkin.delete', 'checkin/1') is False


def test_check_specific_permission(permission: PermissionService):
    p = Permission(action='checkin.delete', resource='checkin/*')
    assert permission._check_permission(p, 'checkin.delete', 'checkin/1')
    assert permission._check_permission(p, 'checkin.delete', 'checkin/12')
    assert permission._check_permission(
        p, 'checkin.create', 'checkin/12') is False
    assert permission._check_permission(
        p, 'permission.revoke', 'checkin.*') is False
