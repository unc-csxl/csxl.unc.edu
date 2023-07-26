"""Mock data for specific roles.

Two roles are setup for testing and development purposes:

1. root (will have sudo permissions to do everything)
2. ambassador (will have a subset of specific permissions)
"""

import pytest
from sqlalchemy.orm import Session
from .reset_table_id_seq import reset_table_id_seq
from ...entities.role_entity import RoleEntity
from ...models.role import Role

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

root_role = Role(id=1, name="root")
root_users = []
ambassador_role = Role(id=2, name="ambassadors")

roles = [root_role, ambassador_role]


def insert_fake_data(session: Session):
    for role in roles:
        entity = RoleEntity.from_model(role)
        session.add(entity)

    reset_table_id_seq(session, RoleEntity, RoleEntity.id, len(roles) + 1)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
