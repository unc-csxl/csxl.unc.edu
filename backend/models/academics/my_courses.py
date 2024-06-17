from pydantic import BaseModel
from datetime import datetime
from ...models import Paginated
from ...models.office_hours.ticket_state import TicketState
from ...models.office_hours.ticket_type import TicketType


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
