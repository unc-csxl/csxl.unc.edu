"""Mock data for organization roles."""

import pytest
import datetime
from sqlalchemy.orm import Session
from ...models.org_role import OrgRole
from ...entities.org_role_entity import OrgRoleEntity

from .reset_table_id_seq import reset_table_id_seq
import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

cads_leader_role = OrgRole(
    id=1,
    user_id=4,
    org_id=1,
    membership_type=2,
    timestamp=datetime.datetime.fromtimestamp(1690732800),
)

super_role = OrgRole(
    id=1,
    user_id=1,
    org_id=1,
    membership_type=0,
    timestamp=datetime.datetime.fromtimestamp(1690732800),
)

org_roles = [cads_leader_role, super_role]

to_add = OrgRole(
    user_id=2,
    org_id=1,
    membership_type=1,
    timestamp=datetime.datetime.fromtimestamp(1690732800),
)

to_star = OrgRole(
    user_id=3,
    org_id=1,
    membership_type=0,
    timestamp=datetime.datetime.fromtimestamp(1690732800),
)

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake org role data into the test session."""

    global org_roles

    # Create entities for test org role data
    entities = []
    for org_role in org_roles:
        entity = OrgRoleEntity.from_model(org_role)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, OrgRoleEntity, OrgRoleEntity.id, len(org_roles) + 1)

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
