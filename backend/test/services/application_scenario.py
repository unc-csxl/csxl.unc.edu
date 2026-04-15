"""Explicit arrange helpers for application service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ...entities.academics.course_entity import CourseEntity
from ...entities.academics.section_entity import SectionEntity
from ...entities.academics.term_entity import TermEntity
from ...entities.application_entity import ApplicationEntity
from ...entities.section_application_table import section_application_table
from ...models.academics.course import Course
from ...models.academics.section import CatalogSectionIdentity, Section
from ...models.academics.term import Term
from ...models.application import Application
from ...models.comp_227 import Comp227
from .auth_scenario import AuthScenario, arrange_auth_scenario
from .reset_table_id_seq import reset_table_id_seq


@dataclass
class ApplicationScenario:
    auth: AuthScenario
    current_term: Term
    comp_110_001_current_term: Section
    comp_110_002_current_term: Section
    application_one: Application
    new_application: Application


def _section_identity(section: Section, course: Course) -> CatalogSectionIdentity:
    return CatalogSectionIdentity(
        id=section.id,
        subject_code=course.subject_code,
        course_number=course.number,
        section_number=section.number,
        title=course.title,
    )


def arrange_application_scenario(session: Session) -> ApplicationScenario:
    auth = arrange_auth_scenario(session)

    now = datetime.now().replace(microsecond=0)
    term_length = timedelta(weeks=17)
    current_term = Term(
        id="Curr",
        name="Current Term",
        start=now,
        end=now + term_length,
        applications_open=now - timedelta(days=1),
        applications_close=now + term_length,
    )

    courses = {
        "comp110": Course(
            id="comp110",
            subject_code="COMP",
            number="110",
            title="Introduction to Programming and Data Science",
            description="Introduces students to programming and data science.",
            credit_hours=3,
        ),
        "comp210": Course(
            id="comp210",
            subject_code="COMP",
            number="210",
            title="Data Structures and Analysis",
            description="Data structures and analysis.",
            credit_hours=3,
        ),
        "comp211": Course(
            id="comp211",
            subject_code="COMP",
            number="211",
            title="Systems Fundamentals",
            description="Systems fundamentals.",
            credit_hours=3,
        ),
        "comp301": Course(
            id="comp301",
            subject_code="COMP",
            number="301",
            title="Foundations of Programming",
            description="Foundations of programming.",
            credit_hours=3,
        ),
        "comp311": Course(
            id="comp311",
            subject_code="COMP",
            number="311",
            title="Computer Organization",
            description="Computer organization.",
            credit_hours=3,
        ),
        "comp523": Course(
            id="comp523",
            subject_code="COMP",
            number="523",
            title="Software Engineering Laboratory",
            description="Software engineering laboratory.",
            credit_hours=4,
        ),
    }
    sections = {
        "comp523_001": Section(
            id=9,
            course_id="comp523",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 2:00PM - 3:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp210_001": Section(
            id=10,
            course_id="comp210",
            number="001",
            term_id=current_term.id,
            meeting_pattern="TTh 9:00AM - 10:15AM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
        "comp110_001": Section(
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
        "comp110_002": Section(
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
        "comp301_001": Section(
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
        "comp301_002": Section(
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
        "comp311_001": Section(
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
        "comp311_002": Section(
            id=16,
            course_id="comp311",
            number="002",
            term_id=current_term.id,
            meeting_pattern="TTh 5:00PM - 6:15PM",
            override_title="",
            override_description="",
            enrolled=100,
            total_seats=200,
        ),
    }

    session.add(TermEntity.from_model(current_term))
    session.add_all(CourseEntity.from_model(course) for course in courses.values())
    session.add_all(SectionEntity.from_model(section) for section in sections.values())
    reset_table_id_seq(session, SectionEntity, SectionEntity.id, 17)

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
    applications = [
        application_one,
        Application(
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
        ),
        Application(
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
        ),
        Application(
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
        ),
        Application(
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
        ),
    ]

    session.add_all(
        ApplicationEntity.from_model(application) for application in applications
    )
    reset_table_id_seq(session, ApplicationEntity, ApplicationEntity.id, 6)
    session.flush()

    application_associations = [
        (1, sections["comp301_001"].id, 0),
        (1, sections["comp110_001"].id, 1),
        (1, sections["comp110_002"].id, 2),
        (2, sections["comp110_001"].id, 0),
        (3, sections["comp110_001"].id, 0),
        (4, sections["comp110_001"].id, 0),
        (5, sections["comp301_001"].id, 0),
    ]
    for application_id, section_id, preference in application_associations:
        session.execute(
            section_application_table.insert().values(
                {
                    "section_id": section_id,
                    "application_id": application_id,
                    "preference": preference,
                }
            )
        )

    session.commit()

    new_application = Application(
        id=6,
        type="new_uta",
        user_id=auth.ambassador.id,
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
        preferred_sections=[
            _section_identity(sections["comp110_001"], courses["comp110"]),
            _section_identity(sections["comp110_002"], courses["comp110"]),
        ],
        term_id=current_term.id,
    )

    return ApplicationScenario(
        auth=auth,
        current_term=current_term,
        comp_110_001_current_term=sections["comp110_001"],
        comp_110_002_current_term=sections["comp110_002"],
        application_one=application_one,
        new_application=new_application,
    )
