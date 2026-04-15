"""Explicit arrange helpers for hiring service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .....entities.academics.course_entity import CourseEntity
from .....entities.academics.section_entity import SectionEntity
from .....entities.academics.section_member_entity import SectionMemberEntity
from .....entities.academics.term_entity import TermEntity
from .....entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)
from .....entities.academics.hiring.hiring_assignment_entity import (
    HiringAssignmentEntity,
)
from .....entities.academics.hiring.hiring_level_entity import HiringLevelEntity
from .....entities.application_entity import ApplicationEntity
from .....entities.office_hours.course_site_entity import CourseSiteEntity
from .....entities.permission_entity import PermissionEntity
from .....entities.role_entity import RoleEntity
from .....entities.section_application_table import section_application_table
from .....entities.user_entity import UserEntity
from .....entities.user_role_table import user_role_table
from .....models import Permission, Role
from .....models.academics.course import Course
from .....models.academics.section import Section
from .....models.academics.section_member import SectionMemberDraft
from .....models.academics.term import Term
from .....models.academics.hiring.application_review import (
    ApplicationReview,
    ApplicationReviewStatus,
)
from .....models.academics.hiring.hiring_assignment import (
    HiringAssignmentDraft,
    HiringAssignmentStatus,
)
from .....models.academics.hiring.hiring_level import (
    HiringLevel,
    HiringLevelClassification,
)
from .....models.application import Application
from .....models.comp_227 import Comp227
from .....models.office_hours.course_site import CourseSite
from .....models.roster_role import RosterRole
from .....models.user import User
from ...reset_table_id_seq import reset_table_id_seq


@dataclass(frozen=True)
class HiringAuthScenario:
    root_role: Role
    root_permission: Permission
    root: User
    ambassador: User
    user: User
    instructor: User
    uta: User
    student: User


@dataclass(frozen=True)
class HiringAcademicsScenario:
    auth: HiringAuthScenario
    current_term: Term
    comp_110_001_current_term: Section
    comp_110_002_current_term: Section
    comp_301_001_current_term: Section
    comp_301_002_current_term: Section
    comp_311_001_current_term: Section


@dataclass(frozen=True)
class HiringCourseSiteScenario:
    academics: HiringAcademicsScenario
    comp_110_site: CourseSite
    comp_301_site: CourseSite


@dataclass
class HiringScenario:
    course_site: HiringCourseSiteScenario
    application_one: Application
    application_two: Application
    application_three: Application
    application_four: Application
    application_five: Application
    uta_level: HiringLevel
    updated_uta_level: HiringLevel
    new_level: HiringLevel
    hiring_assignment: HiringAssignmentDraft
    updated_hiring_assignment: HiringAssignmentDraft
    new_hiring_assignment: HiringAssignmentDraft


def build_hiring_auth_scenario() -> HiringAuthScenario:
    return HiringAuthScenario(
        root_role=Role(id=1, name="root"),
        root_permission=Permission(id=1, action="*", resource="*"),
        root=User(
            id=1,
            pid=999999999,
            onyen="root",
            email="root@unc.edu",
            first_name="Rhonda",
            last_name="Root",
            pronouns="She / Her / Hers",
            accepted_community_agreement=True,
        ),
        ambassador=User(
            id=2,
            pid=888888888,
            onyen="xlstan",
            email="amam@unc.edu",
            first_name="Amy",
            last_name="Ambassador",
            pronouns="They / Them / Theirs",
            accepted_community_agreement=True,
        ),
        user=User(
            id=3,
            pid=111111111,
            onyen="user",
            email="user@unc.edu",
            first_name="Sally",
            last_name="Student",
            pronouns="She / They",
            accepted_community_agreement=True,
        ),
        instructor=User(
            id=4,
            pid=222222222,
            onyen="Ina",
            email="ina@unc.edu",
            first_name="Ina",
            last_name="Instructor",
            pronouns="They / Them / Theirs",
        ),
        uta=User(
            id=5,
            pid=333333333,
            onyen="uhlissa",
            email="uhlissa@unc.edu",
            first_name="Uhlissa",
            last_name="UTA",
            pronouns="They / Them / Theirs",
        ),
        student=User(
            id=6,
            pid=555555555,
            onyen="Stewie",
            email="stewie@unc.edu",
            first_name="Stewie",
            last_name="Student",
            pronouns="They / Them / Theirs",
        ),
    )


def arrange_hiring_scenario(session: Session) -> HiringScenario:
    auth = build_hiring_auth_scenario()
    now = datetime.now().replace(microsecond=0)
    current_term = Term(
        id="Curr",
        name="Current Term",
        start=now,
        end=now + timedelta(weeks=17),
        applications_open=now,
        applications_close=now + timedelta(weeks=17),
    )

    courses = [
        Course(
            id="comp110",
            subject_code="COMP",
            number="110",
            title="Introduction to Programming and Data Science",
            description="Introduces students to programming and data science.",
            credit_hours=3,
        ),
        Course(
            id="comp301",
            subject_code="COMP",
            number="301",
            title="Foundations of Programming",
            description="Foundations of programming.",
            credit_hours=3,
        ),
        Course(
            id="comp311",
            subject_code="COMP",
            number="311",
            title="Computer Organization",
            description="Computer organization.",
            credit_hours=3,
        ),
    ]
    sections = {
        "comp_110_001_current_term": Section(
            id=11,
            course_id="comp110",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 12:00PM - 1:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_110_002_current_term": Section(
            id=12,
            course_id="comp110",
            number="002",
            term_id=current_term.id,
            meeting_pattern="TTh 1:30PM - 2:45PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_301_001_current_term": Section(
            id=13,
            course_id="comp301",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 8:00AM - 9:15AM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_301_002_current_term": Section(
            id=14,
            course_id="comp301",
            number="002",
            term_id=current_term.id,
            meeting_pattern="TTh 5:00PM - 6:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp_311_001_current_term": Section(
            id=15,
            course_id="comp311",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 5:00PM - 6:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
    }

    session.add(RoleEntity.from_model(auth.root_role))
    session.add_all(
        UserEntity.from_model(user)
        for user in vars(auth).values()
        if isinstance(user, User)
    )
    session.flush()
    session.execute(
        user_role_table.insert().values(
            {"role_id": auth.root_role.id, "user_id": auth.root.id}
        )
    )
    session.add(
        PermissionEntity(
            id=auth.root_permission.id,
            role_id=auth.root_role.id,
            action=auth.root_permission.action,
            resource=auth.root_permission.resource,
        )
    )
    reset_table_id_seq(session, RoleEntity, RoleEntity.id, auth.root_role.id + 1)
    reset_table_id_seq(session, UserEntity, UserEntity.id, auth.student.id + 1)
    reset_table_id_seq(
        session,
        PermissionEntity,
        PermissionEntity.id,
        auth.root_permission.id + 1,
    )

    session.add(TermEntity.from_model(current_term))
    session.add_all(CourseEntity.from_model(course) for course in courses)
    session.add_all(SectionEntity.from_model(section) for section in sections.values())
    session.flush()

    memberships = [
        SectionMemberDraft(
            id=1,
            user_id=auth.instructor.id,
            section_id=sections["comp_110_001_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=2,
            user_id=auth.instructor.id,
            section_id=sections["comp_110_002_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=3,
            user_id=auth.instructor.id,
            section_id=sections["comp_301_001_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=4,
            user_id=auth.instructor.id,
            section_id=sections["comp_301_002_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
        SectionMemberDraft(
            id=5,
            user_id=auth.root.id,
            section_id=sections["comp_311_001_current_term"].id,
            member_role=RosterRole.INSTRUCTOR,
        ),
    ]
    session.add_all(
        SectionMemberEntity.from_draft_model(member) for member in memberships
    )
    reset_table_id_seq(session, SectionMemberEntity, SectionMemberEntity.id, 10)

    comp_110_site = CourseSite(id=1, title="COMP 110", term_id=current_term.id)
    comp_301_site = CourseSite(id=2, title="COMP 301", term_id=current_term.id)
    session.add_all(
        [
            CourseSiteEntity.from_model(comp_110_site),
            CourseSiteEntity.from_model(comp_301_site),
        ]
    )
    session.flush()
    session.get(
        SectionEntity, sections["comp_110_001_current_term"].id
    ).course_site_id = comp_110_site.id
    session.get(
        SectionEntity, sections["comp_110_002_current_term"].id
    ).course_site_id = comp_110_site.id
    session.get(
        SectionEntity, sections["comp_301_001_current_term"].id
    ).course_site_id = comp_301_site.id
    reset_table_id_seq(session, CourseSiteEntity, CourseSiteEntity.id, 3)

    academics = HiringAcademicsScenario(
        auth=auth,
        current_term=current_term,
        comp_110_001_current_term=sections["comp_110_001_current_term"],
        comp_110_002_current_term=sections["comp_110_002_current_term"],
        comp_301_001_current_term=sections["comp_301_001_current_term"],
        comp_301_002_current_term=sections["comp_301_002_current_term"],
        comp_311_001_current_term=sections["comp_311_001_current_term"],
    )
    course_site = HiringCourseSiteScenario(
        academics=academics,
        comp_110_site=comp_110_site,
        comp_301_site=comp_301_site,
    )

    application_one = Application(
        id=1,
        type="new_uta",
        user_id=auth.student.id,
        academic_hours=12,
        extracurriculars="Many extracurriculars",
        expected_graduation="Soon",
        program_pursued="CS",
        other_programs="None",
        gpa=3.8,
        comp_gpa=4.0,
        comp_227=Comp227.EITHER,
        intro_video_url="https://www.youtube.com/watch?v=d6O6kyqjcYo",
        prior_experience="None",
        service_experience="None",
        additional_experience="None",
        preferred_sections=[],
        term_id=current_term.id,
    )
    application_two = Application(
        id=2,
        type="new_uta",
        user_id=auth.user.id,
        academic_hours=12,
        extracurriculars="Many extracurriculars",
        expected_graduation="Soon",
        program_pursued="CS",
        other_programs="None",
        gpa=3.8,
        comp_gpa=4.0,
        comp_227=Comp227.EITHER,
        intro_video_url="https://www.youtube.com/watch?v=d6O6kyqjcYo",
        prior_experience="None",
        service_experience="None",
        additional_experience="None",
        preferred_sections=[],
        term_id=current_term.id,
    )
    application_three = Application(
        id=3,
        type="new_uta",
        user_id=auth.root.id,
        academic_hours=12,
        extracurriculars="Many extracurriculars",
        expected_graduation="Soon",
        program_pursued="CS",
        other_programs="None",
        gpa=3.8,
        comp_gpa=4.0,
        comp_227=Comp227.EITHER,
        intro_video_url="https://www.youtube.com/watch?v=d6O6kyqjcYo",
        prior_experience="None",
        service_experience="None",
        additional_experience="None",
        preferred_sections=[],
        term_id=current_term.id,
    )
    application_four = Application(
        id=4,
        type="new_uta",
        user_id=auth.uta.id,
        academic_hours=12,
        extracurriculars="Many extracurriculars",
        expected_graduation="Soon",
        program_pursued="CS",
        other_programs="None",
        gpa=3.8,
        comp_gpa=4.0,
        comp_227=Comp227.EITHER,
        intro_video_url="https://www.youtube.com/watch?v=d6O6kyqjcYo",
        prior_experience="None",
        service_experience="None",
        additional_experience="None",
        preferred_sections=[],
        term_id=current_term.id,
    )
    application_five = Application(
        id=5,
        type="gta",
        user_id=auth.root.id,
        academic_hours=12,
        extracurriculars="Many extracurriculars",
        expected_graduation="Soon",
        program_pursued="PhD",
        other_programs="None",
        gpa=3.8,
        comp_gpa=4.0,
        comp_227=Comp227.EITHER,
        intro_video_url="https://www.youtube.com/watch?v=d6O6kyqjcYo",
        prior_experience="None",
        service_experience="None",
        additional_experience="None",
        preferred_sections=[],
        term_id=current_term.id,
    )
    applications = [
        application_one,
        application_two,
        application_three,
        application_four,
        application_five,
    ]
    session.add_all(
        ApplicationEntity.from_model(application) for application in applications
    )
    reset_table_id_seq(session, ApplicationEntity, ApplicationEntity.id, 6)
    session.flush()

    for application_id, section_id, preference in [
        (application_one.id, academics.comp_301_001_current_term.id, 0),
        (application_one.id, academics.comp_110_001_current_term.id, 1),
        (application_one.id, academics.comp_110_002_current_term.id, 2),
        (application_two.id, academics.comp_110_001_current_term.id, 0),
        (application_three.id, academics.comp_110_001_current_term.id, 0),
        (application_four.id, academics.comp_110_001_current_term.id, 0),
        (application_five.id, academics.comp_301_001_current_term.id, 0),
    ]:
        session.execute(
            section_application_table.insert().values(
                {
                    "section_id": section_id,
                    "application_id": application_id,
                    "preference": preference,
                }
            )
        )

    reviews = [
        ApplicationReview(
            application_id=application_one.id,
            course_site_id=course_site.comp_110_site.id,
            status=ApplicationReviewStatus.NOT_PREFERRED,
            preference=0,
            notes="",
        ),
        ApplicationReview(
            application_id=application_two.id,
            course_site_id=course_site.comp_110_site.id,
            status=ApplicationReviewStatus.PREFERRED,
            preference=0,
            notes="",
        ),
        ApplicationReview(
            application_id=application_three.id,
            course_site_id=course_site.comp_110_site.id,
            status=ApplicationReviewStatus.NOT_PROCESSED,
            preference=0,
            notes="",
        ),
    ]
    session.add_all(ApplicationReviewEntity.from_model(review) for review in reviews)
    reset_table_id_seq(session, ApplicationReviewEntity, ApplicationReviewEntity.id, 4)

    uta_level = HiringLevel(
        id=1,
        title="UTA Full Time",
        salary=2000.0,
        load=1.0,
        classification=HiringLevelClassification.UG,
        is_active=True,
    )
    updated_uta_level = uta_level.model_copy(update={"is_active": False})
    new_level = HiringLevel(
        id=2,
        title="Lead UTA Full Time",
        salary=3000.0,
        load=1.5,
        classification=HiringLevelClassification.UG,
        is_active=True,
    )
    session.add(HiringLevelEntity.from_model(uta_level))
    reset_table_id_seq(session, HiringLevelEntity, HiringLevelEntity.id, 2)

    hiring_assignment = HiringAssignmentDraft(
        id=1,
        user_id=auth.student.id,
        term_id=current_term.id,
        course_site_id=course_site.comp_110_site.id,
        level=uta_level,
        status=HiringAssignmentStatus.COMMIT,
        position_number="sample",
        epar="12345",
        i9=True,
        notes="Some notes here",
        created=now,
        modified=now,
    )
    updated_hiring_assignment = hiring_assignment.model_copy(
        update={"status": HiringAssignmentStatus.FINAL}
    )
    new_hiring_assignment = HiringAssignmentDraft(
        id=2,
        user_id=auth.ambassador.id,
        term_id=current_term.id,
        course_site_id=course_site.comp_110_site.id,
        level=uta_level,
        status=HiringAssignmentStatus.FINAL,
        position_number="sample",
        epar="54321",
        i9=True,
        notes="Some notes here",
        created=now,
        modified=now,
    )
    session.add(HiringAssignmentEntity.from_draft_model(hiring_assignment))
    reset_table_id_seq(session, HiringAssignmentEntity, HiringAssignmentEntity.id, 2)
    session.commit()

    return HiringScenario(
        course_site=course_site,
        application_one=application_one,
        application_two=application_two,
        application_three=application_three,
        application_four=application_four,
        application_five=application_five,
        uta_level=uta_level,
        updated_uta_level=updated_uta_level,
        new_level=new_level,
        hiring_assignment=hiring_assignment,
        updated_hiring_assignment=updated_hiring_assignment,
        new_hiring_assignment=new_hiring_assignment,
    )
