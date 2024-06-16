from pydantic import BaseModel
from datetime import datetime
from ...models import Paginated


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
    section_number: str
    role: str


class CourseOfficeHourEventOverview(BaseModel):
    id: int
    type: str
    mode: str
    description: str
    location_description: str
    start_time: datetime
    end_time: datetime


class CourseOfficeHourEventsOverview(BaseModel):
    current_events: list[CourseOfficeHourEventOverview]
    future_events: list[CourseOfficeHourEventOverview]
