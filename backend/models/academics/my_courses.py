from pydantic import BaseModel
from datetime import datetime
from ...models import Paginated
from enum import Enum
from ...models.user import UserIdentity
from ...models.academics.section_member import SectionMember


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


class OfficeHourGetHelpOverview(BaseModel):
    event_type: str
    event_mode: str
    event_start_time: datetime
    event_end_time: datetime
    ticket: OfficeHourTicketOverview | None
    queue_position: int


class OfficeHoursEventType(Enum):
    """
    Determines the type of an office hours event.
    """

    OFFICE_HOURS = "Office Hours"
    TUTORING = "Tutoring"
    REVIEW_SESSION = "Review Session"


class OfficeHoursEventModeType(Enum):
    """
    Determines the office hours event mode.
    """

    IN_PERSON = "In-Person"
    VIRTUAL_STUDENT_LINK = "Virtual - Student Link"
    VIRTUAL_OUR_LINK = "Virtual - Our Link"


class TicketState(Enum):
    """
    Determines the state of a ticket.
    """

    QUEUED = "Queued"
    CALLED = "Called"
    CLOSED = "Closed"
    CANCELED = "Cancelled"


class TicketType(Enum):
    """
    Determines the type of a ticket.
    """

    CONCEPTUAL_HELP = "Conceptual Help"
    ASSIGNMENT_HELP = "Assignment Help"


class OfficeHoursEventPartial(BaseModel):
    id: int


class OfficeHoursTicketDraft(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursTicket` that has not been created yet.
    """

    oh_event: OfficeHoursEventPartial
    description: str
    type: TicketType
    creators: list[UserIdentity] = []


class OfficeHoursTicket(OfficeHoursTicketDraft):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    created_at: datetime
    state: TicketState = TicketState.QUEUED
    called_at: datetime | None = None
    closed_at: datetime | None = None
    creators: list[SectionMember] = []
    caller: SectionMember | None = None
