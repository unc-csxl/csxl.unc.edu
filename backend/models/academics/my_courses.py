from pydantic import BaseModel
from datetime import datetime


class SectionOverview(BaseModel):
    id: int
    meeting_pattern: str
    override_title: str
    override_description: str


class CourseOverview(BaseModel):
    id: str
    subject_code: str
    number: str
    title: str
    description: str
    sections: list[SectionOverview]


class MyCourseItem(BaseModel):
    course: CourseOverview
    role: str


class TermOverview(BaseModel):
    id: str
    name: str
    start: datetime
    end: datetime
    courses: list[MyCourseItem]


class MyCourseTerms(BaseModel):
    terms: dict[str, TermOverview]
