"""Fixtures used for testing the core services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ...services import (
    PermissionService,
    UserService,
    RoleService,
    OrganizationService,
    OrgRoleService,
    EventService,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    return PermissionService(session)


@pytest.fixture()
def permission_svc_mock():
    """This mocks the PermissionService class to avoid testing its implementation here."""
    return create_autospec(PermissionService)


@pytest.fixture()
def user_svc(session: Session, permission_svc_mock: PermissionService):
    """This fixture is used to test the UserService class with a mocked PermissionService."""
    return UserService(session, permission_svc_mock)


@pytest.fixture()
def user_svc_integration(session: Session):
    """This fixture is used to test the UserService class with a real PermissionService."""
    return UserService(session, PermissionService(session))


@pytest.fixture()
def role_svc(session: Session, permission_svc_mock: PermissionService):
    return RoleService(session, permission_svc_mock)


@pytest.fixture()
def organization_svc_integration(session: Session):
    """This fixture is used to test the OrganizationService class with a real PermissionService."""
    return OrganizationService(
        session,
        PermissionService(session),
        OrgRoleService(session, PermissionService(session)),
    )


@pytest.fixture()
def event_svc_integration(session: Session):
    """This fixture is used to test the EventService class with a real PermissionService."""
    return EventService(session, OrgRoleService(session, PermissionService(session)))


@pytest.fixture()
def org_role_svc_integration(session: Session):
    """This fixture is used to test the OrgRoleService class with a real PermissionService."""
    return OrgRoleService(session, PermissionService(session))
