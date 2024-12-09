"""Contains mock data for to run tests on the organization feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.organization import Organization
from ....models.organization_join_type import OrganizationJoinType
from ....entities.organization_entity import OrganizationEntity

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

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
    join_type=OrganizationJoinType.OPEN,
)

cssg = Organization(
    id=2,
    name="CS+Social Good",
    shorthand="CSSG",
    slug="cssg",
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
    join_type=OrganizationJoinType.APPLY,
)

appteam = Organization(
    id=3,
    name="App Team Carolina",
    shorthand="App Team",
    slug="app-team",
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
    join_type=OrganizationJoinType.APPLY,
)

queerhack = Organization(
    id=16,
    name="queer_hack",
    shorthand="queer_hack",
    slug="queer-hack",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/queerhack.jpg",
    short_description="A community for LGBTQ+ students in tech.",
    long_description="Vision: We envision a future with a tech culture that is inclusive and accessible for LGBTQ+ people. \nMission: We aim to empower LGBTQ+ students in tech by fostering peer connections and curating opportunities to grow as a programmer. Our event programming includes skill-building workshops, weekly study groups, social events, career networking opportunities, and an annual hackathon.\nWhether you're already a Computer Science major or just interested in exploring coding, we'd love for you to join the community.",
    website="http://queerhack.com/",
    email="uncqueerhack@gmail.com",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/queer_hack",
    public=False,
    join_type=OrganizationJoinType.CLOSED,
)

organizations = [cads, cssg, appteam, queerhack]
organization_names = [cads.name, cssg.name, appteam.name]

to_add = Organization(
    name="Android Development Club",
    shorthand="Android Club",
    slug="android-club",
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
    join_type=OrganizationJoinType.APPLY,
)

to_add_conflicting_id = Organization(
    id=2,
    name="Android Development Club",
    shorthand="Android Club",
    slug="android-club",
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
    join_type=OrganizationJoinType.APPLY,
)

new_cads = Organization(
    id=1,
    name="Carolina Analytics & Data Science Club",
    shorthand="CADS",
    slug="cads",
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
    join_type=OrganizationJoinType.OPEN,
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
