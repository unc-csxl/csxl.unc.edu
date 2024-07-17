from pydantic import BaseModel
from enum import Enum

from ...application import Comp227
from ...public_user import PublicUser

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationReviewStatus(Enum):
    NOT_PREFERRED = "Not Preferred"
    NOT_PROCESSED = "Not Processed"
    PREFERRED = "Preferred"


class ApplicationReview(BaseModel):
    """
    Pydantic model to represent an `ApplicationReview`.

    This model is based on the `ApplicationReviewEntity`.
    """

    id: int | None = None
    application_id: int
    course_site_id: int
    status: ApplicationReviewStatus = ApplicationReviewStatus.NOT_PROCESSED
    preference: int
    notes: str


class ApplicationOverview(BaseModel):
    """
    Pydantic model to represent an `Application`.

    This model is based on the `ApplicationEntity` model, which defines the shape
    of the `Application` database in the PostgreSQL database.
    """

    applicant_name: str
    academic_hours: int | None
    extracurriculars: str | None
    expected_graduation: str | None
    program_pursued: str | None
    other_programs: str | None
    gpa: float | None | None
    comp_gpa: float | None
    comp_227: Comp227 | None
    intro_video_url: str | None
    prior_experience: str | None
    service_experience: str | None
    additional_experience: str | None


class ApplicationReviewOverview(ApplicationReview):
    id: int | None = None
    application_id: int
    application: ApplicationOverview
    status: ApplicationReviewStatus = ApplicationReviewStatus.NOT_PROCESSED
    preference: int
    notes: str
    applicant_course_ranking: int


class HiringStatus(BaseModel):
    not_preferred: list[ApplicationReviewOverview]
    not_processed: list[ApplicationReviewOverview]
    preferred: list[ApplicationReviewOverview]
