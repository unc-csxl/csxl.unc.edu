"""Definition for a COMP 423 project for showcasing."""

from pydantic import BaseModel
from enum import Enum

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ProjectType(Enum):
    NEWS_FEED = "XL News Feed / Announcements"
    STUDENT_ORGS = "Student Organization Memberships / Members-only Features"
    SEATING = "Interactive Seating Chart / Map Widget"
    XL_DISPLAY = "XL Digital Display System"
    OTHER = "Other"


class ShowcaseProject(BaseModel):
    team_name: str
    type: ProjectType
    members: list[str]
