"""Tests for the UserService class."""

import pytest
from sqlalchemy.orm import Session

# Tested Dependencies
from ...models.user import User, NewUser
from ...models.pagination import PaginationParams
from ...services import UserService, PermissionService
from ...services.exceptions import ResourceNotFoundException

from .auth_scenario import arrange_auth_scenario
from .fixtures import user_svc, user_svc_integration, permission_svc_mock

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_get(session: Session, user_svc_integration: UserService):
    """Test that a user can be retrieved by PID."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    user = user_svc_integration.get(scenario.ambassador.pid)

    # Assert
    assert user is not None
    assert user.id == scenario.ambassador.id
    assert user.pid == scenario.ambassador.pid
    assert user.onyen == scenario.ambassador.onyen
    assert user.email == scenario.ambassador.email
    assert user.permissions == [
        scenario.ambassador_permission,
        scenario.ambassador_permission_coworking_reservation,
    ]


def test_get_nonexistent(user_svc_integration: UserService):
    """Test that a nonexistent PID returns None."""
    assert user_svc_integration.get(423) is None


def test_get_by_id(session: Session, user_svc_integration: UserService):
    """Test that a user can be retrieved by their ID"""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    user = user_svc_integration.get_by_id(scenario.ambassador.id)  # type: ignore

    # Assert
    assert user is not None
    assert user.id == scenario.ambassador.id
    assert user.pid == scenario.ambassador.pid


def test_get_by_id_nonexistent(user_svc_integration: UserService):
    """Test that a user id that does not exist returns None"""
    with pytest.raises(ResourceNotFoundException):
        user_svc_integration.get_by_id(423)


def test_search_by_first_name(session: Session, user_svc: UserService):
    """Test that a user can be retrieved by Searching for their first name."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "amy")

    # Assert
    assert len(users) == 1
    assert users[0].id == scenario.ambassador.id
    assert users[0].pid == scenario.ambassador.pid
    assert users[0].onyen == scenario.ambassador.onyen
    assert users[0].email == scenario.ambassador.email


def test_search_by_last_name(session: Session, user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their last name."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "bassad")

    # Assert
    assert len(users) == 1
    assert users[0].id == scenario.ambassador.id
    assert users[0].pid == scenario.ambassador.pid
    assert users[0].onyen == scenario.ambassador.onyen
    assert users[0].email == scenario.ambassador.email


def test_search_full_name(session: Session, user_svc: UserService):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "Amy Ambassad")

    # Assert
    assert len(users) == 1
    assert users[0].id == scenario.ambassador.id
    assert users[0].pid == scenario.ambassador.pid
    assert users[0].onyen == scenario.ambassador.onyen
    assert users[0].email == scenario.ambassador.email


def test_search_by_onyen(session: Session, user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their onyen."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "xlst")

    # Assert
    assert len(users) == 1
    assert users[0].id == scenario.ambassador.id
    assert users[0].pid == scenario.ambassador.pid
    assert users[0].onyen == scenario.ambassador.onyen
    assert users[0].email == scenario.ambassador.email


def test_search_by_email(session: Session, user_svc: UserService):
    """Test that a user can be retrieved by Searching for part of their email."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "amam")

    # Assert
    assert len(users) == 1
    assert users[0].id == scenario.ambassador.id
    assert users[0].pid == scenario.ambassador.pid
    assert users[0].onyen == scenario.ambassador.onyen
    assert users[0].email == scenario.ambassador.email


def test_search_match_multiple(session: Session, user_svc: UserService):
    """Test that many users result from an ambiguous search pattern."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "@unc.edu")

    # Assert
    assert len(users) == len(scenario.users)


def test_search_no_match(session: Session, user_svc: UserService):
    """Test that no users result from a search with no matches."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "xyz")

    # Assert
    assert len(users) == 0


def test_search_by_pid_does_not_exist(session: Session, user_svc: UserService):
    """Test searching for a partial PID that does not exist."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "123")

    # Assert
    assert len(users) == 0


def test_search_by_pid_rhonda(session: Session, user_svc: UserService):
    """Test searching for a partial PID that does exist."""
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    users = user_svc.search(scenario.ambassador, "999")

    # Assert
    assert len(users) == 1
    assert users[0] == scenario.root


def test_list(session: Session, user_svc: UserService):
    """Test that a paginated list of users can be produced."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    pagination_params = PaginationParams(page=0, page_size=2, order_by="id", filter="")

    # Act
    users = user_svc.list(scenario.ambassador, pagination_params)

    # Assert
    assert len(users.items) == 2
    assert users.items[0].id == scenario.root.id
    assert users.items[1].id == scenario.ambassador.id


def test_list_second_page(session: Session, user_svc: UserService):
    """Test that subsequent pages of users are produced."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    pagination_params = PaginationParams(page=1, page_size=2, order_by="id", filter="")

    # Act
    users = user_svc.list(scenario.ambassador, pagination_params)

    # Assert
    assert len(users.items) == 2
    assert users.items[0].id == scenario.user.id


def test_list_beyond(session: Session, user_svc: UserService):
    """Test that no users are produced when the end of the list is reached."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    pagination_params = PaginationParams(page=3, page_size=2, order_by="id", filter="")

    # Act
    users = user_svc.list(scenario.ambassador, pagination_params)

    # Assert
    assert len(users.items) == 0


def test_list_order_by(session: Session, user_svc: UserService):
    """Test that users are ordered by the specified field."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    pagination_params = PaginationParams(
        page=0, page_size=len(scenario.users), order_by="first_name", filter=""
    )

    # Act
    users = user_svc.list(scenario.ambassador, pagination_params)

    # Assert
    assert len(users.items) == len(scenario.users)
    user_models_copy = scenario.users[:]
    user_models_copy.sort(key=lambda user: user.first_name)
    for i in range(len(users.items)):
        assert users.items[i].id == user_models_copy[i].id


def test_list_filter(session: Session, user_svc: UserService):
    """Test that users are filtered by search criteria."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    pagination_params = PaginationParams(
        page=0, page_size=3, order_by="id", filter="amy"
    )

    # Act
    users = user_svc.list(scenario.ambassador, pagination_params)

    # Assert
    assert len(users.items) == 1
    assert users.items[0].id == scenario.ambassador.id


def test_list_enforces_permission(
    session: Session,
    user_svc: UserService,
    permission_svc_mock: PermissionService,
):
    """Test that user.list on user/ is enforced by the list method"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    pagination_params = PaginationParams(page=0, page_size=3, order_by="id", filter="")

    # Act
    user_svc.list(scenario.ambassador, pagination_params)

    # Assert
    permission_svc_mock.enforce.assert_called_with(
        scenario.ambassador, "user.list", "user/"
    )


def test_create_user_as_user_registration(user_svc: UserService):
    """Test that a user can be created for registration purposes."""
    new_user = NewUser(pid=123456789, onyen="new_user", email="new_user@unc.edu")
    created_user = user_svc.create(new_user, new_user)
    assert created_user is not None
    assert created_user.id is not None


def test_create_user_as_root(session: Session, user_svc: UserService):
    """Test that a user can be created by a root user as an administrator."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    new_user = NewUser(pid=123456789, onyen="new_user", email="new_user@unc.edu")

    # Act
    created_user = user_svc.create(scenario.root, new_user)

    # Assert
    assert created_user is not None
    assert created_user.id is not None


def test_create_user_enforces_permission(
    session: Session,
    user_svc: UserService,
    permission_svc_mock: PermissionService,
):
    """Test that user.create on user/ is enforced by the create method"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    new_user = NewUser(pid=123456789, onyen="new_user", email="new_user@unc.edu")

    # Act
    user_svc.create(scenario.root, new_user)

    # Assert
    permission_svc_mock.enforce.assert_called_with(
        scenario.root, "user.create", "user/"
    )


def test_update_user_as_user(
    session: Session,
    user_svc: UserService,
    permission_svc_mock: PermissionService,
):
    """Test that a user can update their own information."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(scenario.ambassador.pid)
    assert user is not None
    user.first_name = "Andy"
    user.last_name = "Ambassy"

    # Act
    updated_user = user_svc.update(scenario.ambassador, user)

    # Assert
    assert updated_user is not None
    assert updated_user.id == scenario.ambassador.id
    assert updated_user.first_name == "Andy"
    assert updated_user.last_name == "Ambassy"


def test_update_user_as_root(
    session: Session,
    user_svc: UserService,
    permission_svc_mock: PermissionService,
):
    """Test that a user can be updated by a root user as an administrator."""
    # Arrange
    scenario = arrange_auth_scenario(session)
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(scenario.ambassador.pid)
    assert user is not None
    user.first_name = "Andy"
    user.last_name = "Ambassy"

    # Act
    updated_user = user_svc.update(scenario.root, user)

    # Assert
    assert updated_user is not None
    assert updated_user.id == scenario.ambassador.id
    assert updated_user.first_name == "Andy"
    assert updated_user.last_name == "Ambassy"


def test_update_user_enforces_permission(
    session: Session,
    user_svc: UserService,
    permission_svc_mock: PermissionService,
):
    """Test that user.update on user/ is enforced by the update method"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    permission_svc_mock.get_permissions.return_value = []
    user = user_svc.get(scenario.ambassador.pid)
    assert user is not None

    # Act
    user_svc.update(scenario.root, user)

    # Assert
    permission_svc_mock.enforce.assert_called_with(
        scenario.root, "user.update", f"user/{user.id}"
    )


def test_new_user_accepted_agreement_is_false(
    session: Session, user_svc: UserService
):
    """Test that makes sure newly registered users have not accepted the agreement"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    new_user = NewUser(pid=123456789, onyen="new_user", email="new_user@unc.edu")

    # Act
    user_svc.create(scenario.root, new_user)

    # Assert
    assert new_user.accepted_community_agreement == False


def test_update_profile_community_agreement_stays_false(
    session: Session, user_svc: UserService
):
    """Tests that users who update their profile will still have to accept agreement if they have not yet"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    current_user = user_svc.get(scenario.user.pid)
    assert current_user is not None
    current_user.first_name = "Sam"
    current_user.accepted_community_agreement = False
    assert current_user.accepted_community_agreement == False

    # Act
    updated_user = user_svc.update(scenario.root, current_user)

    # Assert
    assert updated_user is not None
    assert updated_user.first_name == "Sam"
    assert updated_user.accepted_community_agreement == False


def test_update_profile_community_agreement_stays_true(
    session: Session, user_svc: UserService
):
    """Tests that users who update their profile won't have to accept agreement if they have previously"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    current_user = user_svc.get(scenario.user.pid)
    assert current_user is not None
    current_user.first_name = "Sam"
    current_user.accepted_community_agreement = True
    assert current_user.accepted_community_agreement == True

    # Act
    updated_user = user_svc.update(scenario.root, current_user)

    # Assert
    assert updated_user is not None
    assert updated_user.first_name == "Sam"
    assert updated_user.accepted_community_agreement == True


def test_update_profile_then_accept_community_agreement(
    session: Session, user_svc: UserService
):
    """Tests to make sure fields are changed correctly after updating profile, then accepting agreement for first time"""
    # Arrange
    scenario = arrange_auth_scenario(session)
    current_user = user_svc.get(scenario.user.pid)
    assert current_user is not None
    current_user.first_name = "Sam"
    current_user.accepted_community_agreement = False

    # Act
    updated_user = user_svc.update(scenario.root, current_user)

    # Assert
    assert updated_user is not None
    assert updated_user.first_name == "Sam"
    assert updated_user.accepted_community_agreement == False
    updated_user.accepted_community_agreement = True
    assert updated_user.accepted_community_agreement == True
