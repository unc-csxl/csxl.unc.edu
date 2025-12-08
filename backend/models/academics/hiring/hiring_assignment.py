from pydantic import BaseModel
from enum import Enum
from datetime import datetime

from ... import PublicUser
from ... import User
from ...academics import CatalogSectionIdentity
from .hiring_level import HiringLevel
from .application_review import ApplicationReviewOverview

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringAssignmentStatus(Enum):
    DRAFT = "Draft"
    COMMIT = "Commit"
    FINAL = "Final"


class HiringAssignmentDraft(BaseModel):
    id: int | None = None
    user_id: int
    term_id: str
    course_site_id: int
    application_review_id: int | None = None
    level: HiringLevel
    status: HiringAssignmentStatus
    position_number: str
    epar: str
    i9: bool
    notes: str
    created: datetime
    modified: datetime


class HiringAssignmentOverview(BaseModel):
    id: int | None = None
    user: PublicUser
    level: HiringLevel
    status: HiringAssignmentStatus
    position_number: str
    epar: str
    i9: bool
    notes: str


class HiringAssignmentSummaryOverview(BaseModel):
    """Model specific for the summary page."""

    id: int | None = None
    application_review_id: int | None = None
    course_site_id: int | None = None
    course: str | None = None
    user: User
    instructors: str
    level: HiringLevel
    status: HiringAssignmentStatus
    position_number: str
    epar: str
    i9: bool
    notes: str


class HiringAssignmentCsvRow(BaseModel):
    """Model specific for the CSV export."""

    first_name: str
    last_name: str
    onyen: str
    pid: str
    email: str
    instructors: str
    epar: str
    position_number: str
    i9: bool
    notes: str
    status: HiringAssignmentStatus
    level_title: str
    level_load: str
    level_salary: str


class HiringAssignmentSummaryCsvRow(BaseModel):
    """Used in the instructor summary CSV export."""

    first_name: str
    last_name: str
    onyen: str
    pid: str
    email: str
    level_title: str


class HiringCourseSiteOverview(BaseModel):
    course_site_id: int
    sections: list[CatalogSectionIdentity]
    instructors: list[PublicUser]
    total_enrollment: int
    total_cost: float
    coverage: float
    assignments: list[HiringAssignmentOverview]


class HiringAdminOverview(BaseModel):
    sites: list[HiringCourseSiteOverview]


class HiringAdminCourseOverview(BaseModel):
    assignments: list[HiringAssignmentOverview]
    reviews: list[ApplicationReviewOverview]
    instructor_preferences: list[PublicUser]
