from pydantic import BaseModel
from datetime import datetime


class CourseOverview(BaseModel):
    id: str
    subject_code: str
    number: str
    title: str
    description: str


class SectionOverview(BaseModel):
    id: int
    course: CourseOverview
    number: str
    meeting_pattern: str
    override_title: str
    override_description: str


class MyCourseItem(BaseModel):
    section: SectionOverview
    role: str


class TermOverview(BaseModel):
    id: str
    name: str
    start: datetime
    end: datetime
    courses: list[MyCourseItem]


class MyCourseTerms(BaseModel):
    terms: dict[str, TermOverview]
