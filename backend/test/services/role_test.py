"""Tests for the RoleService class."""

from sqlalchemy.orm import Session

# Tested Dependencies
from ...models import Permission, Role
from ...services import RoleService, PermissionService

from .auth_scenario import arrange_auth_scenario
from .fixtures import role_svc, permission_svc_mock

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_list(session: Session, role_svc: RoleService):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    roles = role_svc.list(scenario.root)

    # Assert
    assert len(roles) == 2
    assert scenario.ambassador_role in roles
    assert scenario.root_role in roles


def test_list_enforces_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    role_svc.list(scenario.root)

    # Assert
    permission_svc_mock.enforce.assert_called_once_with(
        scenario.root, "role.list", "role/"
    )


def test_create(session: Session, role_svc: RoleService):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    role = role_svc.create(scenario.root, "Club XL")

    # Assert
    assert role.id is not None
    assert role.id > 0
    persisted = role_svc.details(scenario.root, role.id)
    assert role.name == persisted.name


def test_create_enforces_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    role_svc.create(scenario.root, "Test")

    # Assert
    permission_svc_mock.enforce.assert_called_once_with(
        scenario.root, "role.create", "role/"
    )


def test_details(session: Session, role_svc: RoleService):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    details = role_svc.details(scenario.root, scenario.ambassador_role.id)

    # Assert
    assert details.id == scenario.ambassador_role.id
    assert details.name == scenario.ambassador_role.name
    assert scenario.ambassador_permission in details.permissions


def test_details_enforces_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    role_svc.details(scenario.root, scenario.ambassador_role.id)

    # Assert
    permission_svc_mock.enforce.assert_called_once_with(
        scenario.root,
        "role.details",
        f"role/{scenario.ambassador_role.id}",
    )


def test_grant_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)
    perm = Permission(action="checkin.read", resource="checkin")

    # Act
    role_svc.grant_permission(scenario.root, scenario.ambassador_role.id, perm)

    # Assert
    permission_svc_mock.grant.assert_called_once()


def test_grant_permission_enforces_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)
    perm = Permission(action="checkin.read", resource="checkin")

    # Act
    role_svc.grant_permission(scenario.root, scenario.ambassador_role.id, perm)

    # Assert
    permission_svc_mock.enforce.assert_any_call(
        scenario.root,
        "role.grant_permission",
        f"role/{scenario.ambassador_role.id}",
    )


def test_revoke_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    role_svc.revoke_permission(
        scenario.root,
        scenario.ambassador_role.id,
        scenario.ambassador_permission.id,
    )

    # Assert
    permission_svc_mock.revoke.assert_called_once()


def test_revoke_permission_enforces_permission(
    session: Session,
    role_svc: RoleService,
    permission_svc_mock: PermissionService,
):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act
    role_svc.revoke_permission(
        scenario.root,
        scenario.ambassador_role.id,
        scenario.ambassador_permission.id,
    )

    # Assert
    permission_svc_mock.enforce.assert_any_call(
        scenario.root,
        "role.revoke_permission",
        f"role/{scenario.ambassador_role.id}",
    )


def test_is_member(session: Session, role_svc: RoleService):
    # Arrange
    scenario = arrange_auth_scenario(session)

    # Act / Assert
    assert role_svc.is_member(
        scenario.root, scenario.ambassador_role.id, scenario.ambassador.id
    )
    assert not role_svc.is_member(
        scenario.root, scenario.ambassador_role.id, scenario.user.id
    )


def test_add_member(session: Session, role_svc: RoleService):
    # Arrange
    scenario = arrange_auth_scenario(session)
    assert not role_svc.is_member(
        scenario.root, scenario.ambassador_role.id, scenario.user.id
    )

    # Act
    role_svc.add_member(scenario.root, scenario.ambassador_role.id, scenario.user)

    # Assert
    assert role_svc.is_member(
        scenario.root, scenario.ambassador_role.id, scenario.user.id
    )


def test_remove_member(session: Session, role_svc: RoleService):
    # Arrange
    scenario = arrange_auth_scenario(session)
    assert role_svc.is_member(
        scenario.root, scenario.ambassador_role.id, scenario.ambassador.id
    )

    # Act
    role_svc.remove_member(
        scenario.root, scenario.ambassador_role.id, scenario.ambassador.id
    )

    # Assert
    assert not role_svc.is_member(
        scenario.root, scenario.ambassador_role.id, scenario.ambassador.id
    )
