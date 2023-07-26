"""Tests for the UserService class."""

# Tested Dependencies
from ...models import User, PaginationParams
from ...services import UserService, PermissionService

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import user_svc, user_svc_integration, permission_svc_mock

# Data Models for Fake Data Inserted in Setup
from .user_data import root, ambassador, user
from .permission_data import ambassador_permission


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
    users = user_svc.search(ambassador, "amy")
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_by_last_name(user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their last name."""
    users = user_svc.search(ambassador, "bassad")
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_by_onyen(user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their onyen."""
    users = user_svc.search(ambassador, "xlst")
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_by_email(user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their email."""
    users = user_svc.search(ambassador, "amam")
    assert len(users) == 1
    assert users[0].id == ambassador.id
    assert users[0].pid == ambassador.pid
    assert users[0].onyen == ambassador.onyen
    assert users[0].email == ambassador.email


def test_search_match_multiple(user_svc: UserService):
    """Test that many users result from an ambiguous search pattern."""
    users = user_svc.search(ambassador, "@unc.edu")
    assert len(users) == 3


def test_search_no_match(user_svc: UserService):
    """Test that no users result from a search with no matches."""
    users = user_svc.search(ambassador, "xyz")
    assert len(users) == 0


def test_list(user_svc: UserService):
    """Test that a paginated list of users can be produced."""
    pagination_params = PaginationParams(page=0, page_size=2, order_by="id", filter="")
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 2
    assert users.items[0].id == root.id
    assert users.items[1].id == ambassador.id


def test_list_second_page(user_svc: UserService):
    """Test that subsequent pages of users are produced."""
    pagination_params = PaginationParams(page=1, page_size=2, order_by="id", filter="")
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 1
    assert users.items[0].id == user.id


def test_list_beyond(user_svc: UserService):
    """Test that no users are produced when the end of the list is reached."""
    pagination_params = PaginationParams(page=2, page_size=2, order_by="id", filter="")
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 0


def test_list_order_by(user_svc: UserService):
    """Test that users are ordered by the specified field."""
    pagination_params = PaginationParams(
        page=0, page_size=3, order_by="first_name", filter=""
    )
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 3
    assert users.items[0].id == ambassador.id
    assert users.items[1].id == root.id
    assert users.items[2].id == user.id


def test_list_filter(user_svc: UserService):
    """Test that users are filtered by search criteria."""
    pagination_params = PaginationParams(
        page=0, page_size=3, order_by="id", filter="amy"
    )
    users = user_svc.list(ambassador, pagination_params)
    assert len(users.items) == 1
    assert users.items[0].id == ambassador.id


def test_list_enforces_permission(
    user_svc: UserService, permission_svc_mock: PermissionService
):
    """Test that user.list on user/ is enforced by the list method"""
    pagination_params = PaginationParams(page=0, page_size=3, order_by="id", filter="")
    user_svc.list(ambassador, pagination_params)
    permission_svc_mock.enforce.assert_called_with(ambassador, "user.list", "user/")


def test_create_user_as_user_registration(user_svc: UserService):
    """Test that a user can be created for registration purposes."""
    new_user = User(pid=123456789, onyen="new_user", email="new_user@unc.edu")
    created_user = user_svc.create(new_user, new_user)
    assert created_user is not None
    assert created_user.id is not None


def test_create_user_as_root(user_svc: UserService):
    """Test that a user can be created by a root user as an administrator."""
    new_user = User(pid=123456789, onyen="new_user", email="new_user@unc.edu")
    created_user = user_svc.create(root, new_user)
    assert created_user is not None
    assert created_user.id is not None


def test_create_user_enforces_permission(
    user_svc: UserService, permission_svc_mock: PermissionService
):
    """Test that user.create on user/ is enforced by the create method"""
    new_user = User(pid=123456789, onyen="new_user", email="new_user@unc.edu")
    user_svc.create(root, new_user)
    permission_svc_mock.enforce.assert_called_with(root, "user.create", "user/")


def test_update_user_as_user(
    user_svc: UserService, permission_svc_mock: PermissionService
):
    """Test that a user can update their own information."""
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(ambassador.pid)
    user.first_name = "Andy"
    user.last_name = "Ambassy"
    updated_user = user_svc.update(ambassador, user)
    assert updated_user is not None
    assert updated_user.id == ambassador.id
    assert updated_user.first_name == "Andy"
    assert updated_user.last_name == "Ambassy"


def test_update_user_as_root(
    user_svc: UserService, permission_svc_mock: PermissionService
):
    """Test that a user can be updated by a root user as an administrator."""
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(ambassador.pid)
    user.first_name = "Andy"
    user.last_name = "Ambassy"
    updated_user = user_svc.update(root, user)
    assert updated_user is not None
    assert updated_user.id == ambassador.id
    assert updated_user.first_name == "Andy"
    assert updated_user.last_name == "Ambassy"


def test_update_user_enforces_permission(
    user_svc: UserService, permission_svc_mock: PermissionService
):
    """Test that user.update on user/ is enforced by the update method"""
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(ambassador.pid)
    user_svc.update(root, user)
    permission_svc_mock.enforce.assert_called_with(
        root, "user.update", f"user/{user.id}"
    )
