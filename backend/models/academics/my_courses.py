from pydantic import BaseModel
from datetime import datetime
from ...models import Paginated
from ...models.office_hours.ticket_state import TicketState
from ...models.office_hours.ticket_type import TicketType


class TeachingSectionOverview(BaseModel):
    id: int
    subject_code: str
    course_number: str
    section_number: str
    title: str


class SectionOverview(BaseModel):
    id: int
    number: str
    meeting_pattern: str
    course_site_id: int | None


class CourseOverview(BaseModel):
    id: str
    subject_code: str
    number: str
    title: str
    sections: list[SectionOverview]
    role: str


class CourseSiteOverview(BaseModel):
    id: int
    subject_code: str
    number: str
    title: str
    role: str
    sections: list[SectionOverview]


class TermOverview(BaseModel):
    id: str
    name: str
    start: datetime
    end: datetime
    sites: list[CourseSiteOverview]
    teaching_no_site: list[TeachingSectionOverview]


class CourseMemberOverview(BaseModel):
    pid: int
    first_name: str
    last_name: str
    email: str
    pronouns: str
    section_number: str
    role: str


class OfficeHoursOverview(BaseModel):
    id: int
    type: str
    mode: str
    description: str
    location: str
    location_description: str
    start_time: datetime
    end_time: datetime
    queued: int
    total_tickets: int


class OfficeHourTicketOverview(BaseModel):
    id: int
    created_at: datetime
    called_at: datetime | None
    state: str
    type: str
    description: str
    creators: list[str]
    caller: str | None


class OfficeHourQueueOverview(BaseModel):
    id: int
    type: str
    start_time: datetime
    end_time: datetime
    active: OfficeHourTicketOverview | None
    other_called: list[OfficeHourTicketOverview]
    queue: list[OfficeHourTicketOverview]


class OfficeHourEventRoleOverview(BaseModel):
    role: str


class OfficeHourGetHelpOverview(BaseModel):
    event_type: str
    event_mode: str
    event_start_time: datetime
    event_end_time: datetime
    ticket: OfficeHourTicketOverview | None
    queue_position: int
