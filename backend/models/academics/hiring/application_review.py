from pydantic import BaseModel
from enum import Enum

from ...application import Comp227, ApplicationUnderReview
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


class ApplicationReviewOverview(ApplicationReview):
    id: int | None = None
    application_id: int
    application: ApplicationUnderReview
    applicant_id: int
    status: ApplicationReviewStatus = ApplicationReviewStatus.NOT_PROCESSED
    preference: int
    notes: str
    applicant_course_ranking: int


class HiringStatus(BaseModel):
    not_preferred: list[ApplicationReviewOverview]
    not_processed: list[ApplicationReviewOverview]
    preferred: list[ApplicationReviewOverview]
