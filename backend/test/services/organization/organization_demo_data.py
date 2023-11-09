"""Contains mock data for the live demo of the organizations feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.organization import Organization
from ....entities.organization_entity import OrganizationEntity

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

appteam = OrganizationEntity(
    id=1,
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

acm = OrganizationEntity(
    id=2,
    name="ACM at Carolina",
    shorthand="ACM",
    slug="acm",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/acm.jpg",
    short_description="Largest community and professional society for Tar Heels who study computing.",
    long_description="We are a professional community of Tar Heels who study computing; we are dedicated to exploring our field, defining our interests, engaging with each other, discovering our strengths, and improving our skills.",
    website="https://linktr.ee/unc_acm",
    email="uncacm@unc.edu",
    instagram="https://www.instagram.com/unc_acm/",
    linked_in="",
    youtube="https://www.youtube.com/channel/UCkgDDL-DKsFJKpld2SosbxA",
    heel_life="https://heellife.unc.edu/organization/acm-at-carolina",
    public=False,
)

bit = OrganizationEntity(
    id=3,
    name="Black in Technology",
    shorthand="BIT",
    slug="bit",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/bit.jpg",
    short_description="Increasing Black and other ethnic participation in the fields of technology and Computer Science.",
    long_description="Black in Technology (BiT) is a student and technology-based organization, that dedicates itself to the development of intensive programs for increasing Black and other ethnic participation in the field of technology and Computer Science. BiT aims to increase the representation of Black students pursuing degrees in technology at the University of North Carolina at Chapel Hill. The primary mission of BiT is to voice the concerns of members and work to create an inclusive ecosystem for Black technology majors to thrive within the University.",
    website="https://linktr.ee/BiTunc",
    email="blackintechunc@gmail.com",
    instagram="https://www.instagram.com/uncbit/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/bit",
    public=False,
)

cads = Organization(
    id=4,
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

carvr = OrganizationEntity(
    id=5,
    name="Carolina Augmented and Virtual Reality",
    shorthand="CARVR",
    slug="carvr",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/arvr.png",
    short_description="Students explore XR technologies and connect to clients to create real-world applications.",
    long_description="CARVR is a student organization at UNC Chapel Hill that promotes student development in XR technologies. Students explore XR technologies, learn XR development, work on XR projects and connect to clients to create real-world applications. All students â€“ graduate or undergraduate, in any discipline â€“ are welcome to join!",
    website="https://arvr.web.unc.edu/",
    email="",
    instagram="https://www.instagram.com/uncarvr/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/carvr",
    public=False,
)

cssg = Organization(
    id=6,
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

ctf = OrganizationEntity(
    id=7,
    name="Cybersecurity CTF Club",
    shorthand="CTF",
    slug="ctf",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/ctf.jpg",
    short_description="Hands-on computer security club, developing practical technical abilities through workshops and competitions.",
    long_description="We primarily communicate through discord, invite link atÂ <https://discord.gg/GSdrVQ7>\nUNC-CH's hands-on computer security club, developing practical technical abilities in students and members of the local enthusiast community through lecture, workshops, and participation in competition against teams of practitioners across the world.\n\nCTF stands for Capture The Flag, a form of competitive computer security competition with a typical focus in offensive or defensive operations, or solving a wide array of challenges in a variety of categories.\n\nWe regularly practice skills in reverse engineering, system exploitation, web app auditing, forensics, and cryptography.",
    website="https://ntropy-unc.github.io/",
    email="ntropy.unc@gmail.com",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/ntropy-unc",
    public=False,
)

enablingtech = OrganizationEntity(
    id=8,
    name="Enabling Technology",
    shorthand="Enabling Tech",
    slug="enabling-tech",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/enablingtech.png",
    short_description="We create and design computer programs for children and teenagers with disabilities.",
    long_description="The Enabling Technology Club allows students at UNC to utilize their knowledge in computer science, artistic ability, and leadership skills to create and design computer programs of books and video games through Tar Heel Reader and Tar Heel Gameplay for children and teenagers with disabilities. The organization provides UNC students with an accessible opportunity to serve the community, share their creative enabling technology ideas, and make an impact on the lives of others. Composed of all kinds of students from UNC, the Enabling Technology Club will be an organization for ANYONE who has a desire to help people with disabilities. The club will not limit its membership to just computer science students, as it needs artistic students as well as students who simply support the cause to work on club activities. Additionally, the organization will allow students to learn about the numerous different parts of computer programs and how their work will contribute on a large scale across the globe.",
    website="https://enablingtechnologyclub.web.unc.edu/",
    email="kavishg@live.unc.edu",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/enablingtechnologyclub",
    public=False,
)

esports = OrganizationEntity(
    id=9,
    name="ESports",
    shorthand="ESports",
    slug="esports",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/esports.png",
    short_description="Our goal is to provide a positive and welcoming environment for everyone to pursue their interests in video-game culture. Whether that interest is in content creation, casting, game development, playing video games, getting into competitive esports, or simply watching video games, we are here to ensure that everyone has the space and resources to do so.",
    long_description="Our goal is to provide a positive and welcoming environment for everyone to pursue their interests in video-game culture. Whether that interest is in content creation, casting, game development, playing video games, getting into competitive esports, or simply watching video games, we are here to ensure that everyone has the space and resources to do so.\n\nUsing our access to the Carolina Gaming Arena, we can ensure that you will have the opportunity and resources to play and compete in your favorite games with peak performance.\nWe have members who play and discuss, though not limited to, the following games:\n\\- League of Legends\n\\- DotA 2\n\\- Rocket League\n\\- Overwatch\n\\- Counter-Strike: Global Offensive\n\\- Valorant\n\\-Â Rainbow Six Siege\n\\-Â Smash Ultimate\n\\-Â Super Smash Bros. Melee\n\\- Minecraft\n\\- PokÃ©mon\n\\- World of Warcraft\n\\- Hearthstone\n\\- Beat Saber\n\\- Many more!\nWe also have competitive teams and players who compete in collegiate leagues for the following games:\n\\- League of Legends (3+ teams)\n\\- DotA 2\n\\- Rocket League (2+ teams)\n\\- Overwatch\n\\- Counter Strike - Global Offensive (2 teams)\n\\- Valorant\n\\-Â Rainbow Six Siege\n\\-Â Smash Ultimate\n\\-Â Super Smash Bros. Melee\n\\- We also have casters and content producers for our content creation outlets.\n\nWe also play casually a multitude of other games!\nJoin the club, post on our wall, come to our events, meet people, and most importantly...\nHAVE FUN!",
    website="https://carolinagaming.unc.edu/teams/",
    email="",
    instagram="https://www.instagram.com/carolinaesports/",
    linked_in="",
    youtube="https://www.youtube.com/carolinaesports",
    heel_life="https://heellife.unc.edu/organization/esports",
    public=False,
)

gamedev = OrganizationEntity(
    id=10,
    name="Game Development Club",
    shorthand="Game Dev",
    slug="game-dev",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/gamedev.jpg",
    short_description="A community for anyone interested in learning how to develop video games for all experience levels.",
    long_description="The mission of UNC-CH Game Development Club is to provide a space for anyone interested in learning how to develop video games, whether they have no experience in it whatsoever or are already seasoned game developers. The club is open to anyone that can contribute in the video game development process whether they are interested in programming, 3D modeling, character design, storyboarding, music, creative writing, or any other related creative processes.\nÂ \nThe club also seeks to encourage students not studying computer science to join because game development requires more than just programmers to create a game. Game development is most often associated with computer programming, but it actually requires a much more diverse group of individuals skilled in different creative disciplines. UNC-CH Game Development Club seeks to foster this type of environment and be open to anyone that wishes to learn about this collective creative process.",
    website="",
    email="uncgamedev@gmail.com",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/uncgamedev",
    public=False,
)

gwc = OrganizationEntity(
    id=11,
    name="Girls Who Code",
    shorthand="GWC",
    slug="gwc",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/gwc.png",
    short_description="Debugging the gender gap by providing opportunities to expose middle and high school girls to computer science at an earlier age.",
    long_description="Girls Who Code is a non-profit organization which aims to support and increase the number of women in computer science. The UNC Girls Who Code club aims to get middle- and high-school girls involved in and excited about technology. Any middle- or high-school girl can participate. UNC Computer Science undergraduate and graduate students can apply to become volunteers.",
    website="https://girlswhocode.web.unc.edu/",
    email="carolinawics@gmail.com",
    instagram="https://www.instagram.com/gwc_unc/",
    linked_in="",
    youtube="",
    heel_life="",
    public=False,
)

hacknc = OrganizationEntity(
    id=12,
    name="HackNC",
    shorthand="HackNC",
    slug="hacknc",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/hacknc.jpg",
    short_description="Organizes UNC's annual co-ed inclusive, beginner-friendly hackathon.",
    long_description="HackNC is a weekend for students of all skill levels to broaden their talents. Your challenge is to make an awesome project in just 24 hours. You will have access to hands-on workshops and demos from our sponsors, as well as exciting talks about the awesome things happening right now with computer science and technology - not to mention all of the free food, shirts, stickers, and swag!",
    website="https://hacknc.com/",
    email="hacknsea@gmail.com",
    instagram="",
    linked_in="",
    youtube="https://www.youtube.com/channel/UCDRN6TMC27uSDsZosIwUrZg",
    heel_life="https://heellife.unc.edu/organization/hacknc",
    public=False,
)

ktp = OrganizationEntity(
    id=13,
    name="Kappa Theta Pi",
    shorthand="KTP",
    slug="ktp",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/ktp.jpg",
    short_description="Technology-focused, co-ed professional fraternity.",
    long_description="Kappa Theta Pi is UNC's first professional technology-focused co-ed fraternity. The purpose of this organization is to provide a close-knit community for STEM students to develop socially, professionally, and academically through various events. We will host events including socials, hackathons, alumni networking events, professional development workshops, and tech-based community service. Our members will learn a plethora of skills needed to stay knowledgeable about the tech industry, form a valuable network of brothers, give back to the community via philanthropy, and develop a strong sense of professional development for future job positions.",
    website="http://ktp.cs.unc.edu/",
    email="uncktp@gmail.com",
    instagram="https://www.instagram.com/ktpunc/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/uncktp",
    public=False,
)

pearlhacks = OrganizationEntity(
    id=14,
    name="Pearl Hacks",
    shorthand="Pearl Hacks",
    slug="pearl-hacks",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pearlhacks.jpg",
    short_description="Hackathon for women and nonbinary students catering to first-time hackers looking for a supportive environment to explore technology.",
    long_description="Pearl Hacks strives to empower women and non-binary groups in the field of computer science. We encourage our participants to learn and innovate using their coding skills, and we welcome first-time hackers by creating a collaborative environment for them to learn new skills. Additionally, we welcome a diverse group of minorities and remind them that they are amazing and needed in a field stereotypically dominated by men.",
    website="http://pearlhacks.com/",
    email="pearlhacksunc@gmail.com",
    instagram="https://www.instagram.com/pearlhacks/",
    linked_in="https://www.linkedin.com/company/pearl-hacks/mycompany/",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/pearlhacks",
    public=False,
)

pm = OrganizationEntity(
    id=15,
    name="Product Management Club",
    shorthand="PM Club",
    slug="pm-club",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/pm.jpg",
    short_description="We partner with local tech startups and develop features for their products.",
    long_description="",
    website="https://uncpmclub.com/",
    email="",
    instagram="https://www.linkedin.com/company/unc-product-management-club/",
    linked_in="",
    youtube="",
    heel_life="",
    public=False,
)

queerhack = OrganizationEntity(
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
)

wics = OrganizationEntity(
    id=17,
    name="Women in Computer Science",
    shorthand="WICS",
    slug="wics",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/wics.png",
    short_description="Social, professional, and academic organization to empower and enable women in computer science.",
    long_description="The Women in Computer Science club at UNC Chapel Hill (WiCS) is a social, professional, and academic organization to empower and enable women in computer science. We host a variety of events throughout the year aimed at bringing together the women in tech here on campus and supporting them through mentorship, informative talks, and networking events. We frequently team up with the other organizations in the Computer Science department dedicated to eradicating the gender gap for co-hosted events and coordinate with Girls Who Code and PearlHacks each year.",
    website="",
    email="wins@unc.edu",
    instagram="https://www.instagram.com/uncwics/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/wins",
    public=False,
)

organizations = [
    appteam,
    acm,
    bit,
    cads,
    carvr,
    cssg,
    ctf,
    enablingtech,
    esports,
    gamedev,
    gwc,
    hacknc,
    ktp,
    pearlhacks,
    pm,
    queerhack,
    wics,
]

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global organizations

    # Create entities for test organization data
    entities = []
    for organization in organizations:
        entity = OrganizationEntity.from_model(organization)
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
