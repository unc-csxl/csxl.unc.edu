from pydantic import BaseModel
from datetime import datetime


class SectionOverview(BaseModel):
    number: str
    meeting_pattern: str
    oh_section_id: int | None


class CourseOverview(BaseModel):
    id: str
    subject_code: str
    number: str
    title: str
    sections: list[SectionOverview]
    role: str


class TermOverview(BaseModel):
    id: str
    name: str
    start: datetime
    end: datetime
    courses: list[CourseOverview]


class CourseMemberOverview(BaseModel):
    pid: int
    first_name: str
    last_name: str
    email: str
    pronouns: str
    role: str


class CourseRosterOverview(BaseModel):
    id: str
    subject_code: str
    number: str
    title: str
    members: list[CourseMemberOverview]
