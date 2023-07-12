"""User data for coworking service tests."""

import pytest
from sqlalchemy.orm import Session
from ....entities import UserEntity, RoleEntity, PermissionEntity
from ....models import User, Role, Permission

root = User(
    id=1,
    pid=999999999,
    onyen="root",
    email="root@unc.edu",
    first_name="Rhonda",
    last_name="Root",
)
root_role = Role(id=1, name="root")

ambassador = User(
    id=2,
    pid=888888888,
    onyen="xlstan",
    email="amam@unc.edu",
    first_name="Amy",
    last_name="Ambassador",
)
ambassador_role = Role(id=2, name="ambassadors")
ambassador_permission: Permission

user = User(
    id=3,
    pid=111111111,
    onyen="user",
    email="user@unc.edu",
    first_name="Sally",
    last_name="Student",
)

users = [root, ambassador, user]
roles = [root_role, ambassador_role]

def insert_fake_data(test_session: Session):
    """This function is also used in development data setup."""

    # Bootstrap root User and Role
    root_user_entity = UserEntity.from_model(root)
    test_session.add(root_user_entity)
    root_role_entity = RoleEntity.from_model(root_role)
    root_role_entity.users.append(root_user_entity)
    test_session.add(root_role_entity)
    root_permission_entity = PermissionEntity(
        action="*", resource="*", role=root_role_entity
    )
    test_session.add(root_permission_entity)

    # Bootstrap ambassador and role
    ambassador_entity = UserEntity.from_model(ambassador)
    test_session.add(ambassador_entity)
    ambassador_role_entity = RoleEntity.from_model(ambassador_role)
    ambassador_role_entity.users.append(ambassador_entity)
    test_session.add(ambassador_role_entity)
    ambassador_permission_entity = PermissionEntity(
        action="coworking.checkin", resource="*", role=ambassador_role_entity
    )
    test_session.add(ambassador_permission_entity)

    global ambassador_permission
    ambassador_permission = ambassador_permission_entity.to_model()

    # Bootstrap user without any special perms
    user_entity = UserEntity.from_model(user)
    test_session.add(user_entity)

@pytest.fixture(autouse=True)
def fake_data_fixture(test_session: Session):
    insert_fake_data(test_session)
    test_session.commit()
