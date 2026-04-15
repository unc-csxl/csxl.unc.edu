from dataclasses import dataclass

from sqlalchemy.orm import Session

from ....entities.organization_entity import OrganizationEntity
from ....models.organization import Organization
from ..reset_table_id_seq import reset_table_id_seq


@dataclass(frozen=True)
class OrganizationScenario:
    cads: Organization
    cssg: Organization
    appteam: Organization
    to_add: Organization
    to_add_conflicting_id: Organization
    new_cads: Organization

    @property
    def organizations(self) -> list[Organization]:
        return [self.cads, self.cssg, self.appteam]


def build_organization_scenario() -> OrganizationScenario:
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
    )
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
    )
    to_add_conflicting_id = to_add.model_copy(update={"id": 2})
    new_cads = cads.model_copy(update={"website": "https://cads.cs.unc.edu/"})

    return OrganizationScenario(
        cads=cads,
        cssg=cssg,
        appteam=appteam,
        to_add=to_add,
        to_add_conflicting_id=to_add_conflicting_id,
        new_cads=new_cads,
    )


def arrange_organization_scenario(session: Session) -> OrganizationScenario:
    scenario = build_organization_scenario()
    session.add_all(
        [OrganizationEntity.from_model(org) for org in scenario.organizations]
    )
    reset_table_id_seq(
        session,
        OrganizationEntity,
        OrganizationEntity.id,
        len(scenario.organizations) + 1,
    )
    session.commit()
    return scenario