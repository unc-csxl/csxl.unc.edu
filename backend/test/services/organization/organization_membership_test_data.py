import pytest
from sqlalchemy.orm import Session
from ....models.organization_membership import (
    OrganizationMembership,
    OrganizationMembershipRegistration,
)
from ....entities.organization_membership_entity import OrganizationMembershipEntity
from ....models.public_user import PublicUser
from .organization_test_data import cads, appteam
from ..academics import term_data

from ..reset_table_id_seq import reset_table_id_seq

# Sample objects

# Sample Users
root = PublicUser(
    id=1,
    onyen="root",
    email="root@unc.edu",
    first_name="Rhonda",
    last_name="Root",
    pronouns="She / Her / Hers",
)

ambassador = PublicUser(
    id=2,
    onyen="xlstan",
    email="amam@unc.edu",
    first_name="Amy",
    last_name="Ambassador",
    pronouns="They / Them / Theirs",
)

user = PublicUser(
    id=3,
    onyen="user",
    email="user@unc.edu",
    first_name="Sally",
    last_name="Student",
    pronouns="She / They",
)

# Sample Memberships
member_1 = OrganizationMembershipRegistration(
    id=1,
    user_id=root.id,
    organization_id=cads.id,
    title="President",
    is_admin=True,
    term_id=term_data.current_term.id,
)

member_2 = OrganizationMembershipRegistration(
    id=2,
    user_id=ambassador.id,
    organization_id=cads.id,
    title="Ambassador",
    is_admin=False,
    term_id=term_data.current_term.id,
)

member_to_add = OrganizationMembershipRegistration(
    user_id=user.id,
    organization_id=appteam.id,
    term_id=term_data.current_term.id,
)

cads_membership = OrganizationMembership(
    id=2,
    user=ambassador,
    organization_id=cads.id,
    organization_name=cads.name,
    organization_slug=cads.slug,
    title="Treasurer",
    is_admin=True,
    term=term_data.current_term,
)

bad_membership = OrganizationMembership(
    id=100,
    user=ambassador,
    organization_id=cads.id,
    organization_name=cads.name,
    organization_slug=cads.slug,
    title="Treasurer",
    is_admin=True,
    term=term_data.current_term,
)

roster = [member_1, member_2]


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global roster

    # Create entities for test organization data
    entities = []
    for membership in roster:
        entity = OrganizationMembershipEntity.from_model(membership)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session,
        OrganizationMembershipEntity,
        OrganizationMembershipEntity.id,
        len(roster) + 1,
    )

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
