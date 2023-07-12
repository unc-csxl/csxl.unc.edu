"""Tests for the UserService class."""

from unittest.mock import create_autospec
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...models import User, Role, Permission, PaginationParams
from ...entities import UserEntity, RoleEntity, PermissionEntity
from ...services import UserService, PermissionService

# Mock Models
root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu',
            first_name='Rhonda', last_name='Root')
root_role = Role(id=1, name='root')

ambassador = User(id=2, pid=888888888, onyen='xlstan',
                  email='amam@unc.edu', first_name='Amy', last_name='Ambassador')
ambassador_role = Role(id=2, name='ambassadors')
ambassador_permission: Permission

user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu',
            first_name='Sally', last_name='Student')


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

    test_session.execute(
        text(f'ALTER SEQUENCE {UserEntity.__table__}_id_seq RESTART WITH {10}'))
    yield


@pytest.fixture()
def permission_svc_mock():
    """This mocks the PermissionService class to avoid testing its implementation here."""
    return create_autospec(PermissionService)


@pytest.fixture()
def user_svc(test_session: Session, permission_svc_mock: PermissionService):
    """This fixture is used to test the UserService class with a mocked PermissionService."""
    return UserService(test_session, permission_svc_mock)

@pytest.fixture()
def user_svc_integration(test_session: Session):
    """This fixture is used to test the UserService class with a real PermissionService."""
    return UserService(test_session, PermissionService(test_session))


def test_get(user_svc_integration: UserService):
    """Test that a user can be retrieved by PID."""
    user = user_svc_integration.get(ambassador.pid)
    assert user is not None
    assert user.id == ambassador.id
    assert user.pid == ambassador.pid
    assert user.onyen == ambassador.onyen
    assert user.email == ambassador.email
    assert user.permissions == [ambassador_permission]


def test_search_by_first_name(user_svc: UserService):
    """Test that a user can be retrieved by Searching for their first name."""
    users = user_svc.search(ambassador, 'amy')
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_by_last_name(user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their last name."""
    users = user_svc.search(ambassador, 'bassad')
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_by_onyen(user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their onyen."""
    users = user_svc.search(ambassador, 'xlst')
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_by_email(user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their email."""
    users = user_svc.search(ambassador, 'amam')
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_match_multiple(user_svc: UserService):
    """Test that many users result from an ambiguous search pattern."""
    users = user_svc.search(ambassador, '@unc.edu')
    assert len(users) == 3


def test_search_no_match(user_svc: UserService):
    """Test that no users result from a search with no matches."""
    users = user_svc.search(ambassador, 'xyz')
    assert len(users) == 0


def test_list(user_svc: UserService):
    """Test that a paginated list of users can be produced."""
    pagination_params = PaginationParams(
        page=0, page_size=2, order_by='id', filter='')
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 2
    assert users.items[0].id == root.id
    assert users.items[1].id == ambassador.id


def test_list_second_page(user_svc: UserService):
    """Test that subsequent pages of users are produced."""
    pagination_params = PaginationParams(
        page=1, page_size=2, order_by='id', filter='')
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 1
    assert users.items[0].id == user.id


def test_list_beyond(user_svc: UserService):
    """Test that no users are produced when the end of the list is reached."""
    pagination_params = PaginationParams(
        page=2, page_size=2, order_by='id', filter='')
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 0


def test_list_order_by(user_svc: UserService):
    """Test that users are ordered by the specified field."""
    pagination_params = PaginationParams(
        page=0, page_size=3, order_by='first_name', filter='')
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 3
    assert users.items[0].id == ambassador.id
    assert users.items[1].id == root.id
    assert users.items[2].id == user.id


def test_list_filter(user_svc: UserService):
    """Test that users are filtered by search criteria."""
    pagination_params = PaginationParams(
        page=0, page_size=3, order_by='id', filter='amy')
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 1
    assert users.items[0].id == ambassador.id


def test_list_enforces_permission(user_svc: UserService, permission_svc_mock: PermissionService):
    """Test that user.list on user/ is enforced by the list method"""
    pagination_params = PaginationParams(
        page=0, page_size=3, order_by='id', filter='')
    user_svc.list(ambassador, pagination_params)
    permission_svc_mock.enforce.assert_called_with(
        ambassador, 'user.list', 'user/')


def test_create_user_as_user_registration(user_svc: UserService):
    """Test that a user can be created for registration purposes."""
    new_user = User(pid=123456789, onyen='new_user', email='new_user@unc.edu')
    created_user = user_svc.create(new_user, new_user)
    assert created_user is not None
    assert created_user.id is not None


def test_create_user_as_root(user_svc: UserService):
    """Test that a user can be created by a root user as an administrator."""
    new_user = User(pid=123456789, onyen='new_user', email='new_user@unc.edu')
    created_user = user_svc.create(root, new_user)
    assert created_user is not None
    assert created_user.id is not None


def test_create_user_enforces_permission(user_svc: UserService, permission_svc_mock: PermissionService):
    """Test that user.create on user/ is enforced by the create method"""
    new_user = User(pid=123456789, onyen='new_user', email='new_user@unc.edu')
    user_svc.create(root, new_user)
    permission_svc_mock.enforce.assert_called_with(
        root, 'user.create', 'user/')


def test_update_user_as_user(user_svc: UserService, permission_svc_mock: PermissionService):
    """Test that a user can update their own information."""
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(ambassador.pid)
    user.first_name = 'Andy'
    user.last_name = 'Ambassy'
    updated_user = user_svc.update(ambassador, user)
    assert updated_user is not None
    assert updated_user.id == ambassador.id
    assert updated_user.first_name == 'Andy'
    assert updated_user.last_name == 'Ambassy'


def test_update_user_as_root(user_svc: UserService, permission_svc_mock: PermissionService):
    """Test that a user can be updated by a root user as an administrator."""
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(ambassador.pid)
    user.first_name = 'Andy'
    user.last_name = 'Ambassy'
    updated_user = user_svc.update(root, user)
    assert updated_user is not None
    assert updated_user.id == ambassador.id
    assert updated_user.first_name == 'Andy'
    assert updated_user.last_name == 'Ambassy'


def test_update_user_enforces_permission(user_svc: UserService, permission_svc_mock: PermissionService):
    """Test that user.update on user/ is enforced by the update method"""
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(ambassador.pid)
    user_svc.update(root, user)
    permission_svc_mock.enforce.assert_called_with(
        root, 'user.update', f'user/{user.id}')