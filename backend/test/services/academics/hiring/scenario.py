"""Explicit arrange helpers for hiring service tests."""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from .....entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)
from .....entities.academics.hiring.hiring_assignment_entity import (
    HiringAssignmentEntity,
)
from .....entities.academics.hiring.hiring_level_entity import HiringLevelEntity
from .....entities.application_entity import ApplicationEntity
from .....entities.section_application_table import section_application_table
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
from ...reset_table_id_seq import reset_table_id_seq
from ..course_site_scenario import CourseSiteScenario, arrange_course_site_scenario


@dataclass
class HiringScenario:
    course_site: CourseSiteScenario
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


def arrange_hiring_scenario(session: Session) -> HiringScenario:
    course_site = arrange_course_site_scenario(session)
    auth = course_site.academics.auth
    current_term = course_site.academics.current_term
    now = datetime.now().replace(microsecond=0)

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
    session.add_all(ApplicationEntity.from_model(application) for application in applications)
    reset_table_id_seq(session, ApplicationEntity, ApplicationEntity.id, 6)
    session.flush()

    for application_id, section_id, preference in [
        (application_one.id, course_site.academics.comp_301_001_current_term.id, 0),
        (application_one.id, course_site.academics.comp_110_001_current_term.id, 1),
        (application_one.id, course_site.academics.comp_110_002_current_term.id, 2),
        (application_two.id, course_site.academics.comp_110_001_current_term.id, 0),
        (application_three.id, course_site.academics.comp_110_001_current_term.id, 0),
        (application_four.id, course_site.academics.comp_110_001_current_term.id, 0),
        (application_five.id, course_site.academics.comp_301_001_current_term.id, 0),
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