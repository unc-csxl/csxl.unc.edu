from pydantic import BaseModel
from enum import Enum
from datetime import datetime

from ... import PublicUser
from ...academics import CatalogSectionIdentity
from .hiring_level import HiringLevel

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class HiringAssignmentStatus(Enum):
    DRAFT = "Draft"
    COMMIT = "Commit"
    FINAL = "Final"


class HiringAssignmentOverview(BaseModel):
    id: int | None
    user: PublicUser
    level: HiringLevel
    status: HiringAssignmentStatus
    position_number: str
    epar: str
    i9: bool
    notes: str
    created: datetime
    modified: datetime


class HiringCourseSiteOverview(BaseModel):
    course_site_id: int
    sections: list[CatalogSectionIdentity]
    instructors: list[PublicUser]
    total_enrollment: int
    total_cost: float
    coverage: float
    assignments: list[HiringAssignmentOverview]
    instructor_preferences: list[PublicUser]


class HiringAdminOverview(BaseModel):
    sites: list[HiringCourseSiteOverview]
