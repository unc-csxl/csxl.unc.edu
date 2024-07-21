import pytest
from sqlalchemy.orm import Session
from ....services.reset_table_id_seq import reset_table_id_seq

from .....entities.application_entity import ApplicationEntity
from .....entities.section_application_table import section_application_table
from .....entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)

from .....models.application import Comp227, Application, CatalogSectionIdentity
from .....models.academics.hiring.application_review import (
    ApplicationReview,
    ApplicationReviewStatus,
)

from ... import user_data
from ...academics import section_data, term_data
from ...office_hours import office_hours_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

application_one = Application(
    id=1,
    type="new_uta",
    user_id=user_data.student.id,
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
    term_id=term_data.current_term.id,
)

application_two = Application(
    id=2,
    type="new_uta",
    user_id=user_data.user.id,
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
    term_id=term_data.current_term.id,
)

application_three = Application(
    id=3,
    type="new_uta",
    user_id=user_data.root.id,
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
    term_id=term_data.current_term.id,
)

application_four = Application(
    id=4,
    type="new_uta",
    user_id=user_data.uta.id,
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
    term_id=term_data.current_term.id,
)

new_application = Application(
    id=5,
    type="new_uta",
    user_id=user_data.ambassador.id,
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
        CatalogSectionIdentity(
            id=section_data.comp_110_001_current_term.id,
            subject_code="COMP",
            course_number="110",
            section_number="001",
            course_title="Intro to Programming",
        ),
        CatalogSectionIdentity(
            id=section_data.comp_110_002_current_term.id,
            subject_code="COMP",
            course_number="110",
            section_number="002",
            course_title="Intro to Programming",
        ),
    ],
    term_id=term_data.current_term.id,
)


applications = [application_one, application_two, application_three, application_four]

application_associations = [
    (application_one, section_data.comp_301_001_current_term, 0),
    (application_one, section_data.comp_110_001_current_term, 1),
    (application_one, section_data.comp_110_002_current_term, 2),
    (application_two, section_data.comp_110_001_current_term, 0),
    (application_three, section_data.comp_110_001_current_term, 0),
    (application_four, section_data.comp_110_001_current_term, 0),
]

review_one = ApplicationReview(
    application_id=application_one.id,
    course_site_id=office_hours_data.comp_110_site.id,
    status=ApplicationReviewStatus.NOT_PREFERRED,
    preference=0,
    notes="",
)

review_two = ApplicationReview(
    application_id=application_two.id,
    course_site_id=office_hours_data.comp_110_site.id,
    status=ApplicationReviewStatus.PREFERRED,
    preference=0,
    notes="",
)

review_three = ApplicationReview(
    application_id=application_three.id,
    course_site_id=office_hours_data.comp_110_site.id,
    status=ApplicationReviewStatus.NOT_PROCESSED,
    preference=0,
    notes="",
)

reviews = [review_one, review_two, review_three]


def insert_fake_data(session: Session):
    for application in applications:
        entity = ApplicationEntity.from_model(application)
        session.add(entity)

    reset_table_id_seq(
        session,
        ApplicationEntity,
        ApplicationEntity.id,
        len(applications) + 1,
    )

    session.commit()

    for application, section, preference in application_associations:
        session.execute(
            section_application_table.insert().values(
                {
                    "section_id": section.id,
                    "application_id": application.id,
                    "preference": preference,
                }
            )
        )
        session.commit()

    for review in reviews:
        entity = ApplicationReviewEntity.from_model(review)
        session.add(entity)

    reset_table_id_seq(
        session,
        ApplicationReviewEntity,
        ApplicationReviewEntity.id,
        len(reviews) + 1,
    )

    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
