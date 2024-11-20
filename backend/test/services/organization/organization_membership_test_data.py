import pytest
from sqlalchemy.orm import Session
from ....models.organization import Organization
from ....entities.organization_entity import OrganizationEntity
from ....models.organization_membership import OrganizationMembership
from ....models.organization_role import OrganizationRole
from ....entities.organization_membership_entity import OrganizationMembershipEntity
from ....models.user import User
from ....entities.user_entity import UserEntity

from ..reset_table_id_seq import reset_table_id_seq

# Sample objects

# Sample Organization
cads = Organization(
    id=1,
    name="Carolina Analytics & Data Science Club",
    shorthand="CADS",
    slug="cads",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    short_description="Provides students interested in Data Science opportunities to grow.",
    long_description="CADS provides students interested in Data Science opportunities to grow personally, intellectually, professionally, and socially among a support network of students, professors, and career professionals. This mission is to be accomplished through events, including a speaker series from industry professionals, data case competition, workshops, and investigating and analyzing University and community data to drive community-based projects and solutions.",
    website="https://carolinadata.unc.edu/",
    email="carolinadatascience@gmail.com",
    instagram="https://www.instagram.com/carolinadatascience/",
    linked_in="https://www.linkedin.com/company/carolina-data/",
    youtube="https://www.youtube.com/channel/UCO44Yjhjuo5-TLUCAaP0-cQ",
    heel_life="https://heellife.unc.edu/organization/carolinadatascience",
    public=True,
)

# Sample Users
root = User(
    id=1,
    pid=999999999,
    onyen="root",
    email="root@unc.edu",
    first_name="Rhonda",
    last_name="Root",
    pronouns="She / Her / Hers",
    accepted_community_agreement=True,
)

ambassador = User(
    id=2,
    pid=888888888,
    onyen="xlstan",
    email="amam@unc.edu",
    first_name="Amy",
    last_name="Ambassador",
    pronouns="They / Them / Theirs",
    accepted_community_agreement=True,
)

user = User(
    id=3,
    pid=111111111,
    onyen="user",
    email="user@unc.edu",
    first_name="Sally",
    last_name="Student",
    pronouns="She / They",
    accepted_community_agreement=True,
)

# Sample Memberships
member_1 = OrganizationMembership(
    id=1,
    user=root,
    organization_id=cads.id,
    organization_slug=cads.slug,
    organization_role=OrganizationRole.ADMIN,
)

member_2 = OrganizationMembership(
    id=2,
    user=ambassador,
    organization_id=cads.id,
    organization_slug=cads.slug,
    organization_role=OrganizationRole.OFFICER,
)

member_to_add = OrganizationMembership(
    id=3,
    user=user,
    organization_id=cads.id,
    organization_slug=cads.slug,
    organization_role=OrganizationRole.MEMBER,
)

roster = [member_1, member_2]


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global roster

    # Create entities for test organization data
    entities = []
    for org in roster:
        entity = OrganizationMembershipEntity.from_model(org)
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
