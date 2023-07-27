"""Mock data for organizations."""

import pytest
from sqlalchemy.orm import Session
from ...models.organization import Organization
from ...entities.organization_entity import OrganizationEntity
from ...models.user import User
from ...entities.user_entity import UserEntity
from ...models.org_role import OrgRole
from ...entities.org_role_entity import OrgRoleEntity

from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

cads = Organization(
    id=1,
    name="Carolina Analytics & Data Science Club",
    slug="CADS",
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

cssg = Organization(
    id=2,
    name="CS+Social Good",
    slug="CSSG",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cssg.png",
    short_description="We build apps for nonprofits and organizations for social good.",
    long_description="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
    website="https://cssgunc.org/",
    email="cssgunc@gmail.com",
    instagram="https://www.instagram.com/unc_cssg/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/cssg",
    public=False,
)

appteam = OrganizationEntity(
    id=3,
    name="App Team Carolina",
    slug="App Team",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/appteam.jpg",
    short_description="UNC Chapel Hill's iOS development team.",
    long_description="The mission of App Team Carolina is to create a collaborative space for UNC students to design, build, and release apps for Apple platforms. App Team Carolina's multi-faceted development process aims to leverage its individual skillsets while encouraging cooperation among team members with different levels of experience.",
    website="",
    email="",
    instagram="https://www.instagram.com/appteamcarolina/",
    linked_in="https://www.linkedin.com/company/appteamcarolina",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/appteamcarolina",
    public=False,
)

organizations = [cads, cssg, appteam]
organization_names = [cads.name, cssg.name, appteam.name]

to_add = OrganizationEntity(
    name="Android Development Club",
    slug="Android Club",
    logo="https://1000logos.net/wp-content/uploads/2016/10/Android-Logo.png",
    short_description="UNC Chapel Hill's Android development team.",
    long_description="We make super cool Android apps for the UNC CS department.",
    website="",
    email="",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="",
    public=True,
)

new_cads = OrganizationEntity(
    id=1,
    name="Carolina Analytics & Data Science Club",
    slug="CADS",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    short_description="Provides students interested in Data Science opportunities to grow.",
    long_description="CADS provides students interested in Data Science opportunities to grow personally, intellectually, professionally, and socially among a support network of students, professors, and career professionals. This mission is to be accomplished through events, including a speaker series from industry professionals, data case competition, workshops, and investigating and analyzing University and community data to drive community-based projects and solutions.",
    website="https://cads.cs.unc.edu/",
    email="carolinadatascience@gmail.com",
    instagram="https://www.instagram.com/carolinadatascience/",
    linked_in="https://www.linkedin.com/company/carolina-data/",
    youtube="https://www.youtube.com/channel/UCO44Yjhjuo5-TLUCAaP0-cQ",
    heel_life="https://heellife.unc.edu/organization/carolinadatascience",
    public=True,
)

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global organizations

    # Create entities for test organization data
    entities = []
    for org in organizations:
        entity = OrganizationEntity.from_model(org)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, OrganizationEntity, OrganizationEntity.id, len(organizations) + 1
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
