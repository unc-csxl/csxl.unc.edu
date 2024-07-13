import pytest
from sqlalchemy.orm import Session
from ...services.reset_table_id_seq import reset_table_id_seq

from ....entities.application_entity import NewUTAApplicationEntity, ApplicationEntity
from ....entities.section_application_table import section_application_table
from ....entities.application_review_entity import ApplicationReviewEntity

from ....models.application import Comp227
from ....models.application_details import NewUTAApplicationDetails
from ....models.application_review import ApplicationReview, ApplicationReviewStatus

from .. import user_data
from ..academics import section_data
from ..office_hours import office_hours_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

application_one = NewUTAApplicationDetails(
    id=1,
    user_id=user_data.student.id,
    user=user_data.student,
    academic_hours=12,
    extracurriculars="Many extracurriculars",
    expected_graduation="Soon",
    program_pursued="CS",
    other_programs="None",
    gpa=3.8,
    comp_gpa=4.0,
    comp_227=Comp227.EITHER,
    intro_video_url="video here",
    prior_experience="None",
    service_experience="None",
    additional_experience="None",
    preferred_sections=[],
)

application_two = NewUTAApplicationDetails(
    id=2,
    user_id=user_data.user.id,
    user=user_data.user,
    academic_hours=12,
    extracurriculars="Many extracurriculars",
    expected_graduation="Soon",
    program_pursued="CS",
    other_programs="None",
    gpa=3.8,
    comp_gpa=4.0,
    comp_227=Comp227.EITHER,
    intro_video_url="video here",
    prior_experience="None",
    service_experience="None",
    additional_experience="None",
    preferred_sections=[],
)

application_three = NewUTAApplicationDetails(
    id=3,
    user_id=user_data.root.id,
    user=user_data.root,
    academic_hours=12,
    extracurriculars="Many extracurriculars",
    expected_graduation="Soon",
    program_pursued="CS",
    other_programs="None",
    gpa=3.8,
    comp_gpa=4.0,
    comp_227=Comp227.EITHER,
    intro_video_url="video here",
    prior_experience="None",
    service_experience="None",
    additional_experience="None",
    preferred_sections=[],
)

application_four = NewUTAApplicationDetails(
    id=4,
    user_id=user_data.uta.id,
    user=user_data.uta,
    academic_hours=12,
    extracurriculars="Many extracurriculars",
    expected_graduation="Soon",
    program_pursued="CS",
    other_programs="None",
    gpa=3.8,
    comp_gpa=4.0,
    comp_227=Comp227.EITHER,
    intro_video_url="video here",
    prior_experience="None",
    service_experience="None",
    additional_experience="None",
    preferred_sections=[],
)


applications = [application_one, application_two, application_three, application_four]

application_associations = [
    (application_one, section_data.comp_110_001_current_term, 0),
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
        entity = NewUTAApplicationEntity.from_model(application)
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
