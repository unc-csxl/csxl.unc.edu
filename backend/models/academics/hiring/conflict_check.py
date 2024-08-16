from pydantic import BaseModel

from .hiring_assignment import HiringAssignmentSummaryOverview

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationPriority(BaseModel):
    """
    When checking for conflicts for an application desired by multiple parties,
    this model indicates a single class' ranking for both student and instructor.
    """

    student_priority: int
    instructor_priority: int
    course_site_id: int
    course_title: str


class ConflictCheck(BaseModel):
    """
    Model that embeds potential for conflicts when making assignments.
    """

    application_id: int
    assignments: list[HiringAssignmentSummaryOverview]
    priorities: list[ApplicationPriority]
