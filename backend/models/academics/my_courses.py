from pydantic import BaseModel
from datetime import datetime

from ...models.office_hours.ticket_tag import OfficeHoursTicketTag
from ...models.public_user import PublicUser


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
    subject_code: str
    course_number: str
    section_number: str


class CourseOverview(BaseModel):
    id: str
    subject_code: str
    number: str
    title: str
    sections: list[SectionOverview]
    role: str


class CourseSiteOverview(BaseModel):
    id: int
    term_id: str
    subject_code: str
    number: str
    title: str
    role: str
    sections: list[SectionOverview]
    gtas: list[PublicUser]
    utas: list[PublicUser]


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
    recurrence_pattern_id: int | None


class OfficeHourTicketOverview(BaseModel):
    id: int
    created_at: datetime
    called_at: datetime | None
    closed_at: datetime | None
    state: str
    type: str
    description: str
    creators: list[PublicUser]
    caller: PublicUser | None
    has_concerns: bool | None
    caller_notes: str | None
    tags: list[OfficeHoursTicketTag]


class OfficeHourStatisticsOverview(BaseModel):
    # add more
    average_minutes: int
    total_tickets_called: int
    history: list[OfficeHourTicketOverview]


class OfficeHourQueueOverview(BaseModel):
    id: int
    type: str
    start_time: datetime
    end_time: datetime
    active: OfficeHourTicketOverview | None
    other_called: list[OfficeHourTicketOverview]
    queue: list[OfficeHourTicketOverview]
    personal_tickets_called: int
    average_minutes: int
    total_tickets_called: int
    history: list[OfficeHourTicketOverview]


class OfficeHourEventRoleOverview(BaseModel):
    role: str


class OfficeHourGetHelpOverview(BaseModel):
    event_type: str
    event_mode: str
    event_start_time: datetime
    event_end_time: datetime
    event_location: str
    event_location_description: str
    ticket: OfficeHourTicketOverview | None
    queue_position: int
