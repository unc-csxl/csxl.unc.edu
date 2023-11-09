"""Mock data for permissions in the system."""

import pytest
from sqlalchemy.orm import Session
from ...entities.permission_entity import PermissionEntity

from ...models.permission import Permission

from . import role_data
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

root_role_permission = Permission(id=1, action="*", resource="*")
ambassador_permission = Permission(id=2, action="checkin.create", resource="checkin")
ambassador_permission_coworking_reservation = Permission(
    id=3, action="coworking.reservation.*", resource="*"
)
permissions = [
    root_role_permission,
    ambassador_permission,
    ambassador_permission_coworking_reservation,
]


def insert_fake_data(session: Session):
    root_permission_entity = PermissionEntity(
        id=root_role_permission.id,
        role_id=role_data.root_role.id,
        action=root_role_permission.action,
        resource=root_role_permission.resource,
    )
    session.add(root_permission_entity)

    for i in range(1, len(permissions)):
        ambassador_permission_entity = PermissionEntity(
            id=permissions[i].id,
            role_id=role_data.ambassador_role.id,
            action=permissions[i].action,
            resource=permissions[i].resource,
        )
        session.add(ambassador_permission_entity)

    reset_table_id_seq(
        session, PermissionEntity, PermissionEntity.id, len(permissions) + 1
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
